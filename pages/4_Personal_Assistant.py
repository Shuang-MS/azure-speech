import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

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

# Hide the default headers and footers and maximize iframe space
st.markdown("""
<style>
    /* Hide all default UI elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Remove all margins, paddings, and scrollbars */
    html, body, [class*="css"] {
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* Make iframe container take full viewport height */
    .iframe-container {
        position: relative;
        width: 100vw;
        height: 100vh; /* Use full viewport height */
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    
    .responsive-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }
    
    /* Remove all padding and margins from Streamlit containers */
    .stApp {
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide the tiny header too */
    h3 {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        line-height: 0 !important;
        font-size: 0.7rem !important;
    }
    
    /* Target the specific div that wraps Streamlit content */
    .stApp > div:first-child {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] {
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

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