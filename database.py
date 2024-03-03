import mysql.connector

def establish_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admiraljai_69",
        database="miniproject"
    )