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

# Add credentials reminder
if "profile" in st.session_state and st.session_state.profile:
    st.success("已配置Azure凭据!", icon="✅")
else:
    st.info("请先配置Azure凭据", icon="ℹ️")

# Credentials shortcut button
if st.button("🔑 配置凭据", use_container_width=True):
    st.switch_page("pages/5_Credentials.py")

st.markdown("---")

def render_feature_card(feature, disabled=False):
    if st.button(feature['title'], key=feature['key'], use_container_width=True, disabled=disabled):
        st.switch_page(feature['page'])
    st.caption(feature['description'], unsafe_allow_html=True)

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
