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
