import requests
import streamlit as st
import mysql.connector
from mysql.connector import cursor

from app import db
from database import establish_connection


def signup():
    st.title("Management/Department Sign Up")
    new_username = st.text_input("New Username")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    department = st.selectbox("Select Department", ["Operations", "Conservation"])

    if st.button("Sign Up"):
        cursor.execute("SELECT * FROM ManagementUsers WHERE username = %s OR email = %s", (new_username, new_email))
        existing_user = cursor.fetchone()
        if existing_user:
            st.error("Username or email already exists. Please choose a different username or email.")
        else:
            cursor.execute("INSERT INTO ManagementUsers (username, email, password, department) VALUES (%s, %s, %s, %s)", (new_username, new_email, new_password, department))
            db.commit()
            st.success("Sign up successful! You can now login.")
def login():
    st.title("Management/Department Login")
    login_identifier = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM ManagementUsers WHERE (username = %s OR email = %s) AND password = %s", (login_identifier, login_identifier, password))
        user = cursor.fetchone()
        if user:
            st.session_state.logged_in = True
        else:
            st.error("Invalid username/email or password")