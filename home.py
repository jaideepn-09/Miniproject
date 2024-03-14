import streamlit as st

from database import establish_connection
from datetime import datetime, timedelta

def homepage(db):
    st.title("Home Page")
    st.write("Welcome to the homepage!")

    st.subheader("Dashboard")
    dashboard_option = st.radio("Select an option:", ["Update", "Conservation Project Status", "Habitats Info", "Observation"])

    if dashboard_option == "Species":
        st.write("Species Management")
        if dashboard_option == "Display Species":
            display_species(db)

        elif dashboard_option == "Insert Species":
            insert_species(db)

        elif dashboard_option == "Update Species":
            update_species(db)

        elif dashboard_option == "Delete Species":
            delete_species(db)

    elif dashboard_option == "Conservation Project Status":
        st.write("Conservation Project Status")
        if dashboard_option == "Display Conservation Project Status":
            display_cons(db)

        elif dashboard_option == "Insert Conservation Project Status":
            insert_cons(db)

        elif dashboard_option == "Update Conservation Project Status":
            update_cons(db)

        elif dashboard_option == "Delete Conservation Project Status":
            delete_cons(db)

    elif dashboard_option == "Habitats Info":
        st.write("Habitats Info option selected")

    elif dashboard_option == "Observation":
        st.write("Observation option selected")

# def search_all(cursor, search_query):
#     # Search in OBSERVATIONS table
#     query = "SELECT * FROM OBSERVATIONS WHERE OB_ID = %s OR OB_LOC LIKE %s"
#     cursor.execute(query, (int(search_query), '%' + search_query + '%'))
#     observation_data = cursor.fetchall()
#
#     # Search in SPECIES table
#     query = "SELECT * FROM SPECIES WHERE SP_ID = %s OR SP_NAME LIKE %s OR SP_CLASSIFICATION LIKE %s"
#     cursor.execute(query, (int(search_query), '%' + search_query + '%', '%' + search_query + '%'))
#     species_data = cursor.fetchall()
#
#     # Search in CONSERVATION_PLAN table
#     query = "SELECT * FROM CONSERVATION_PLAN WHERE PROJ_ID = %s OR PROJ_NAME LIKE %s"
#     cursor.execute(query, (int(search_query), '%' + search_query + '%'))
#     conservation_projects_data = cursor.fetchall()
#
#     # Search in HABITATS table
#     query = "SELECT * FROM SPECIES_PRESERVES WHERE PID = %s OR PNAME LIKE %s"
#     cursor.execute(query, (int(search_query), '%' + search_query + '%'))
#     habitat_data = cursor.fetchall()
#
#     # Search in ENVIRONMENTAL_DATA table
#     query = "SELECT * FROM ENVIRONMENTAL_DATA WHERE D_ID = %s OR WATER_QUAL LIKE %s"
#     cursor.execute(query, (int(search_query), '%' + search_query + '%'))
#     environmental_data = cursor.fetchall()
#
#     # Search in PROTECTED_BY table
#     query = "SELECT * FROM PROTECTED_BY WHERE SP_ID = %s OR CONSERVATION_STATUS LIKE %s"
#     cursor.execute(query, (int(search_query), '%' + search_query + '%'))
#     protected_data = cursor.fetchall()
#
#     # Combine all search results
#     all_results = {
#         "Observations": observation_data,
#         "Species": species_data,
#         "Conservation Projects": conservation_projects_data,
#         "Habitats": habitat_data,
#         "Environmental Data": environmental_data,
#         "Protected Data": protected_data
#     }
#
#     return all_results
#
#
# def search_across_all(cursor):
#     search_query = st.text_input("Search across all data:")
#     if st.button("Search"):
#         search_results = search_all(cursor, search_query)
#
#         for table_name, data in search_results.items():
#             if data:
#                 st.write(f"### Search Results in {table_name}:")
#                 for row in data:
#                     st.write(row)
#             else:
#                 st.write(f"No results found in {table_name}.")

def display_species(cursor):
            st.title("Display Species")
            query = "SELECT * FROM SPECIES"
            cursor.execute(query)
            specieses = cursor.fetchall()

            if specieses:
                st.write("### Observations")
                for species in specieses:
                    st.write(
                        f"Species ID: {species[0]}, Species name: {species[1]}, Classification: {species[2]}")
            else:
                st.write("No Species found.")
