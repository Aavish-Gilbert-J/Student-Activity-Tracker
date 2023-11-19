# assignments.py
import streamlit as st
import sqlite3
from datetime import datetime

def create_assignments_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_name TEXT NOT NULL,
            deadline DATE NOT NULL,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create assignment_logs table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignment_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_description TEXT NOT NULL,
            event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create a trigger to log when a new assignment is added
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS after_insert_assignment
        AFTER INSERT ON assignments
        BEGIN
            INSERT INTO assignment_logs (event_type, event_description, event_timestamp)
            VALUES ('INSERT', 'New assignment added', CURRENT_TIMESTAMP);
        END;
    ''')

    conn.commit()
    conn.close()

def add_assignment(assignment_name, deadline, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO assignments (assignment_name, deadline, user_id) VALUES (?, ?, ?)", (assignment_name, deadline, user_id))

    conn.commit()
    conn.close()

def view_assignments(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assignments WHERE user_id = ?", (user_id,))
    assignments = cursor.fetchall()

    conn.close()
    return assignments

def update_assignment_deadline(assignment_id, new_deadline):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE assignments SET deadline = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_deadline, assignment_id))

    conn.commit()
    conn.close()

def delete_assignment(assignment_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))

    conn.commit()
    conn.close()

# def display_assignments_page():
#     st.title("Assignments")

#     # Create assignments table if not exists
#     create_assignments_table()

#     user_id = st.session_state.user_id

#     # Add assignment form
#     with st.form("add_assignment_form"):
#         assignment_name = st.text_input("Assignment Name:")
#         deadline = st.date_input("Deadline:", min_value=datetime.today())
#         submit_button = st.form_submit_button("Add Assignment")

#     if submit_button:
#         # Add assignment to the database
#         add_assignment(assignment_name, deadline, user_id)
#         st.success(f"Assignment '{assignment_name}' added with deadline '{deadline}'.")

#     # View assignments
#     assignments = view_assignments(user_id)
#     if assignments:
#         st.subheader("Your Assignments:")
#         for assignment in assignments:
#             st.write(f"Assignment: {assignment[1]}, Deadline: {assignment[2]}")
            
#             # Update deadline form
#             with st.form(key=f"update_assignment_{assignment[0]}"):
#                 new_deadline = st.date_input("New Deadline:", min_value=datetime.today())
#                 update_button = st.form_submit_button("Update Deadline")

#             if update_button:
#                 # Update assignment deadline
#                 update_assignment_deadline(assignment[0], new_deadline)
#                 st.success(f"Deadline for '{assignment[1]}' updated to '{new_deadline}'.")
            
#             # Delete assignment button
#             if st.button(f"Delete {assignment[1]}"):
#                 # Delete assignment
#                 delete_assignment(assignment[0])
#                 st.success(f"Assignment '{assignment[1]}' deleted.")

#     else:
#         st.info("No assignments found.")



def display_assignments_page():
    st.title("Assignments")

    # Create assignments table if not exists
    create_assignments_table()

    user_id = st.session_state.user_id

    # Add assignment form
    with st.form("add_assignment_form"):
        assignment_name = st.text_input("Assignment Name:")
        deadline = st.date_input("Deadline:", min_value=datetime.today())
        submit_button = st.form_submit_button("Add Assignment")

    if submit_button:
        # Add assignment to the database
        add_assignment(assignment_name, deadline, user_id)
        st.success(f"Assignment '{assignment_name}' added with deadline '{deadline}'.")

    # View assignments
    assignments = view_assignments(user_id)
    if assignments:
        st.subheader("Your Assignments:")
        for assignment in assignments:
            st.write(f"Assignment: {assignment[1]}, Deadline: {assignment[2]}")

            # Display last modification timestamp
            st.write(f"Last Modified: {assignment[4]}")

            # Update deadline form
            with st.form(key=f"update_assignment_{assignment[0]}"):
                new_deadline = st.date_input("New Deadline:", min_value=datetime.today())
                update_button = st.form_submit_button("Update Deadline")

            if update_button:
                # Update assignment deadline
                update_assignment_deadline(assignment[0], new_deadline)
                st.success(f"Deadline for '{assignment[1]}' updated to '{new_deadline}'.")
            
            # Delete assignment button
            if st.button(f"Delete {assignment[1]}"):
                # Delete assignment
                delete_assignment(assignment[0])
                st.success(f"Assignment '{assignment[1]}' deleted.")

    else:
        st.info("No assignments found.")
