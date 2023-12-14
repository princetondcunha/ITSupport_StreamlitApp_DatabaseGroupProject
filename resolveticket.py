import random
from datetime import datetime
import streamlit as st
import mysql.connector
from mysql_conn import mysqlconnect


def is_incident_id_exists(incident_id, cursor):
    connection = mysqlconnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM Incident WHERE IncidentID = {incident_id}")
    return cursor.fetchone() is not None

def is_knowledge_id_exists(knowledge_id, cursor):
    connection = mysqlconnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM KnowledgeBase WHERE KB_ID = {knowledge_id}")
    return cursor.fetchone() is not None

def has_knowledge_id(incident_id, cursor):
    connection = mysqlconnect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM Incident WHERE IncidentID = {incident_id} AND KnowledgeBaseID IS NOT NULL")
    return cursor.fetchone() is not None

def update_knowledge_id(incident_id, knowledge_id, cursor):
    connection = mysqlconnect()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE Incident SET KnowledgeBaseID = {knowledge_id} WHERE IncidentID = {incident_id}")
    connection.commit()

def resolveticket():
    '''Write Table Data'''
    st.title("Q-wizer")

    connection = mysqlconnect()
    cursor = connection.cursor()

    st.header("Resolve Ticket")
    incident_id = st.text_input("Incident ID")
    
    action = st.selectbox("Select Action", ["Map Existing Solution", "Create New Solution"])
    if action == "Map Existing Solution":
        knowledge_base_id = st.text_input("Enter Knowledge Base ID")

    if action == "Create New Solution":
        issue_type = st.text_input("Enter issue type")
        answer_template = st.text_input("Enter answer template")


    if action == "Create New Solution" and st.button("Resolve"):
        try:
            incident_id = int(incident_id)
        except ValueError:
            st.error("Incident ID should be a number. Please enter a valid number.")
        
        if is_incident_id_exists(incident_id, cursor):
            counter1 = 1
            print(f"{incident_id} Available")
        else:
            print(f"Incident ID {incident_id} is unavailable.")
            counter1 = 0
            st.error(f"Incident ID {incident_id} not found. Please enter a valid Incident ID.")
        
        if not has_knowledge_id(incident_id, cursor):
            counter2 = 1
            print("Knowledgebase Null")
        else:
            print("Knowledgebase has value")
            counter2 = 0
            st.error(f"Incident ID {incident_id} has a solution already.")
        
        if( counter1*counter2 ):
            try:
                max_kb_id_query = "SELECT MAX(KB_ID) FROM KnowledgeBase"
                cursor.execute(max_kb_id_query)
                max_kb_id = cursor.fetchone()[0] or 0  # Default to 0 if no existing records
                new_kb_id = max_kb_id + 1
                insert_query = f"INSERT INTO KnowledgeBase (KB_ID, IssueType, AnswerTemplate) VALUES ({new_kb_id}, '{issue_type}', '{answer_template}')"
                cursor.execute(insert_query)
                connection.commit()
                print(f"Data added to KnowledgeBase with KB_ID: {new_kb_id}")
                update_knowledge_id(incident_id, new_kb_id, cursor)
                st.success("Ticket resolved successfully!")

            except Exception as e:
                st.error(f"An error occurred while adding data to KnowledgeBase")
            
    if action == "Map Existing Solution" and st.button("Resolve"):
        try:
            incident_id = int(incident_id)
        except ValueError:
            st.error("Incident ID should be a number. Please enter a valid number.")
        
        if is_incident_id_exists(incident_id, cursor):
            counter1 = 1
            print(f"{incident_id} Available")
        else:
            print(f"Incident ID {incident_id} is unavailable.")
            counter1 = 0
            st.error(f"Incident ID {incident_id} not found. Please enter a valid Incident ID.")
            
        if not has_knowledge_id(incident_id, cursor):
            counter2 = 1
            print("Knowledgebase Null")
        else:
            print("Knowledgebase has value")
            counter2 = 0
            st.error(f"Incident ID {incident_id} has a solution already.")
        
        try:
            knowledge_id = int(knowledge_base_id)
        except ValueError:
            st.error("Knowledge ID should be a number. Please enter a valid number.")
        
        if is_knowledge_id_exists(knowledge_id, cursor):
            counter3 = 1
            print(f"{knowledge_id} Available")
        else:
            print(f"Knowledge ID {knowledge_id} is not available.")
            counter3 = 0
            st.error(f"Knowledge ID {knowledge_id} not found. Please enter a valid Knowledge ID.")
        
        if( counter1 * counter2 * counter3 ):
            update_knowledge_id(incident_id, knowledge_id, cursor)
            st.success("Ticket resolved successfully!")
       
valid_credentials = {"username": "admin", "password": "admin"}
is_logged_in = False

def login_page():
    global is_logged_in
    title_container = st.empty()
    input_container = st.empty()
    password_container = st.empty()
    button_container = st.empty()

    if not is_logged_in:
        title_container.title("Login")
        username = input_container.text_input("Username")
        password = password_container.text_input("Password", type="password")
        login_button = button_container.button("Login")

        if login_button:
            if username == valid_credentials["username"] and password == valid_credentials["password"]:
                is_logged_in = True
                st.success("Login successful!")
                input_container.empty()
                password_container.empty()
                button_container.empty()
                title_container.empty()
            else:
                st.error("Invalid credentials. Please try again.")

    return is_logged_in