def search_species(cursor, search_query):
    if search_query.isdigit():
        query = "SELECT * FROM SPECIES WHERE SP_ID = %s"
        cursor.execute(query, (int(search_query),))
    else:
        query = "SELECT * FROM SPECIES WHERE SP_NAME LIKE %s"
        cursor.execute(query, ('%' + search_query + '%',))
    species_data = cursor.fetchall()
    return species_data
def insert_species(db, cursor):
            st.title("Insert Species")
            sp_id = st.text_input("Species ID")
            sp_name = st.text_input("Species name")
            sp_classification = st.text_input("Species Classification")

            if st.button("Submit"):
                query = "INSERT INTO SPECIES (SP_ID,SP_NAME, SP_CLASSIFICATION) VALUES (%s, %s, %s)"
                values = (sp_id, sp_name, sp_classification)
                try:
                    cursor.execute(query, values)
                    db.commit()
                    st.success("Species added successfully!")
                except Exception as e:
                    st.error(f"Failed to add Species: {e}")
                    db.rollback()

def delete_species(db, cursor):
    st.title("Delete Species")
    sp_id = st.number_input("Enter Species ID to delete", min_value=100, max_value=999, step=1)

    if st.button("Delete"):
        # Check if species ID exists
        cursor.execute("SELECT * FROM SPECIES WHERE SP_ID = %s", (sp_id,))
        species = cursor.fetchone()

        if species:
            try:
                # Delete species if found
                query = "DELETE FROM SPECIES WHERE SP_ID = %s"
                cursor.execute(query, (sp_id,))
                db.commit()
                st.success("Species deleted successfully!")
            except Exception as e:
                st.error(f"Failed to delete species: {e}")
                db.rollback()
        else:
            st.warning("Species not found.")



def update_species(db, cursor):
            st.title("Update species Location")
            sp_id = st.text_input("Enter species ID to update")
            new_name = st.text_input("Enter name of the species")

            if st.button("Update"):
                query = "UPDATE SPECIES SET SP_NAME = %s WHERE SP_ID = %s"
                try:
                    cursor.execute(query, (new_name, sp_id))
                    db.commit()
                    st.success("New species updated successfully!")
                except Exception as e:
                    st.error(f"Failed to update new species: {e}")
                    db.rollback()

def display_Habitats(cursor):
    st.title("Display Wildlife Preserve")
    query = "SELECT * FROM SPECIES_PRESERVES"
    cursor.execute(query)
    Habitats = cursor.fetchall()

    if Habitats:
        st.write("### WILDLIFE PRESERVE")
        for Habitat in Habitats:
            st.write(f"PID: {Habitat[0]}, PNAME: {Habitat[1]}, PLOC: {Habitat[2]}, PECOSYSTEM: {Habitat[3]}, SP_ID: {Habitat[4]}")
    else:
        st.write("No Wildlife Preserve found.")

def insert_Habitats(db, cursor):
    st.title("Insert Preserve")
    pid = st.text_input("Preserve ID")
    pname = st.text_input("Preserve Name")
    ploc = st.text_input("PreserveLocation")
    pecosystem = st.text_input("Preserveecosystem")
    sp_id = st.text_input("Species ID")

    if st.button("Submit"):
        query = "INSERT INTO species_preserves (P_ID, PNAME, PLOC,PECOSYSTEM, SP_ID) VALUES (%s, %s, %s, %s, %s)"
        values = (pid, pname, ploc,pecosystem, sp_id)
        try:
            cursor.execute(query, values)
            db.commit()
            st.success("Wildife preserve added successfully!")
        except Exception as e:
            st.error(f"Failed to add Wildlife preserve: {e}")
            db.rollback()
def search_Habitats(cursor, search_query):
    if search_query.isdigit():
        query = "SELECT * FROM SPECIES_PRESERVES WHERE PID = %s"
        cursor.execute(query, (int(search_query),))
    else:
        query = "SELECT * FROM SPECIES_PRESERVES WHERE PNAME LIKE %s"
        cursor.execute(query, ('%' + search_query + '%',))
    habitats_data = cursor.fetchall()
    return habitats_data
def delete_Habitats(db, cursor):
    st.title("Delete Wildlife Preserve")
    pid = st.text_input("Enter WildLife Preserve ID to delete")

    if st.button("Delete"):
        query = "DELETE FROM SPECIES_PRESERVES WHERE PID = %s"
        try:
            cursor.execute(query, (pid,))
            db.commit()
            if cursor.rowcount > 0:
                st.success("Wildlife Preserve deleted successfully!")
            else:
                st.warning("Wildlife preserve not found.")
        except Exception as e:
            st.error(f"Failed to delete Wildlife preserve: {e}")
            db.rollback()

