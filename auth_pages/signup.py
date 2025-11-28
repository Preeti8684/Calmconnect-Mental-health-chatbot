import streamlit as st
from pymongo import MongoClient
import hashlib

def show_signup(go_to):

    st.title("📝 Create Account")

    client = MongoClient("mongodb://localhost:27017/")
    db = client["calmconnect_db"]
    users = db["users"]

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    cpassword = st.text_input("Confirm Password", type="password")

    def hash_pass(p):
        return hashlib.sha256(p.encode()).hexdigest()

    if st.button("Signup"):

        if not username or not password:
            st.warning("All fields are required")
        elif password != cpassword:
            st.error("Passwords do not match")
        elif users.find_one({"username": username}):
            st.error("Username already exists")
        else:
            users.insert_one({"username": username,
                              "password": hash_pass(password)})

            st.success("Signup successful! Please login.")
            go_to("login")

    st.write("---")
    if st.button("Go to Login"):
        go_to("login")
