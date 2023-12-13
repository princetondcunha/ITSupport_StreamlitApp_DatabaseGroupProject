'''MySQL Connection'''

import os
from dotenv import load_dotenv
import mysql.connector

def mysqlconnect():
    '''Connect to MySQL Database'''
    load_dotenv()

    host = os.getenv("HOST")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")

    db_config = {
        'host': host,
        'user': user,
        'password': password,
        'database': database,
    }

    connection = mysql.connector.connect(**db_config)
    return connection