def update_Habitats(db, cursor):
    st.title("Update Wildlife preserve ")
    pid = st.text_input("Enter Wildlife preserve ID to update")
    ploc = st.text_input("Enter updated Wildlife preserve Location")

    if st.button("Update"):
        query = "UPDATE SPECIES_PRESERVES SET PLOC = %s WHERE PID = %s"
        try:
            cursor.execute(query, (ploc, pid))
            db.commit()
            st.success("Wildlife preserve updated successfully!")
        except Exception as e:
            st.error(f"Failed to update Wildlife preserve: {e}")
            db.rollback()
def display_cons(cursor):
    st.title("Display Conservation Project Status")
    query = "SELECT * FROM conservation_plan"
    cursor.execute(query)
    conserves = cursor.fetchall()

    if conserves:
        st.write("### Conservation Projects")
        for conserve in conserves:
            st.write(
                f"Project ID: {conserve[0]}, Project name: {conserve[1]}, Start_date: {conserve[2]}, End_date: {conserve[3]}, SP_ID: {conserve[4]}")
    else:
        st.write("No Conservation Project found.")


def insert_cons(db, cursor):
    st.title("Insert Conservation Project")
    proj_id = st.text_input("Project ID")
    proj_name = st.text_input("Project name")
    today = datetime.today()
    min_date = today - timedelta(days=365 * 100)
    max_date = today + timedelta(days=365 * 100)
    str_date = st.date_input("Start date",min_value=min_date, max_value=max_date)
    end_date = st.date_input("End date",min_value=min_date, max_value=max_date)
    sp_id = st.text_input("Species ID")

    if st.button("Submit"):
        query = "INSERT INTO conservation_plan(PROJ_ID,PROJ_NAME, STR_DATE, END_DATE,SP_ID) VALUES (%s, %s, %s,%s,%s)"
        values = (proj_id,proj_name,str_date,end_date,sp_id)
        try:
            cursor.execute(query, values)
            db.commit()
            st.success("Project added successfully!")
        except Exception as e:
            st.error(f"Failed to add Project: {e}")
            db.rollback()


def delete_cons(db, cursor):
    st.title("Delete Project")
    proj_id = st.text_input("Enter Project ID to delete")

    if st.button("Delete"):
        query = "DELETE FROM conservation_plan WHERE proj_ID = %s"
        try:
            cursor.execute(query, (proj_id,))
            db.commit()
            if cursor.rowcount > 0:
                st.success("Project deleted successfully!")
            else:
                st.warning("Project not found.")
        except Exception as e:
            st.error(f"Failed to delete Project: {e}")
            db.rollback()

# Example usage:
# update_cons(db_connection, db_cursor)


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

def search_observations(cursor, search_query):
    if search_query.isdigit():
        query = "SELECT * FROM OBSERVATIONS WHERE OB_ID = %s"
        cursor.execute(query, (int(search_query),))
    else:
        query = "SELECT * FROM OBSERVATIONS WHERE OB_LOC LIKE %s"
        cursor.execute(query, ('%' + search_query + '%',))
    observations_data = cursor.fetchall()
    return observations_data

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
            if cursor.rowcount > 0:
                st.success("Observation deleted successfully!")
            else:
                st.warning("Observation not found.")
        except Exception as e:
            st.error(f"Failed to delete Observation: {e}")
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

def display_data(cursor):
    st.title("Display Environmental Data")
    query = "SELECT * FROM ENVIRONMENTAL_DATA"
    cursor.execute(query)
    environmental_data = cursor.fetchall()

    if environmental_data:
        st.write("### ENVIRONMENTAL DATA")
        for data in environmental_data:
            st.write(f"D_ID: {data[0]}, WATER_QUAL: {data[1]}, WEATHER_COND: {data[2]}, SOIL_COMP: {data[3]}, AIR_QUAL: {data[4]}, PID: {data[5]}")
    else:
        st.write("No environmental data found.")

def search_environmental_data(cursor, search_query):
    if search_query.isdigit():
        query = "SELECT * FROM ENVIRONMENTAL_DATA WHERE D_ID = %s"
        cursor.execute(query, (int(search_query),))
    else:
        query = "SELECT * FROM ENVIRONMENTAL_DATA WHERE WATER_QUAL LIKE %s"
        cursor.execute(query, ('%' + search_query + '%',))
    environmental_data = cursor.fetchall()
    return environmental_data

