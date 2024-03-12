import mysql.connector

def establish_connection():
    return mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database=""
    )

