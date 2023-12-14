'''IT Querywizer'''

import streamlit as st
from readdata import read, readcustom
from writedata import insert
from resolveticket import resolveticket
from resolveticket import login_page



def main():
    '''Main'''
    st.sidebar.title("Navigation")
    pages = ["View Database", "Create an Issue","Resolve Ticket" ,"Insights"]
    choice = st.sidebar.radio("Go to", pages)

    if choice == "View Database":
        read()
    elif choice == "Create an Issue":
        insert()
    elif choice == "Resolve Ticket":
        if login_page():
            resolveticket()
    elif choice == "Insights":
        readcustom()

if __name__ == "__main__":
    main()
