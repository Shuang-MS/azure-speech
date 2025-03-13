import streamlit as st
import os
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from services import translation, llm_analysis
import time
from datetime import datetime
import requests

def translate_text_azure(text, target_lang, source_lang):
    result, latency = translation.azure_text_translate(text, target_lang, source_lang)
    if result.get("error"):
        st.error(result["error"])
        return None
    
    return f"{result['source_language']} -> {target_lang} | {latency:.2f}s: <br/>{result['translated_text'][0]}"

def translate_text_gpt(text, target_lang):
    result, latency = llm_analysis.text_translate(text, target_lang, None)
    if result.get("error"):
        st.error(result["error"])
        return None
    return f"{result['source_language']} -> {target_lang} | {latency:.2f}s: <br/>{result['translated_text']}"

def translate_document(file_bytes, filename, source_lang, target_lang):
    endpoint = os.getenv("AZURE_DOCUMENT_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_TRANSLATOR_KEY")
    
    client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
    # Implementation of document translation
    # This would require Azure Blob Storage setup for source and target containers
    # Return translation status or result

def _render_translation_result(container, result):
    if result:
        container.markdown(f"""
            <div style="padding: 0.5rem; border-radius: 8px; margin: 1rem 0; height: 200px; 
            overflow-y: auto; border: 1px solid #e2e8f0;">
                <p style="margin: 0; color: #FFFFFF; font-size: 1.1rem;">{result}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        container.markdown("""
            <div style="padding: 0.5rem; border-radius: 8px; margin: 1rem 0; height: 200px; 
            overflow-y: auto; border: 1px solid #e2e8f0;">
                <p style="margin: 0; color: #FFFFFF; font-size: 1.1rem;">No translation available</p>
            </div>
        """, unsafe_allow_html=True)

st.title("文本和文档翻译")

# Language selection
languages = {
    "中文": "zh",
    "英语": "en",
    "西班牙语": "es",
    "法语": "fr",
    "德语": "de",
    "日语": "ja"
}

tab1, tab2 = st.tabs(["文本翻译", "文档翻译"])

with tab1:
    st.subheader("文本翻译")
    
    source_lang = st.selectbox("源语言", list(languages.keys()) , key="source_text", index=0)
    target_lang = st.selectbox("目标语言", list(languages.keys()), key="target_text", index=1)
    
    input_text = st.text_area("请输入要翻译的文本:", height=150)
    
    # Add translation tool selection
    st.markdown("#### 选择翻译工具:")
    col1, col2 = st.columns(2)
    with col1:
        use_azure = st.checkbox("Azure翻译", value=True)
        with col1:
            azure_container = st.empty()
            azure_container.markdown(f"""
                <div style="padding: 0.5rem; border-radius: 8px; margin: 1rem 0;
                overflow-y: auto; border: 1px solid #e2e8f0; 
                opacity: {'1' if use_azure else '0.5'};">
                    <p style="margin: 0; color: #888888; 
                    font-size: 1.1rem;">{'选择"Azure翻译"后在此显示翻译结果' if not use_azure else 'Azure Translator'}</p>
                </div>
            """, unsafe_allow_html=True)
    with col2:
        use_llm = st.checkbox("LLM翻译", value=False)
        with col2:
            llm_container = st.empty()
            llm_container.markdown(f"""
                <div style="padding: 0.5rem; border-radius: 8px; margin: 1rem 0;
                overflow-y: auto; border: 1px solid #e2e8f0; 
                opacity: {'1' if use_llm else '0.5'};">
                    <p style="margin: 0; color: #888888; 
                    font-size: 1.1rem;">{'选择"LLM翻译"后在此显示翻译结果' if not use_llm else 'GPT-4o-mini'}</p>
                </div>
            """, unsafe_allow_html=True)
    
    if st.button("开始翻译"):
        if not input_text:
            st.warning("请输入要翻译的文本")
        elif not (use_azure or use_llm):
            st.warning("请至少选择一个翻译工具")
        else:
            # Now perform translations
            if use_azure:
                azure_translated = translate_text_azure(input_text, languages[target_lang], languages[source_lang])
                _render_translation_result(azure_container, azure_translated)
            
            if use_llm:
                llm_translated = translate_text_gpt(input_text, languages[target_lang])
                _render_translation_result(llm_container, llm_translated)

with tab2:
    st.header("文档翻译")
    
    source_lang = st.selectbox("源语言", list(languages.keys()), key="source_doc")
    target_lang = st.selectbox("目标语言", list(languages.keys()), key="target_doc")
    
    uploaded_file = st.file_uploader(
        "选择要翻译的文档", type=['txt', 'docx', 'pdf'])
    
    if uploaded_file is not None:
        if st.button("翻译文档"):
            try:
                file_bytes = uploaded_file.read()
                result = translate_document(file_bytes, uploaded_file.name, 
                                         languages[source_lang], 
                                         languages[target_lang])
                st.success("文档翻译已开始!")
            except Exception as e:
                st.error(f"翻译错误: {str(e)}")

