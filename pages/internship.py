# internship.py
import streamlit as st
import sqlite3
from datetime import datetime

def create_internship_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internship (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            project_id INT,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_internship(company_name, start_date, end_date, project_id, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO internship (company_name, start_date, end_date, project_id, user_id) VALUES (?, ?, ?, ?, ?)", (company_name, start_date, end_date, project_id, user_id))

    conn.commit()
    conn.close()

def view_internships(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT internship.id, internship.company_name, internship.start_date, internship.end_date, projects.project_name, projects.description
        FROM internship
        LEFT JOIN projects ON internship.project_id = projects.project_name
        WHERE internship.user_id = ?
    """, (user_id,))
    
    internships = cursor.fetchall()
    # print(internships)

    conn.close()
    return internships


def update_internship_dates(internship_id, new_start_date, new_end_date):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE internship SET start_date = ?, end_date = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_start_date, new_end_date, internship_id))

    conn.commit()
    conn.close()

def delete_internship(internship_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM internship WHERE id = ?", (internship_id,))

    conn.commit()
    conn.close()

def display_internship_page():
    st.title("Internship")

    # Create internship table if not exists
    create_internship_table()

    user_id = st.session_state.user_id
    
    # Add internship form
    with st.form("add_internship_form"):
        company_name = st.text_input("Company Name:")
        start_date = st.date_input("Start Date:", min_value=datetime.today())
        end_date = st.date_input("End Date:", min_value=datetime.today())
        project_id = st.text_input("Project ID (if any):")
        submit_button = st.form_submit_button("Add Internship")

    if submit_button:
        # Add internship to the database
        add_internship(company_name, start_date, end_date, project_id, user_id)
        st.success(f"Internship at '{company_name}' added from '{start_date}' to '{end_date}'.")
        

    # View internships
    internships = view_internships(user_id)
    if internships:
        st.subheader("Your Internships:")
        for internship in internships:
            # print(internship)
            st.write(f"Company: {internship[1]}, Start Date: {internship[2]}, End Date: {internship[3]}, Project: {internship[4]}, Description: {internship[5]}")
            
            # Update dates form
            with st.form(key=f"update_internship_{internship[0]}"):
                new_start_date = st.date_input("New Start Date:", min_value=datetime.today())
                new_end_date = st.date_input("New End Date:", min_value=datetime.today())
                update_button = st.form_submit_button("Update Dates")

            if update_button:
                # Update internship dates
                update_internship_dates(internship[0], new_start_date, new_end_date)
                st.success(f"Dates for '{internship[1]}' updated to '{new_start_date}' - '{new_end_date}'.")
            
            # Delete internship button
            if st.button(f"Delete {internship[1]}", key=f"delete_internship_{internship[0]}"):
                # Delete internship
                delete_internship(internship[0])
                st.success(f"Internship at '{internship[1]}' deleted.")


    else:
        st.info("No internships found.")
