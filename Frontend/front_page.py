import streamlit

"Hello World"
"""
Bare Minimum Streamlit Frontend
This is the absolute simplest Streamlit setup that connects to a backend
"""

import streamlit as st
import requests
import base64
import json
from pandas import DataFrame

# ============= CONFIGURATION =============

API_URL = "http://localhost:8000"  # Your FastAPI backend URL

# ============= API CLIENT =============

# ====== Test Endpoints ======

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

# ====== Printer Endpoints ======

def call_get_full_queue_endpoint():
    """Call next file endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/queue")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

def call_print_next_file_endpoint():
    """Call print file endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/print")
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

st.title("3D Printer Manager")

# Add new printer section
st.header("Add New Printer")

col1, col2, col3 = st.columns(3)

with col1:
    port = st.text_input("Port", value="/dev/ttyUSB0")

with col2:
    baud = st.number_input("Baud Rate", value=115200, step=1000)

with col3:
    printer_name = st.text_input("Printer Name (optional)")

if st.button("Add Printer"):
    response = requests.post(
        f"{API_URL}/printers/add",
        json={
            "port": port,
            "baud": baud,
            "name": printer_name if printer_name else None
        }
    )

    if response.status_code == 200:
        data = response.json()
        st.success(f"✅ Added {data['printer_name']} (ID: {data['printer_id']})")
    else:
        st.error(f"❌ Failed to add printer: {response.text}")

# Display printers
st.header("Connected Printers")

# Refresh button
if st.button("Refresh"):
    st.rerun()

# Get list of printers
response = requests.get(f"{API_URL}/printers")

if response.status_code == 200:
    data = response.json()

    if data["total"] == 0:
        st.info("No printers configured yet.")
    else:
        for printer in data["printers"]:
            with st.expander(f"🖨️ {printer['name']} (ID: {printer['id']})"):
                st.write(f"**Port:** {printer['port']}")
                st.write(f"**Online:** {'✅ Yes' if printer['printer_online'] else '❌ No'}")
                st.write(f"**Printing:** {'✅ Yes' if printer['is_printing'] else '❌ No'}")
                st.write(f"**Queue Length:** {printer['queue_length']}")

                # Add file to queue
                filepath = st.text_input(f"File path", key=f"file_{printer['id']}")
                if st.button(f"Add to Queue", key=f"add_{printer['id']}"):
                    add_response = requests.post(
                        f"{API_URL}/printers/{printer['id']}/queue/add",
                        params={"filepath": filepath}
                    )
                    if add_response.status_code == 200:
                        st.success("Added to queue!")
                        st.rerun()
                    else:
                        st.error(f"Error: {add_response.text}")

                # Remove printer
                if st.button(f"Remove Printer", key=f"remove_{printer['id']}"):
                    delete_response = requests.delete(
                        f"{API_URL}/printers/{printer['id']}"
                    )
                    if delete_response.status_code == 200:
                        st.success("Printer removed!")
                        st.rerun()