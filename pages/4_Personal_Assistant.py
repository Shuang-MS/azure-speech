import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
import sys

# Add parent directory to path to import styles
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_iframe_fullscreen_style

# Load environment variables
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")
gpt4o_deployment = os.getenv("GPT4o_DEPLOYMENT_NAME")
gpt4o_mini_deployment = os.getenv("GPT4o_MINI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Use wide layout for more space and disable initial sidebar
st.set_page_config(page_title="个人助手", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# Set Azure OpenAI API configuration from environment variables
client = AzureOpenAI(
    azure_endpoint = api_endpoint, 
    api_key=api_key,  
    api_version=api_version
)

# Set a default deployment name
if "deployment_name" not in st.session_state:
    st.session_state["deployment_name"] = gpt4o_deployment

if "messages" not in st.session_state:
    st.session_state.messages = []

# Import and apply the fullscreen iframe style
st.markdown(f"<style>{get_iframe_fullscreen_style()}</style>", unsafe_allow_html=True)

# Minimal header (almost invisible)
st.markdown("<h3><a href='https://playground.azuretsp.com/' target='_blank'>Azure TSP Playground</a></h3>", unsafe_allow_html=True)

# Embed the Azure TSP Playground using all available space
st.markdown("""
<div class="iframe-container">
    <iframe class="responsive-iframe" src="https://playground.azuretsp.com/" allow="microphone; camera" frameborder="0"></iframe>
</div>
""", unsafe_allow_html=True)

# Comment out all the chat functionality for now
# Display chat messages from history (keeping this commented until needed)
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# Accept user input code remains commented as in your current version