def insert_data(db, cursor):
    st.title("Insert Environmental Data")
    d_id = st.text_input("Data ID")
    water_qual = st.text_input("Water Quality")
    weather_cond = st.text_input("Weather Conditions")
    soil_comp = st.text_input("Soil Composition")
    air_qual = st.text_input("Air Quality")
    pid = st.text_input("Habitat ID")

    if st.button("Submit"):
        query = "INSERT INTO ENVIRONMENTAL_DATA (D_ID, WATER_QUAL, WEATHER_COND, SOIL_COMP, AIR_QUAL, PID) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (d_id, water_qual, weather_cond, soil_comp, air_qual, pid)
        try:
            cursor.execute(query, values)
            db.commit()
            st.success("Environmental data added successfully!")
        except Exception as e:
            st.error(f"Failed to add environmental data: {e}")
            db.rollback()

def delete_data(db, cursor):
    st.title("Delete Environmental Data")
    d_id = st.text_input("Enter Data ID to delete")

    if st.button("Delete"):
        query = "DELETE FROM ENVIRONMENTAL_DATA WHERE D_ID = %s"
        try:
            cursor.execute(query, (d_id,))
            db.commit()
            if cursor.rowcount > 0:
                st.success("Environmental Data deleted successfully!")
            else:
                st.warning("Environmental Data not found.")
        except Exception as e:
            st.error(f"Failed to delete Environmental Data: {e}")
            db.rollback()

def update_data(db, cursor):
    st.title("Update Environmental Data")
    d_id = st.text_input("Enter Data ID to update")
    air_qual = st.text_input("Enter updated Air Quality")

    if st.button("Update"):
        query = "UPDATE ENVIRONMENTAL_DATA SET AIR_QUAL = %s WHERE D_ID = %s"
        try:
            cursor.execute(query, (air_qual, d_id))
            db.commit()
            st.success("Environmental data updated successfully!")
        except Exception as e:
            st.error(f"Failed to update environmental data: {e}")
            db.rollback()
def insert_protected_by(db, cursor):
    st.title("Insert Protected By")
    conservation_status = st.text_input("Conservation Status")
    sp_id = st.text_input("Species ID")
    proj_id = st.text_input("Project ID")

    if st.button("Submit"):
        query = "INSERT INTO PROTECTED_BY (CONSERVATION_STATUS, SP_ID, PROJ_ID) VALUES (%s, %s, %s)"
        values = (conservation_status, sp_id, proj_id)
        try:
            cursor.execute(query, values)
            db.commit()
            st.success("Data inserted into PROTECTED_BY table successfully!")
        except Exception as e:
            st.error(f"Failed to insert data into PROTECTED_BY table: {e}")
            db.rollback()
def display_protected_by(cursor):
    st.title("Display Protected By")
    query = "SELECT * FROM PROTECTED_BY"
    cursor.execute(query)
    protected_data = cursor.fetchall()

    if protected_data:
        st.write("### Protected By Data")
        for data in protected_data:
            st.write(f"Species ID: {data[1]}, Conservation Status: {data[0]}, Project ID: {data[2]}")
    else:
        st.write("No protected data found.")

def insert_protected_by(db, cursor):
    st.title("Insert Protected By")
    conservation_status = st.text_input("Conservation Status")
    sp_id = st.text_input("Species ID")
    proj_id = st.text_input("Project ID")

    if st.button("Submit"):
        query = "INSERT INTO PROTECTED_BY (CONSERVATION_STATUS, SP_ID, PROJ_ID) VALUES (%s, %s, %s)"
        values = (conservation_status, sp_id, proj_id)
        try:
            cursor.execute(query, values)
            db.commit()
            st.success("Data inserted into PROTECTED_BY table successfully!")
        except Exception as e:
            st.error(f"Failed to insert data into PROTECTED_BY table: {e}")
            db.rollback()

def delete_protected_by(db, cursor):
    st.title("Delete Protected By")
    sp_id = st.text_input("Enter Species ID to delete")

    if st.button("Delete"):
        query = "DELETE FROM PROTECTED_BY WHERE SP_ID = %s"
        try:
            cursor.execute(query, (sp_id,))
            db.commit()
            if cursor.rowcount > 0:
                st.success("Data deleted from PROTECTED_BY table successfully!")
            else:
                st.warning("Data with provided Species ID not found in PROTECTED_BY table.")
        except Exception as e:
            st.error(f"Failed to delete data from PROTECTED_BY table: {e}")
            db.rollback()

if __name__ == "__main__":
    db = establish_connection()
    homepage(db)
