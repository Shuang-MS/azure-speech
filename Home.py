import streamlit as st
from styles import load_css

# Page configuration
st.set_page_config(page_title="Azure 语音助手", page_icon="🎧", layout="wide")

# Import CSS from styles.py
st.markdown(load_css(), unsafe_allow_html=True)

# App title
st.markdown("<h1 class='centered-title'>🎧 Azure 语音助手</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with st.container():
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    
    # Speech Translation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 语音翻译", key="speech_trans", use_container_width=True):
            st.switch_page("pages/speech_translation.py")
        st.markdown("<p class='description'>实时翻译语音内容，支持多种语言</p>", unsafe_allow_html=True)
        
    # Text Translation
    with col2:
        if st.button("📝 文本翻译", key="text_trans", use_container_width=True):
            st.switch_page("pages/text_translation.py")
        st.markdown("<p class='description'>快速翻译文本，支持多种语言格式</p>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🗓️ 会议摘要", key="meeting_summary", use_container_width=True):
            st.switch_page("pages/2_Meeting_Summary.py")
        st.markdown("<p class='description'>转录会议，生成会议纪要</p>", unsafe_allow_html=True)
        
    # Other Features
    with col4:
        if st.button("🔍 智能查询", key="voice_assistant", use_container_width=True):
            st.switch_page("pages/voice_assistant.py")
        st.markdown("<p class='description'>提供天气、新闻等多种信息查询服务</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)