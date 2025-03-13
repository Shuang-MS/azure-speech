import streamlit as st
import os
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
import time
from datetime import datetime
import requests

def translate_text_azure(text, target_lang, source_lang='auto-detect'):
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    try:
        response = client.translate(content=[text], to=[target_lang], from_parameter=source_lang)
        return response[0].translations[0].text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None

def translate_text_gpt4(text, target_lang):
    # Replace with your GPT-4 mini API endpoint and implementation
    # This is a placeholder
    return f"GPT-4 translation to {target_lang}: {text}"

def translate_document(file_bytes, filename, source_lang, target_lang):
    endpoint = os.getenv("AZURE_DOCUMENT_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_TRANSLATOR_KEY")
    
    client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
    # Implementation of document translation
    # This would require Azure Blob Storage setup for source and target containers
    # Return translation status or result

st.title("Text and Document Translation")

# Language selection
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja"
}

# Create two tabs for text and document translation
tab1, tab2 = st.tabs(["Text Translation", "Document Translation"])

with tab1:
    st.header("Text Translation")
    
    source_lang = st.selectbox("Source Language", list(languages.keys()), key="source_text")
    target_lang = st.selectbox("Target Language", list(languages.keys()), key="target_text")
    
    input_text = st.text_area("Enter text to translate:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Translate with Azure"):
            if input_text:
                translated = translate_text_azure(input_text, languages[target_lang], languages[source_lang])
                if translated:
                    st.success("Translation complete!")
                    st.write(translated)
    
    with col2:
        if st.button("Translate with GPT-4"):
            if input_text:
                translated = translate_text_gpt4(input_text, languages[target_lang])
                if translated:
                    st.success("Translation complete!")
                    st.write(translated)

with tab2:
    st.header("Document Translation")
    
    source_lang = st.selectbox("Source Language", list(languages.keys()), key="source_doc")
    target_lang = st.selectbox("Target Language", list(languages.keys()), key="target_doc")
    
    uploaded_file = st.file_uploader("Choose a document to translate", 
                                   type=['txt', 'docx', 'pdf'])
    
    if uploaded_file is not None:
        if st.button("Translate Document"):
            try:
                # Handle document translation
                file_bytes = uploaded_file.read()
                result = translate_document(file_bytes, uploaded_file.name, 
                                         languages[source_lang], 
                                         languages[target_lang])
                st.success("Document translation initiated!")
                # Add progress tracking and download link for translated document
            except Exception as e:
                st.error(f"Error translating document: {str(e)}")
