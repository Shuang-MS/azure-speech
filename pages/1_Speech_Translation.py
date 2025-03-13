import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
import io
import tempfile
import uuid
import time
from apis import speech_translation

st.set_page_config(page_title="语音翻译", page_icon="🎤", layout="centered")
st.title("🎤 语音翻译")

# Azure Speech service configuration (you should load these from environment variables or secure storage)
speech_key = os.environ.get('SPEECH_KEY', '')
speech_region = os.environ.get('SPEECH_REGION', '')
language_map = speech_translation.LANGUAGE_MAP
solution_funcs = {
    "Azure Speech Translation": {
        "translator": speech_translation.recognize_from_file,
        "tts": speech_translation.synthesize_text,
    },
    "GPT-4o-Audio": {
        "translator": None,
        "tts": None,
    },
    "ASR + LLM + TTS": {
        "translator": None,
        "tts": speech_translation.synthesize_text,
    }
}

if not speech_key or not speech_region:
    st.error("Please set the SPEECH_KEY and SPEECH_REGION environment variables")
    st.stop()

with st.container():
    col_left, col_right = st.columns([1, 1], gap="large")

with col_left:  
    st.markdown("#### 🎙 输入设置")  
    with st.container():  
        col_from, col_to = st.columns([1, 1])
        with col_from:
            speaker1_source = st.selectbox(  
                "我说：",  
                tuple(language_map.keys()) + ("Auto",),  
                index=0,  
                help="选择您的原始语言或让系统自动检测",
                key="speaker1_source" 
            )
            audio_value1 = None

        with col_to:
            speaker1_target = st.selectbox(  
                "我想听：",  
                tuple(language_map.keys()),  
                index=1,  
                help="选择您希望翻译成的目标语言"  
            )  
          
    with st.container():  
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)  
        options = list(solution_funcs.keys())
        selected_sol = st.radio(
            "⚙️ 方案选项",  
            options,  
            index=0,
            disabled=True  
        )
        st.markdown('</div>', unsafe_allow_html=True)  
          
    st.markdown("#### 🗣️ 语音输入")  
    audio_value1 = st.audio_input(  
        "点击麦克风开始录音",  
        key="audio1",  
        help="点击按钮开始录音，再次点击结束录音"  
    )

with col_right:  
    st.markdown("#### 🔄 处理结果")  
    if audio_value1:
        solution = solution_funcs[selected_sol]
        with st.status(f"**正在翻译...**", expanded=True) as status:  
            # Processing animation  
            st.markdown("""  
                <div style="display: flex; align-items: center; gap: 1rem;">  
                    <div class="spinner"></div>  
                </div>  
            """, unsafe_allow_html=True)  
              
            # Save and process audio  
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:  
                temp_audio.write(audio_value1.getvalue())  
                temp_path = temp_audio.name  
            
            st.write(f"Audio saved to {temp_path}")
              
            # Translation processing  
            source_language = language_map.get(speaker1_source, None)  
            target_language = language_map.get(speaker1_target)  
            recognized, translation, latency = solution['translator'](  
                temp_path, target_language, source_language  
            )  
              
            # Update status  
            status.update(  
                label="✅ 翻译完成，用时 {:.2f}s".format(latency),  
                state="complete",
                expanded=False
            )  
              
        # Results display  
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)  
          
        # Original text  
        st.markdown("##### 📝 语音转录")  
        st.markdown(f"""  
            <div style="  
                padding: 0.5rem;  
                background: #f8fafc;  
                border-radius: 8px;  
                margin: 1rem 0;  
            ">  
                <p style="margin: 0; color: #334155; font-size: 1.1rem;">  
                    {recognized or '未能识别到语音内容'}  
                </p>  
            </div>  
        """, unsafe_allow_html=True)  
          
        # Translation  
        st.markdown(f"##### 🌍 翻译：{speaker1_target}")  
        st.markdown(f"""  
            <div style="  
                padding: 0.5rem;  
                background: #f0fdf4;  
                border-radius: 8px;  
                margin: 1rem 0;  
            ">  
                <p style="margin: 0; color: #15803d; font-size: 1.1rem;">  
                    {translation or '翻译失败'}  
                </p>  
            </div>  
        """, unsafe_allow_html=True)
        if translation:
            with st.spinner("生成语音中..."):
                audio_bytes = solution['tts'](translation, target_language)
                if audio_bytes:
                    st.audio(audio_bytes)
        
        os.unlink(temp_audio.name)
        st.markdown('</div>', unsafe_allow_html=True)

