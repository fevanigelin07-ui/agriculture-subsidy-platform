import streamlit as st
import hashlib
import secrets
from database import engine, Base, SessionLocal
from models import User, Subsidy, Application
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
Base.metadata.create_all(bind=engine)
db = SessionLocal()
if db.query(Subsidy).count() == 0:
    db.add_all([
        Subsidy(
            name="Crop Subsidy",
            description="Financial support for crop cultivation",
            amount=10000,
            eligibility="Small and medium farmers"
        ),
        Subsidy(
            name="Equipment Subsidy",
            description="Support for purchasing agricultural equipment",
            amount=25000,
            eligibility="Registered farmers"
        ),
        Subsidy(
            name="Irrigation Subsidy",
            description="Support for irrigation facilities",
            amount=15000,
            eligibility="Farmers with agricultural land"
                )
    ])
    db.commit()

db.close()
st.title("🌾 Agriculture Subsidy Application Platform")
st.header("Farmer Login")
with st.form("login_form"):
    login_email = st.text_input("Email")
    login_password = st.text_input(
        "Password",
        type="password"
    )
    login_button = st.form_submit_button("Login")
if login_button:
    db = SessionLocal()
        user = (
        db.query(User)
        .filter(User.email == login_email)
        .first()
    )
    if user:
        salt, stored_hash = user.password.split(":", 1)
                login_hash = hashlib.sha256(
            (salt + login_password).encode()
        ).hexdigest()
        if login_hash == stored_hash:
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
                        st.session_state.user_name = user.name
            st.success(f"Welcome, {user.name}!")
        else:
            st.error("Invalid email or password.")
    else:
        st.error("Invalid email or password.")
       db.close()
if st.session_state.logged_in:
    st.success(
        f"Logged in as {st.session_state.user_name}"
    )
    if st.button("Logout"):
                st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
st.success("Database connected successfully!")
st.header("Farmer Registration")
with st.form("registration_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
            )
    register = st.form_submit_button("Register")
if register:
    db = SessionLocal()
    existing_user = (
        db.query(User)
        .filter(User.email == email)
