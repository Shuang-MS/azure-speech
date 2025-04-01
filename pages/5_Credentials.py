# core.py
import streamlit as st
import sys
import os
import io
import time
import json
from dotenv import dotenv_values
from urllib.parse import urlparse, parse_qs
import uuid


# Add parent directory to path to import styles module
sys.path.append(os.path.dirname(__file__))
from styles import get_credential_page_style
from utils.constants import required_credentials

# --- Security UI Enhancements ---
st.markdown(get_credential_page_style(), unsafe_allow_html=True)

# --- Initialize Session State ---
if 'creds' not in st.session_state:
    # Initialize with credential categories from constants
    st.session_state.creds = {
        category: {cred: "" for cred in creds} for category, creds in required_credentials.items()
    }

# --- Main Page Layout ---
st.title("🔐 Credential Manager")

# --- Import/Export Controls ---
import_col, export_col = st.columns(2)

# Generate a unique session ID if not already present
if 'unique_session_id' not in st.session_state:
    st.session_state.unique_session_id = int(time.time())

# --- Load credentials from URL parameters ---
params = st.query_params
if "creds" in params:
    try:
        # Decode the JSON from URL parameters
        loaded_creds = json.loads(params["creds"])
        # Update the session state
        for category in required_credentials.keys():
            if category in loaded_creds:
                st.session_state.creds[category].update(loaded_creds[category])
        st.success("Credentials loaded successfully!")
    except Exception as e:
        st.error(f"Error loading credentials: {str(e)}")

# --- Import/Export Controls ---
with import_col:
    # Import Controls
    st.caption("📥 Import Credentials from .env file")
    uploaded_file = st.file_uploader(
        "Import Credentials",
        type=["env"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        config = dotenv_values(stream=io.StringIO(content))
        
        # Organize imported credentials by category
        imported_creds = {category: {} for category in required_credentials.keys()}
        
        for key, value in config.items():
            # Find which category this credential belongs to
            for category, creds in required_credentials.items():
                if key in creds:
                    imported_creds[category][key] = value
                    break
        
        # Update session state
        for category, creds in imported_creds.items():
            st.session_state.creds[category].update(creds)
            
        st.success("Credentials imported successfully!")

def _json_to_env(json_content):
    content = []
    for category, creds in json_content.items():
        for key, value in creds.items():
            if value:  # Only include non-empty values
                content.append(f"{key}={value}")
    return "\n".join(content)

with export_col:
    st.caption("📤 Export Credentials")
    export_data = _json_to_env(st.session_state.creds)
    st.download_button(
        label="Download",
        data=export_data,
        file_name=f"credentials_{int(time.time())}.env",
        mime="text/plain",
        use_container_width=True
    )

# Create tab objects for each credential category
tab_objects = st.tabs([f"{cat.title()}" for cat in required_credentials.keys()])

# Fill in credential tabs with form fields
for i, (category, creds) in enumerate(required_credentials.items()):
    with tab_objects[i]:
        # Use unique form key by including category
        with st.form(f"{category}_form_{i}"):
            st.subheader(f"{category.title()} Credentials")
            for j, (cred_key, cred_info) in enumerate(creds.items()):
                input_type = cred_info.get("type", "default")
                label = cred_info.get("label", cred_key)
                
                # Use truly unique key for each input
                unique_key = f"{category}_{cred_key}_{i}_{j}"
                
                # Store input value directly in session state
                current_value = st.session_state.creds[category].get(cred_key, "")
                input_value = st.text_input(
                    label, 
                    value=current_value,
                    type=input_type,
                    key=unique_key
                )
                # Update the session state after input
                st.session_state.creds[category][cred_key] = input_value
                
            submitted = st.form_submit_button("Save")
            if submitted:
                st.success(f"{category.title()} credentials saved!")