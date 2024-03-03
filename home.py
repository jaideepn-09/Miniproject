import streamlit as st
from database import establish_connection

def homepage(db):
    st.title("Home Page")
    st.write("Welcome to the homepage!")

    st.subheader("Dashboard")
    dashboard_option = st.radio("Select an option:", ["Update", "Conservation Project Status", "Habitats Info", "Observation"])

    if dashboard_option == "Species":
        st.write("Species Management")

    elif dashboard_option == "Conservation Project Status":
        st.write("Conservation Project Status option selected")

    elif dashboard_option == "Habitats Info":
        st.write("Habitats Info option selected")

    elif dashboard_option == "Observation":
        st.write("Observation option selected")

def display_observations(cursor):
    st.title("Display Observations")
    query = "SELECT * FROM OBSERVATIONS"
    cursor.execute(query)
    observations = cursor.fetchall()

    if observations:
        st.write("### Observations")
        for observation in observations:
            st.write(f"ID: {observation[0]}, Date: {observation[1]}, Location: {observation[2]}, Species ID: {observation[3]}, Data ID: {observation[4]}")
    else:
        st.write("No observations found.")

def insert_observation(db, cursor):
    st.title("Insert Observation")
    ob_id = st.text_input("Observation ID")
    ob_date = st.date_input("Date")
    ob_loc = st.text_input("Location")
    sp_id = st.text_input("Species ID")
    d_id = st.text_input("Data ID")

    if st.button("Submit"):
        query = "INSERT INTO OBSERVATIONS (OB_ID, OB_DATE, OB_LOC, SP_ID, D_ID) VALUES (%s, %s, %s, %s, %s)"
        values = (ob_id, ob_date, ob_loc, sp_id, d_id)
        try:
            cursor.execute(query, values)
            db.commit()
            st.success("Observation added successfully!")
        except Exception as e:
            st.error(f"Failed to add observation: {e}")
            db.rollback()

def delete_observation(db, cursor):
    st.title("Delete Observation")
    ob_id = st.number_input("Enter Observation ID to delete", min_value=1, step=1)

    if st.button("Delete"):
        query = "DELETE FROM OBSERVATIONS WHERE OB_ID = %s"
        try:
            cursor.execute(query, (ob_id,))
            db.commit()
            st.success("Observation deleted successfully!")
        except Exception as e:
            st.error(f"Failed to delete observation: {e}")
            db.rollback()

def update_observation_location(db, cursor):
    st.title("Update Observation Location")
    ob_id = st.number_input("Enter Observation ID to update", min_value=1, step=1)
    new_location = st.text_input("Enter new location")

    if st.button("Update"):
        query = "UPDATE OBSERVATIONS SET OB_LOC = %s WHERE OB_ID = %s"
        try:
            cursor.execute(query, (new_location, ob_id))
            db.commit()
            st.success("Observation location updated successfully!")
        except Exception as e:
            st.error(f"Failed to update observation location: {e}")
            db.rollback()

if __name__ == "__main__":
    db = establish_connection()
    homepage(db)
