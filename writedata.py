'''Write Data into MySQL Database'''

import random
from datetime import datetime
import streamlit as st
import mysql.connector
from mysql_conn import mysqlconnect

def insert():
    '''Write Table Data'''
    st.title("Q-wizer")

    connection = mysqlconnect()
    cursor = connection.cursor()

    st.header("Create an Issue")

    customer_data = {}
    customer_columns = ['FName','LName','EmailAddress']
    for column in customer_columns:
        customer_data[column] = st.text_input(f"Enter {column}", "")

    emails_data = {}
    emails_columns = ['Content']

    for column in emails_columns:
        emails_data[column] = st.text_input(f"Enter {column}", "")

    incident_data = {}
    incident_columns = ['Priority']

    workson_data = {}

    for column in incident_columns:
        incident_data[column] = st.selectbox(f"Select {column}", ['Low', 'Medium', 'High', 'Critical'])

    if st.button("Add Data"):

        if all(customer_data.values()) and all(emails_data.values()) and all(incident_data.values()):
            #Create New Customer
            insert_customer = f"INSERT INTO Customer ({', '.join(customer_data.keys())}) VALUES ({', '.join(['%s']*len(customer_data))})"
            
            print("TRACE: [CUSTOMER DATA]",customer_data)    

            try:
                cursor.execute(insert_customer, tuple(customer_data.values()))
                connection.commit()
                extract_latest_customer = "SELECT CustomerID FROM Customer ORDER BY CustomerID DESC LIMIT 1"
            except mysql.connector.IntegrityError:
                extract_latest_customer = f"SELECT CustomerID FROM Customer WHERE EmailAddress = '{customer_data['EmailAddress']}'"

            cursor.execute(extract_latest_customer)
            latest_customer = cursor.fetchone()

            #Create New Email
            emails_data['CustomerID'] = latest_customer[0]

            extract_supportreps = "SELECT * FROM SupportRepresentative"
            cursor.execute(extract_supportreps)
            supportreps = cursor.fetchall()

            selected_supportreps = random.choice(supportreps)
            emails_data['EmployeeID'] = selected_supportreps[0]
            supportreps_fname = selected_supportreps[1]
            supportreps_lname = selected_supportreps[2]
            supportreps_email = selected_supportreps[3]

            emails_data['TimeSent'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print("TRACE: [EMAIL DATA]",emails_data)    

            insert_emails = f"INSERT INTO Emails ({', '.join(emails_data.keys())}) VALUES ({', '.join(['%s']*len(emails_data))})"

            try:
                cursor.execute(insert_emails, tuple(emails_data.values()))
                connection.commit()
            except mysql.connector.IntegrityError as e:
                print("Error: ", e)

            #Create New Incident
            incident_data['IssueDescription'] = emails_data['Content']

            incident_data['CreationDate'] = datetime.now().strftime('%Y-%m-%d')

            print("TRACE: [INCIDENT DATA]",incident_data)    

            insert_incident = f"INSERT INTO Incident ({', '.join(incident_data.keys())}) VALUES ({', '.join(['%s']*len(incident_data))})"

            try:
                cursor.execute(insert_incident, tuple(incident_data.values()))
                connection.commit()
            except mysql.connector.IntegrityError as e:
                print("Error: ", e)

            extract_latest_incident = "SELECT IncidentID FROM Incident ORDER BY IncidentID DESC LIMIT 1"
            cursor.execute(extract_latest_incident)
            latest_incident = cursor.fetchone()

            #Create New Works
            workson_data['IncidentID'] = latest_incident[0]
            workson_data['EmployeeID'] = emails_data['EmployeeID']

            print("TRACE: [WORKS ON DATA]", workson_data)

            insert_workson = f"INSERT INTO WorksOn ({', '.join(workson_data.keys())}) VALUES ({', '.join(['%s']*len(workson_data))})"

            try:
                cursor.execute(insert_workson, tuple(workson_data.values()))
                connection.commit()
            except mysql.connector.IntegrityError as e:
                print("Error: ", e)

            st.success("Data added successfully!")

            st.text("Incident Ticket generated with ID: " + str(workson_data['IncidentID']) + " and assigned to Support Representative: " + str(supportreps_fname) + " " + str(supportreps_lname) + " (" + str(supportreps_email) + ")")
            
        else:
            st.error("Please fill in all required fields.")

