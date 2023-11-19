# meetings.py
import streamlit as st
import sqlite3
from datetime import datetime
from sqlite3 import IntegrityError  # Added import statement

def create_meetings_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_name TEXT NOT NULL,
            meeting_date DATE NOT NULL,
            user_id INT,
            last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_meeting(meeting_name, meeting_date, user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO meetings (meeting_name, meeting_date, user_id) VALUES (?, ?, ?)", (meeting_name, meeting_date, user_id))
        conn.commit()
        st.success(f"Meeting '{meeting_name}' added on '{meeting_date}'.")
    except IntegrityError:
        st.error("Error: Meeting date clashes with an existing meeting.")

    conn.close()

def view_meetings(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meetings WHERE user_id = ?", (user_id,))
    meetings = cursor.fetchall()

    conn.close()
    return meetings

def update_meeting_date(meeting_id, new_meeting_date):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE meetings SET meeting_date = ?, last_modified = CURRENT_TIMESTAMP WHERE id = ?", (new_meeting_date, meeting_id))

    conn.commit()
    conn.close()

def delete_meeting(meeting_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM meetings WHERE id = ?", (meeting_id,))

    conn.commit()
    conn.close()

def display_meetings_page():
    st.title("Meetings")

    # Create meetings table if not exists
    create_meetings_table()

    user_id = st.session_state.user_id

    # Add meeting form
    with st.form("add_meeting_form"):
        meeting_name = st.text_input("Meeting Name:")
        meeting_date = st.date_input("Meeting Date:", min_value=datetime.today())
        submit_button = st.form_submit_button("Add Meeting")

    if submit_button:
        # Add meeting to the database
        add_meeting(meeting_name, meeting_date, user_id)

    # View meetings
    meetings = view_meetings(user_id)
    if meetings:
        st.subheader("Your Meetings:")
        for meeting in meetings:
            st.write(f"Meeting: {meeting[1]}, Date: {meeting[2]}")
            
            # Update date form
            with st.form(key=f"update_meeting_{meeting[0]}"):
                new_meeting_date = st.date_input("New Meeting Date:", min_value=datetime.today())
                update_button = st.form_submit_button("Update Meeting Date")

            if update_button:
                # Update meeting date
                update_meeting_date(meeting[0], new_meeting_date)
                st.success(f"Date for '{meeting[1]}' updated to '{new_meeting_date}'.")
            
            # Delete meeting button
            delete_button_key = f"delete_meeting_{meeting[0]}"
            if st.button(f"Delete {meeting[1]}", key=delete_button_key):
                # Delete meeting
                delete_meeting(meeting[0])
                st.success(f"Meeting '{meeting[1]}' deleted.")

    else:
        st.info("No meetings found.")