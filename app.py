import streamlit as st
import mysql.connector

from database import establish_connection
from home import display_observations, insert_observation, delete_observation, update_observation_location, \
    display_species, insert_species, delete_species, update_species, display_cons, insert_cons, delete_cons, \
     display_Habitats, insert_Habitats, search_species, delete_Habitats, update_Habitats, display_data, \
    insert_data, delete_data, update_data, display_protected_by, insert_protected_by, delete_protected_by

# MySQL connection configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admiraljai_69",
    database="park"
)
cursor = db.cursor()

def update_protected_by_status(cursor):
    cursor.callproc("UpdateProtectedByStatus")

def update_cons(db, cursor):
    st.title("Update End_date")
    proj_id = st.text_input("Enter proj ID to update")
    end_date = st.date_input("Enter the deadline")

    if st.button("Update"):
        query = "UPDATE conservation_plan SET END_DATE = %s WHERE PROJ_ID = %s"
        try:
            cursor.execute(query, (end_date.strftime('%Y-%m-%d'), proj_id))
            db.commit()
            # Update conservation status in PROTECTED_BY table
            update_protected_by_status(cursor)
            st.success("New deadline updated successfully!")
        except Exception as e:
            st.error(f"Failed to update new deadline: {e}")
            db.rollback()
# Function to handle management/department login
def login(cursor):
    with st.expander("Login", expanded=True):
        login_identifier = st.text_input("Username or Email 📧")
        password = st.text_input("Password 🔒", type="password")

        if st.button("Login", key='login'):
            if not login_identifier or not password:
                st.error("Please enter both username/email and password.")
                return False

            cursor.execute(
                "SELECT * FROM ManagementUsers WHERE (BINARY username = %s OR BINARY email = %s) AND BINARY password = %s",
                (login_identifier, login_identifier, password))
            user = cursor.fetchone()
            if user:
                st.success("Logged in successfully! 🎉")
                st.session_state["logged_in"] = True
                st.experimental_rerun()
                return True
            else:
                st.error("Invalid username/email or password ❌")
                return False
    return False

def signup(cursor):
    with st.expander("Sign Up", expanded=True):
        new_username = st.text_input("New Username 🆕")
        new_email = st.text_input("New Email 📧")
        new_password = st.text_input("New Password 🔒", type="password")
        department = st.selectbox("Select Department", ["Operations", "Conservation"])

        if st.button("Sign Up", key='signup'):
            cursor.execute("SELECT * FROM ManagementUsers WHERE BINARY username = %s OR BINARY email = %s",
                           (new_username, new_email))
            existing_user = cursor.fetchone()
            if existing_user:
                st.error("Username or email already exists. Please choose a different username or email. ❌")
            else:
                cursor.execute(
                    "INSERT INTO ManagementUsers (username, email, password, department) VALUES (%s, %s, %s, %s)",
                    (new_username, new_email, new_password, department))
                db.commit()
                st.success("Sign up successful! You can now login. ✅")

