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
        extract_tables = cursor.fetchall()
        table_names = []
        for tables in extract_tables:
            table_names.append(tables[0])

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

        custom_queries = [
            'Support Representative / Incident Tickets Insights',
            'Incidents per Month',
            'Number of Incidents Based on Priority',
            'Knowledge Base Insights'
            ]
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

        elif selected_queries == 'Support Representative / Incident Tickets Insights':
            headvalue = st.text_input("Enter the number of entries you would like to display")
            performer = st.selectbox("Top or Low Performers", ['Top', 'Low'])
            if st.button("Get Insights"):
                if performer == 'Top':
                    cursor.execute("SELECT SupportRepresentative.EmployeeID, FName AS 'First Name', LName AS 'Last Name', COUNT(IncidentID) AS 'Number of Incidents Worked On' FROM SupportRepresentative JOIN WorksOn ON SupportRepresentative.EmployeeID = WorksOn.EmployeeID GROUP BY SupportRepresentative.EmployeeID ORDER BY COUNT(IncidentID) DESC")
                elif performer == 'Low':
                    cursor.execute("SELECT SupportRepresentative.EmployeeID, FName AS 'First Name', LName AS 'Last Name', COUNT(IncidentID) AS 'Number of Incidents Worked On' FROM SupportRepresentative JOIN WorksOn ON SupportRepresentative.EmployeeID = WorksOn.EmployeeID GROUP BY SupportRepresentative.EmployeeID ORDER BY COUNT(IncidentID)")
                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]

                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df.head(int(headvalue)), hide_index=True,use_container_width=True)

                fig = px.bar(df.head(int(headvalue)), x='First Name', y='Number of Incidents Worked On', title='Support Representatives and Number of Incidents Worked On')
                fig.update_xaxes(title_text='Employees')
                fig.update_yaxes(title_text='Incidents worked on')
                st.plotly_chart(fig)

        elif selected_queries == 'Incidents per Month':
            priority = st.selectbox("Select the Priority", ['','Critical', 'High', 'Medium', 'Low'])

            if priority == '':
                cursor.execute("SELECT Priority, MONTH(CreationDate) AS Month, COUNT(*) AS IncidentCount FROM Incident GROUP BY Priority, Month ORDER BY Priority, Month")
                    
                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]

                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df.head(), hide_index=True,use_container_width=True)

                fig = px.bar(df, x='Month', y='IncidentCount', color='Priority',
                title='Incidents Vs Month',
                labels={'IncidentCount': 'Incident Count', 'Month': 'Month'},
                category_orders={'Priority': sorted(df['Priority'].unique())})

                for priority in df['Priority'].unique():
                    line_data = df[df['Priority'] == priority]
                    line_trace = px.line(line_data, x='Month', y='IncidentCount')
                    line_trace.update_traces(name=priority)
                    fig.add_trace(line_trace.data[0])

                fig.update_layout(barmode='stack', legend_title_text='Priority')
                st.plotly_chart(fig)
            
            elif priority == 'Critical':
                cursor.execute("SELECT MONTH(CreationDate) AS Month, COUNT(*) AS IncidentCount FROM Incident WHERE Priority = 'Critical' GROUP BY Month ORDER BY Month")

                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]

                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df, hide_index=True,use_container_width=True)

                fig = px.bar(df, x='Month', y='IncidentCount', labels={'IncidentCount': 'Number of Incidents'}, title='Critical Incidents by Month')
                fig.update_layout(xaxis_title='Month', yaxis_title='Number of Incidents')
                st.plotly_chart(fig)

            elif priority == 'High':
                cursor.execute("SELECT MONTH(CreationDate) AS Month, COUNT(*) AS IncidentCount FROM Incident WHERE Priority = 'High' GROUP BY Month ORDER BY Month")

                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]

                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df, hide_index=True,use_container_width=True)

                fig = px.bar(df, x='Month', y='IncidentCount', labels={'IncidentCount': 'Number of Incidents'}, title='High Priority Incidents by Month')
                fig.update_layout(xaxis_title='Month', yaxis_title='Number of Incidents')
                st.plotly_chart(fig)

            elif priority == 'Medium':
                cursor.execute("SELECT MONTH(CreationDate) AS Month, COUNT(*) AS IncidentCount FROM Incident WHERE Priority = 'Medium' GROUP BY Month ORDER BY Month")

                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]

                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df, hide_index=True,use_container_width=True)

                fig = px.bar(df, x='Month', y='IncidentCount', labels={'IncidentCount': 'Number of Incidents'}, title='Medium Priority Incidents by Month')
                fig.update_layout(xaxis_title='Month', yaxis_title='Number of Incidents')
                st.plotly_chart(fig)

            elif priority == 'Low':
                cursor.execute("SELECT MONTH(CreationDate) AS Month, COUNT(*) AS IncidentCount FROM Incident WHERE Priority = 'Low' GROUP BY Month ORDER BY Month")

                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]

                df = pd.DataFrame(table_data, columns=column_names)
                st.dataframe(df, hide_index=True,use_container_width=True)

                fig = px.bar(df, x='Month', y='IncidentCount', labels={'IncidentCount': 'Number of Incidents'}, title='Low Priority Incidents by Month')
                fig.update_layout(xaxis_title='Month', yaxis_title='Number of Incidents')
                st.plotly_chart(fig)

        if selected_queries == 'Knowledge Base Insights':
            number_of_rows = st.text_input("Number of Rows to Display")
            action = st.selectbox("Select Action", ["Top", "Bottom"])

            if st.button("Get Insights"):
                try:
                    number_of_rows = int(number_of_rows)
                except ValueError:
                    st.error("Number of rows should be a valid number")
            
                cursor.execute("SELECT kb.KB_ID,kb.IssueType,COUNT(inc.KnowledgeBaseID) AS IncidentCount FROM KnowledgeBase AS kb LEFT JOIN Incident AS inc ON kb.KB_ID = inc.KnowledgeBaseID GROUP BY kb.KB_ID, kb.IssueType ORDER BY kb.KB_ID")
                table_data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]
                df = pd.DataFrame(table_data, columns=column_names)

                if action == "Top":
                    st.dataframe(df.sort_values(by='IncidentCount', ascending=False).head(number_of_rows),hide_index=True, use_container_width=True)
                if action == "Bottom":
                    st.dataframe(df.sort_values(by='IncidentCount', ascending=True).head(number_of_rows),hide_index=True, use_container_width=True)

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
