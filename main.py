import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, auth

# Global variable to keep track of Firebase app initialization
default_app_initialized = False

def initialize_firebase():
    global default_app_initialized
    if not default_app_initialized:
        # Initialize Firebase only if it's not already initialized
        cred = credentials.Certificate(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
        default_app_initialized = True

initialize_firebase()

def create_user(email, password):
    return auth.create_user(email=email, password=password)


def add_single_user(email, password):
    try:
        user = create_user(email, password)
        return f"{email.split('@')[0]} created successfully!"
    except Exception as e:
        st.error(f"Error: {e} for {email.split('@')[0]}")
        return f"Error: {e} for {email.split('@')[0]}"

def bulk_upload_users(file):
    try:
        df = pd.read_excel(file)
        if 'username' not in df.columns or 'password' not in df.columns:
            return "Excel file must contain 'email' and 'password' columns."
        
        results = []
        for _, row in df.iterrows():
            email = row['username']
            password = row['password']
            # Replace username with email and append '@istudent.ly'
            username = email.split('@')[0] + '@istudent.ly'
            result = add_single_user(username, password)
            results.append(f"{username.split('@')[0]} created successfully!")
            # Show success message after each user is created
            st.success(f"{username.split('@')[0]} created successfully!")
        
        # Return a summary of the results
        return "\n".join(results)
    except Exception as e:
        st.error(f"Error: {e}")
        return f"Error: {e}"

st.title("User Management for arabic.istudent.ly")

option = st.selectbox("Choose an option", ["Add Single User", "Bulk Upload Users"])

if option == "Add Single User":
    st.header("Add a Single User")
    email = st.text_input("Username")
    password = st.text_input("Password")
    
    if st.button("Add User"):
        if email and password:
            # Replace username with email and append '@istudent.ly'
            username = email.split('@')[0] + '@istudent.ly'
            result = add_single_user(username, password)
            st.success(f"{email.split('@')[0]} created successfully!")
        else:
            st.error("Please enter both username and password.")
    
elif option == "Bulk Upload Users":
    st.header("Bulk Upload Users from Excel")
    uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")
    
    if uploaded_file:
        result = bulk_upload_users(uploaded_file)
