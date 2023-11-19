# user_management.py
import streamlit as st
import sqlite3

def create_users_table():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(username, password, role):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))

    conn.commit()
    conn.close()

def view_users():
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()
    return users

def delete_user(user_id):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()

def display_user_management_page():
    st.title("Login/Signup")

    # Create users table if not exists
    create_users_table()

    # View users
    users = view_users()
    if users:
        st.subheader("Existing Users:")
        for user in users:
            st.write(f"Username: {user[1]}, Role: {user[3]}")
            
            # Delete user button
            if st.button(f"Delete {user[1]}"):
                # Delete user
                delete_user(user[0])
                st.success(f"User '{user[1]}' deleted.")

    else:
        st.info("No users found.")

    # Add user form
    st.subheader("Add New User:")
    with st.form("add_user_form"):
        new_username = st.text_input("Username:")
        new_password = st.text_input("Password:", type="password")
        new_role = st.selectbox("Role:", ["Student", "Teacher", "Internship Manager", "Admin"])
        add_user_button = st.form_submit_button("Add User")

    if add_user_button:
        # Add new user to the database
        add_user(new_username, new_password, new_role)
        st.success(f"User '{new_username}' added with role '{new_role}'.")



def update_user_role(user_id, new_role):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))

    conn.commit()
    conn.close()

from datetime import datetime

def authenticate_user(username, password):
    conn = sqlite3.connect("data/student_tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    conn.close()
    return user

def display_user_management_page():
    st.title("User Management")

    # Create users table if not exists
    create_users_table()

    # Add user form
    st.subheader("Add New User:")
    with st.form("add_user_form"):
        new_username = st.text_input("Username:")
        new_password = st.text_input("Password:", type="password")
        new_role = st.selectbox("Role:", ["Student", "Teacher", "Internship Manager", "Admin"])
        add_user_button = st.form_submit_button("Add User")

    if add_user_button:
        # Add new user to the database
        add_user(new_username, new_password, new_role)
        st.success(f"User '{new_username}' added with role '{new_role}'.")

    # Authentication form
    st.subheader("Authenticate User:")
    with st.form("auth_user_form"):
        auth_username = st.text_input("Username:")
        auth_password = st.text_input("Password:", type="password")
        auth_button = st.form_submit_button("Authenticate User")

    if auth_button:
        # Authenticate user
        authenticated_user = authenticate_user(auth_username, auth_password)
        # print(authenticated_user)
        try:
            if authenticated_user:
                st.session_state.user_id = authenticated_user[1]
                st.success(f"User '{auth_username}' authenticated with role '{authenticated_user[3]}'.")
            else:
                st.error("Authentication failed. Please check your username and password.")
        except TypeError:
            st.error("Authentication failed. Please check your username and password.")

# View users
    users = view_users()
    if users:
        st.subheader("Existing Users:")
        for user in users:
            st.write(f"Username: {user[1]}, Role: {user[3]}")
            
            # Update role form
            with st.form(key=f"update_user_{user[0]}"):
                new_role = st.selectbox("New Role:", ["Student", "Teacher", "Internship Manager", "Admin"])
                update_button = st.form_submit_button("Update User Role")

            if update_button:
                # Update user role
                update_user_role(user[0], new_role)
                st.success(f"Role for '{user[1]}' updated to '{new_role}'.")
            
            # Delete user button
            if st.button(f"Delete {user[1]}"):
                # Delete user
                delete_user(user[0])
                st.success(f"User '{user[1]}' deleted.")

    else:
        st.info("No users found.")