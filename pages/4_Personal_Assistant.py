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

st.set_page_config(page_title="个人助手", page_icon="🤖" layout="centered")
st.title("🤖 个人助手")

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

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)