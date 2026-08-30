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
                .first()
    )
    if existing_user:
        st.error("Email already registered.")
    else:
        salt = secrets.token_hex(16)
        new_user = User(
                        name=name,
            email=email,
            password=
                salt + ":" +
                hashlib.sha256(
                    (salt + password).encode()
                ).hexdigest()
                    )
        db.add(new_user)
        db.commit()
        st.success("Registration successful!")
    db.close()
st.header("Available Subsidies")
db = SessionLocal()
subsidies = db.query(Subsidy).all()
for subsidy in subsidies:
    st.subheader(subsidy.name)
    st.write(subsidy.description)
    st.write("Amount: ₹", subsidy.amount)
    st.write(
                "Eligibility:",
        subsidy.eligibility
    )
    with st.form(f"apply_{subsidy.id}"):
        email = st.text_input(
            "Farmer Email",
            key=f"email_{subsidy.id}"
                    )
        land_area = st.number_input(
            "Land Area (acres)",
            min_value=0.0,
            key=f"land_{subsidy.id}"
        )
        crop = st.text_input(
                        "Crop",
            key=f"crop_{subsidy.id}"
        )
        apply_button = st.form_submit_button(
            "Apply for this Subsidy"
        )
        if apply_button:
            user = (
                            db.query(User)
                .filter(User.email == email)
                .first()
            )
            if user is None:
                st.error(
                    "Farmer not registered. Please register first."
                )
                            else:
                application = Application(
                    user_id=user.id,
                    subsidy_id=subsidy.id,
                    land_area=land_area,
                    crop=crop,
                    status="Pending"
                )
                db.add(application)
                db.commit()
                st.success(
                    "Application submitted successfully!"
                )
    st.divider()
st.header("My Applications")
if st.session_state.logged_in:
    my_applications = (
        db.query(Application)
        .filter(
            Application.user_id ==
            st.session_state.user_id
        )
        .all()
    )
        if my_applications:
        for application in my_applications:
            subsidy = (
                db.query(Subsidy)
                .filter(
                    Subsidy.id ==
                    application.subsidy_id
                )
                .first()
            )
            st.subheader(
                subsidy.name
                if subsidy
                else "Unknown Subsidy"
            )
                        st.write(
                "Land Area:",
                application.land_area,
                "acres"
            )
            st.write(
                "Crop:",
                application.crop
            )
            st.write(
                "Status:",
                application.status
            )
            st.divider()
    else:
        st.info(
            "You have not submitted any applications yet."
        )
db.close()
st.header("Admin Dashboard")
admin_password = st.text_input(
    "Admin Password",
    type="password"
)
if admin_password == "admin123":
    st.success("Admin access granted!")
    admin_db = SessionLocal()
    applications = (
        admin_db.query(Application).all()
    )
    st.subheader("Subsidy Applications")
    for application in applications:
        user = (
            admin_db.query(User)
            .filter(User.id == application.user_id)
            .first()
        )
        subsidy = (
            admin_db.query(Subsidy)
            .filter(Subsidy.id == application.subsidy_id)
            .first()
        )
        st.write(
            "Farmer:",
            user.name if user else "Unknown"
        )
        st.write(
            "Email:",
            user.email if user else "Unknown"
        )
        st.write(
            "Subsidy:",
            subsidy.name if subsidy else "Unknown"
        )
        st.write(
            "Land Area:",
            application.land_area
        )
        st.write(
            "Crop:",
            application.crop
        )
        st.write(
            "Status:",
            application.status
        )
        col1, col2 = st.columns(2)
        if col1.button(
            "Approve",
            key=f"approve_{application.id}"
        ):
            application.status = "Approved"
            admin_db.commit()
            st.success(
                "Application approved!"
            )
            st.rerun()
        if col2.button(
            "Reject",
            key=f"reject_{application.id}"
        ):
            application.status = "Rejected"
            admin_db.commit()
            st.warning(
                "Application rejected!"
            )
            st.rerun()
        st.divider()
    admin_db.close()


        
