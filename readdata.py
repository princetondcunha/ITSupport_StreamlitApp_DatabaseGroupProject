'''Read Data from MySQL Database'''

import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from mysql_conn import mysqlconnect

def read():
    '''Read Table Data'''
    st.title("Q-wizer")

    try:
        connection = mysqlconnect()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        table_names = [table[0].decode('utf-8') for table in cursor.fetchall()]

        selected_table = st.selectbox("Select a table", table_names)

        if selected_table:
            cursor.execute(f"SELECT * FROM {selected_table}")
            table_data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]  # Get column names from cursor

            # Create DataFrame with column names
            df = pd.DataFrame(table_data, columns=column_names)

            # Display the current data
            st.dataframe(df, hide_index=True,use_container_width=True)

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

def readcustom():
    '''Read Table Data using Pre-Defined Queries'''
    st.title("Q-wizer")
    st.header("Insights")

    try:
        connection = mysqlconnect()
        cursor = connection.cursor()

        custom_queries = ['Support Representative who has worked on Most Incident Tickets', 'Support Representative who has worked on Least Incident Tickets','Customers with Most Issues','Customers with Least Issues','Number of Incidents Based on Priority']
        selected_queries  = st.selectbox("What insight do you want to find?", custom_queries)

        if selected_queries == 'Number of Incidents Based on Priority':
            cursor.execute("SELECT Priority, COUNT(IncidentID) AS Count FROM Incident GROUP BY Priority ORDER BY Priority")
            table_data = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]  # Get column names from cursor

            # Create DataFrame with column names
            df = pd.DataFrame(table_data, columns=column_names)

            # Display the current data
            st.dataframe(df, hide_index=True,use_container_width=True)

            fig = px.bar(df, x='Priority', y='Count', title='Number of Incidents Based on Priority', labels={'Count': 'Number of Incidents'})
            
            custom_order = ['Critical', 'High', 'Medium', 'Low']
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': custom_order})

            st.plotly_chart(fig)

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
