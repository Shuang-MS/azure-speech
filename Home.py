import streamlit as st
from styles import load_css
from dotenv import load_dotenv
from utils import constants
import os
import shutil

# Page configuration
st.set_page_config(page_title="Azure AI", page_icon="🧠", layout="centered")
st.title("🧠 Azure AI")
st.markdown(load_css(), unsafe_allow_html=True)

def init_env_file():
    env_path = ".env"
    env_example_path = ".env.example"
    
    if not os.path.exists(env_path) and os.path.exists(env_example_path):
        shutil.copy2(env_example_path, env_path)
        st.info("Initialized .env file from .env.example")

# Initialize .env file if it doesn't exist
init_env_file()
load_dotenv(override=True)

# Add credentials section
with st.expander("🔑 Credentials Settings"):
    st.write("Please set your Azure credentials. Values will be saved to .env file.")
    
    # Create input fields for each credential
    updated_values = {}
    for key, config in constants.required_credentials.items():
        current_value = os.getenv(key, "")
        new_value = st.text_input(
            config["label"], 
            value=current_value, 
            key=f"input_{key}", 
            type=config.get("type", "default")
        )
        if new_value and new_value != current_value:
            updated_values[key] = new_value
    
    # Save button to update .env file
    if updated_values and st.button("Save Credentials"):
        env_path = ".env"
        
        # Read existing .env file line by line to preserve format
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                env_lines = f.readlines()
        else:
            env_lines = []

        # Update or append environment variables
        updated_lines = []
        updated_keys = set()
        
        # Process existing lines
        for line in env_lines:
            line = line.strip()
            if not line or line.startswith("#"):
                updated_lines.append(line)
                continue
                
            if "=" in line:
                key = line.split("=", 1)[0].strip()
                if key in updated_values:
                    # Preserve quotes if they exist in original
                    if '"' in line:
                        updated_lines.append(f'{key} = "{updated_values[key]}"')
                    else:
                        updated_lines.append(f'{key} = {updated_values[key]}')
                    updated_keys.add(key)
                else:
                    updated_lines.append(line)
        
        # Add new variables that weren't in the file
        for key, value in updated_values.items():
            if key not in updated_keys:
                updated_lines.append(f'{key} = "{value}"')
        
        # Write back to .env
        with open(env_path, "w") as f:
            f.write("\n".join(updated_lines))
            if updated_lines:
                f.write("\n")
        
        st.success("Credentials saved successfully!")

def render_feature_card(feature):
    if st.button(feature['title'], key=feature['key'], use_container_width=True):
        st.switch_page(feature['page'])
    st.caption(feature['description'], unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with st.container():
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    # Speech Translation
    col1, col2 = st.columns(2)
    with col1:
        render_feature_card(constants.features[0])
        
    # Text Translation
    with col2:
        render_feature_card(constants.features[1])
    
    col3, col4 = st.columns(2)
    with col3:
        render_feature_card(constants.features[2])
        
    # Other Features
    with col4:
        render_feature_card(constants.features[3])
    
    st.markdown('</div>', unsafe_allow_html=True)
