import streamlit as st
import mysql.connector
from home import display_observations, insert_observation, delete_observation, update_observation_location
# MySQL connection configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admiraljai_69",
    database="miniproject"
)
cursor = db.cursor()

# Function to handle management/department login
def login():
    st.title("Management/Department Login")
    login_identifier = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Validate login credentials against database
        cursor.execute("SELECT * FROM ManagementUsers WHERE (username = %s OR email = %s) AND password = %s",
                       (login_identifier, login_identifier, password))
        user = cursor.fetchone()
        if user:
            st.success("Logged in successfully!")
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username/email or password")

# Function to handle management/department signup
def signup():
    st.title("Management/Department Sign Up")
    new_username = st.text_input("New Username")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    department = st.selectbox("Select Department", ["Operations", "Conservation"])

    if st.button("Sign Up"):
        # Check if username or email already exists
        cursor.execute("SELECT * FROM ManagementUsers WHERE username = %s OR email = %s", (new_username, new_email))
        existing_user = cursor.fetchone()
        if existing_user:
            st.error("Username or email already exists. Please choose a different username or email.")
        else:
            # Insert new user into database
            cursor.execute("INSERT INTO ManagementUsers (username, email, password, department) VALUES (%s, %s, %s, %s)",
                           (new_username, new_email, new_password, department))
            db.commit()
            st.success("Sign up successful! You can now login.")

# Function to display home page with dashboard
def home_page():
    st.title("Home Page")
    st.write("Welcome to the home page!!")

    st.subheader("Dashboard")
    dashboard_option = st.radio("Select an option:",
                                ["Species", "Conservation Project Status", "Habitats Info", "Observation"])

    if dashboard_option == "Species":
        st.write("Different Species")

    elif dashboard_option == "Conservation Project Status":
        st.write("Conservation Project Status option selected")

    elif dashboard_option == "Habitats Info":
        st.write("Habitats Info option selected")

    elif dashboard_option == "Observation":
        st.write("Observation option selected")

        st.title("Observations Management System")


        menu = st.sidebar.radio("Menu", ["Display Observations", "Insert Observation", "Delete Observation",
                                 "Update Observation Location"])

        if menu == "Display Observations":
            display_observations(cursor)
        elif menu == "Insert Observation":
            insert_observation(db, cursor)
        elif menu == "Delete Observation":
            delete_observation(db, cursor)
        elif menu == "Update Observation Location":
            update_observation_location(db, cursor)

        cursor.close()
        db.close()

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

def main():
    st.title("National Park Management System")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        home_page()

    else:
        action = st.radio("Choose an option:", ["Login", "Sign Up"])

        if action == "Login":
            login()
        elif action == "Sign Up":
            signup()

if __name__ == "__main__":
    main()
