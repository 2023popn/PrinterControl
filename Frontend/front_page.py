"""
Bare Minimum Streamlit Frontend
This is the absolute simplest Streamlit setup that connects to a backend
"""

import streamlit as st
import requests
import base64

# ============= CONFIGURATION =============

API_URL = "http://localhost:8000"  # Your FastAPI backend URL

# ============= API CLIENT =============

def call_get_endpoint():
    """Call a GET endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/data")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def call_post_endpoint(text: str):
    """Call a POST endpoint"""
    try:
        response = requests.post(
            f"{API_URL}/api/data",
            json={"text": text}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def call_post_file_upload(file):
    """Call the file POST endpoint"""
    try:
        response = requests.post(
            f"{API_URL}/api/file",
            files={"file": file}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# ============= UI =============

st.title("Frontend → Backend Connection")

# Test GET request
st.header("Test GET Request")
if st.button("Fetch Data from Backend"):
    data = call_get_endpoint()
    if data:
        st.success("✅ Connected to backend!")
        st.json(data)

st.divider()

# Test POST request
st.header("Test POST Request")
user_input = st.text_input("Enter some text:")
if st.button("Send to Backend"):
    if user_input:
        result = call_post_endpoint(user_input)
        if result:
            st.success("✅ Data sent and received!")
            st.json(result)
    else:
        st.warning("Please enter some text")

st.divider()

# File uploader
st.header("File Uploader")
file = st.file_uploader("Upload a file")
if st.button("Send File to Backend"):
    if file:
        result = call_post_file_upload(file)
        if result:
            st.success("✅ Data sent and received!")
            st.json(result)
        else:
            st.warning("No file detected")
