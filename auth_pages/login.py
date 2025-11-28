import streamlit as st
from pymongo import MongoClient
import hashlib

def show_login(go_to):

    st.title("🔐 Login to CalmConnect")

    client = MongoClient("mongodb://localhost:27017/")
    db = client["calmconnect_db"]
    users = db["users"]

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    def hash_pass(p):
        return hashlib.sha256(p.encode()).hexdigest()

    if st.button("Login"):
        user = users.find_one({"username": username, "password": hash_pass(password)})
        if user:
            st.session_state.user = username
            st.success("Login successful!")
            go_to("main_app")
        else:
            st.error("Invalid username or password")

    st.write("---")
    if st.button("Go to Signup"):
        go_to("signup")