def home_page():
    print()
    st.subheader("Welcome to the home page!!")
    # search_query = st.text_input("Search by species name, project name, wildlife preserve name, observation location, or data ID:")
    # if st.button("Search"):
    #     search_result = search_all(cursor, search_query)
    #     if search_result:
    #         st.write("### Search Results:")
    #         for result in search_result:
    #             st.write(result)
    #     else:
    #         st.write("No results found matching the search query.")
    with st.expander("Dashboard Options"):
        dashboard_option = st.selectbox("",["Home","Species", "Conservation Project", "Wildlife preserve Info", "Observation", "Environmental_data", "Protected By"])
    if dashboard_option == "":
        st.write("Welcome!!!")
    elif dashboard_option == "Species":
        st.write("Different Species")
        search_query = st.text_input("Search by species name or ID:")
        if st.button("Search"):
            species_data = search_species(cursor, search_query)

            if species_data:
                st.write("### Search Results:")
                for species in species_data:
                    st.write(f"Species ID: {species[0]}, Species Name: {species[1]}, Classification: {species[2]}")
            else:
                st.write("No species found matching the search query.")
        menu = st.sidebar.radio("Menu", ["Display Species", "Insert Species", "Delete Species",
                                         "Update Species"])
        if menu == "Display Species":
            display_species(cursor)
        elif menu == "Insert Species":
            insert_species(db, cursor)
        elif menu == "Delete Species":
            delete_species(db, cursor)
        elif menu == "Update Species":
            update_species(db, cursor)

        cursor.close()
        db.close()
        pass
    elif dashboard_option == "Conservation Project":
        st.write("Conservation Project Status")

        menu = st.sidebar.radio("Menu", ["Display Conservation Project", "Insert Conservation Project",
                                         "Delete Conservation Project",
                                         "Update Conservation Project"])

        if menu == "Display Conservation Project":
            display_cons(cursor)
        elif menu == "Insert Conservation Project":
            insert_cons(db, cursor)
            update_protected_by_status(cursor)  # Update conservation status in PROTECTED_BY table
            st.success("Conservation project inserted successfully!")
        elif menu == "Delete Conservation Project":
            delete_cons(db, cursor)
        elif menu == "Update Conservation Project":
            update_cons(db, cursor)

        cursor.close()
        db.close()

    elif dashboard_option == "Wildlife preserve Info":
        st.write("Wildlife preserve Info ")
        search_query = st.text_input("Search by Wildlife Preserve name or ID:")
        if st.button("Search"):
            species_data = search_species(cursor, search_query)

            if species_data:
                st.write("### Search Results:")
                for species in species_data:
                    st.write(f"Species_preserve ID: {species[0]}, Species_preserve Name: {species[1]}")
            else:
                st.write("No Wildlife Preserves found matching the search query.")
        menu = st.sidebar.radio("Menu", ["Display Wildlife preserve", "Insert Wildlife preserve","Delete Wildlife preserve","Update Wildlife preserve"])
        if menu == "Display Wildlife preserve":
            display_Habitats(cursor)
        elif menu == "Insert Wildlife preserve":
            insert_Habitats(db, cursor)
        elif menu == 'Delete Wildlife preserve':
            delete_Habitats(db,cursor)
        elif menu == "Update Wildlife preserve":
            update_Habitats(db,cursor)
        cursor.close()
        db.close()
    elif dashboard_option == "Observation":
        st.title("Observations Management System")
        search_query = st.text_input("Search by Observation ID or Location:")
        if st.button("Search"):
            if search_query.isdigit():
                query = "SELECT * FROM OBSERVATIONS WHERE OB_ID = %s"
                cursor.execute(query, (int(search_query),))
            else:
                query = "SELECT * FROM OBSERVATIONS WHERE OB_LOC LIKE %s"
                cursor.execute(query, ('%' + search_query + '%',))
            observations_data = cursor.fetchall()

            if observations_data:
                st.write("### Search Results:")
                for observation in observations_data:
                    st.write(f"Observation ID: {observation[0]}, Observation Location: {observation[1]}")
            else:
                st.write("No observations found matching the search query.")

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

    elif dashboard_option == ("Environmental_data"):
        st.title("Environmental Data")
        search_query = st.text_input("Search by Data ID")
        if st.button("Search"):
            if search_query.isdigit():
                query = "SELECT * FROM ENVIRONMENTAL_DATA WHERE D_ID = %s"
                cursor.execute(query, (int(search_query),))
            else:
                query = "SELECT * FROM ENVIRONMENTAL_DATA WHERE WATER_QUAL LIKE %s"
                cursor.execute(query, ('%' + search_query + '%',))
            environmental_data = cursor.fetchall()

            if environmental_data:
                st.write("### Search Results:")
                for data in environmental_data:
                    st.write(f"Data ID: {data[0]}, Water Quality: {data[1]}")
            else:
                st.write("No environmental data found matching the search query.")
        menu = st.sidebar.radio("Menu",["Display Environmental Data", "Insert Environmental Data", "Delete Environmental Data",
                                  "Update Environmental Data"])

        if menu == "Display Environmental Data":
            display_data(cursor)
        elif menu == "Insert Environmental Data":
            insert_data(db, cursor)
        elif menu == "Delete Environmental Data":
            delete_data(db, cursor)
        elif menu == "Update Environmental Data":
            update_data(db, cursor)

        cursor.close()
        db.close()
    elif dashboard_option == "Protected By":
        st.title("Protected By")
        search_query = st.text_input("Search by Species ID or Conservation ID")
        if st.button("Search"):
            if search_query.isdigit():
                query = "SELECT * FROM PROTECTED_BY WHERE SP_ID = %s"
                cursor.execute(query, (int(search_query),))
            else:
                query = "SELECT * FROM PROTECTED_BY WHERE CONSERVATION_STATUS LIKE %s"
                cursor.execute(query, ('%' + search_query + '%',))
            protected_data = cursor.fetchall()

            if protected_data:
                st.write("### Search Results:")
                for data in protected_data:
                    st.write(f"Species ID: {data[1]}, Conservation Status: {data[0]}, Project ID: {data[2]}")
            else:
                st.write("No protected data found matching the search query.")

        menu = st.sidebar.radio("Menu", ["Display Protected By", "Insert Protected By", "Delete Protected By"])

        if menu == "Display Protected By":
            display_protected_by(cursor)
        elif menu == "Insert Protected By":
            insert_protected_by(db, cursor)
        elif menu == "Delete Protected By":
            delete_protected_by(db, cursor)

        cursor.close()
        db.close()


def main():
    st.title("National Park Management System")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if st.session_state["logged_in"]:
        if st.button('Logout', key='logout'):
            st.session_state["logged_in"] = False
            st.experimental_rerun()
        st.write("You are logged in!")  # Add a debug statement to check if this is executed
        home_page()  # Check if home page content is called when logged in
    else:
        action = st.radio("Choose an option:", ["Login", "Sign Up"])

        if action == "Login":
            if login(cursor):
                st.write("Login successful!")
                home_page()
        elif action == "Sign Up":
            signup(cursor)

if __name__ == "__main__":
    main()
