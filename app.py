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
