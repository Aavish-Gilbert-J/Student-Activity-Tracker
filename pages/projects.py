# projects.py
import streamlit as st
import sqlite3
from datetime import datetime

def create_projects_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            project_name TEXT NOT NULL primary key,
            description TEXT NOT NULL,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(project_name)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_project(project_name, description, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO projects (project_name, description, user_id) VALUES (?, ?, ?)", (project_name, description, user_id))

    conn.commit()
    conn.close()

def view_projects(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects WHERE user_id = ?", (user_id,))
    projects = cursor.fetchall()
    # print(projects)

    conn.close()
    return projects

def update_project_deadline(project_id, new_deadline):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE projects SET description = ?, last_modified = CURRENT_TIMESTAMP WHERE project_name = ?", (new_deadline, project_id))

    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM projects WHERE project_name = ?", (project_id,))

    conn.commit()
    conn.close()

def display_projects_page():

    st.title("Projects")

    # Create projects table if not exists
    create_projects_table()

    user_id = st.session_state.user_id

    # Add project form
    with st.form("add_project_form"):
        project_name = st.text_input("Project Name:")
        deadline = st.text_input("Description:")
        submit_button = st.form_submit_button("Add Project")

    if submit_button:
        # Add project to the database
        add_project(project_name, deadline, user_id)
        st.success(f"Project '{project_name}' added.")

    # View projects
    projects = view_projects(user_id)
    if projects:
        st.subheader("Your Projects:")
        for project in projects:
            st.write(f"Project: {project[1]}, Description: {project[1]}")
            
            # Update deadline form
            with st.form(key=f"update_project_{project[0]}"):
                new_deadline = st.text_input("New Description:")
                update_button = st.form_submit_button("Update Project Description")

            if update_button:
                # Update project deadline
                update_project_deadline(project[0], new_deadline)
                st.success(f"Deadline for '{project[1]}' updated to '{new_deadline}'.")
            
            # Delete project button
            if st.button(f"Delete {project[1]}"):
                # Delete project
                delete_project(project[0])
                st.success(f"Project '{project[1]}' deleted.")

    else:
        st.info("No projects found.")
