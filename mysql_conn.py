'''MySQL Connection'''

import os
from dotenv import load_dotenv
import mysql.connector

def mysqlconnect():
    '''Connect to MySQL Database'''
    
    db_config = {
        'host': 'dbcourse.cs.smu.ca',
        'user': 'u10',
        'password': 'positionCLEANquarter91',
        'database': 'u10',
    }

    connection = mysql.connector.connect(**db_config)
    return connection
