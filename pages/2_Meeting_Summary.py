import streamlit as st
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import time
from services import speech_fast_transcription, llm_analysis, aoai_audio
from styles import get_file_uploader_style

@st.fragment
def download_transcription():
    st.download_button(
        label="下载音频转录",
        icon="📥",
        data=transcription.encode('utf-8'),
        file_name=f"transcription_{time.strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        key="download_transcription"
    )

transcription_tools = {
    "fast_transcription": {
        "name": "Azure Speech Fast Transcription",
        "function": speech_fast_transcription.fast_transcript,
        "limit": {
            "file_size": 200,  # 200 MB
            "duration": "2 hours",  # 2 hours
        }
    },
    "gpt4o_transcribe": {
        "name": "GPT-4o-transcribe",
        "function": aoai_audio.transcribe,
        "limit": {
            "file_size": 25,  # 25 MB
            "duration": "10 min",  # Officially anounced 1500s, but with bug
        }
    }
}

# 设置页面配置
st.set_page_config(page_title="会议录转摘", page_icon="🗓️", layout="centered")
st.title("🗓️ 会议录转摘")
st.markdown(get_file_uploader_style(), unsafe_allow_html=True)

tool_names = [tool["name"] for tool in transcription_tools.values()]
tool_keys = list(transcription_tools.keys())
selected_tool_name = st.radio(
    "选择音频转录工具",
    tool_names,
    index=0,
    horizontal=True
)
transcription_tool = tool_keys[tool_names.index(selected_tool_name)]

audio_limit = transcription_tools[transcription_tool]["limit"]
audio_limit_msg = f"Audio file size limit: {audio_limit['file_size']} MB, audio length limit: {audio_limit['duration']}"
audio_file = st.file_uploader("🎤 上传音频文件", type=["wav", "mp3", "m4a"])
st.caption(audio_limit_msg)

if audio_file is not None:
    file_size_bytes = audio_file.size
    file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB
    if file_size_mb > audio_limit["file_size"]:
        st.error(f"文件大小超过限制：{audio_limit['file_size']} MB")
        audio_file = None

image_limit = 20
image_limit_msg = f"Image size limit: {image_limit} MB"
image_file = st.file_uploader("🖼️ 上传图像文件", type=["jpg", "jpeg", "png"])
st.caption(image_limit_msg)

if image_file is not None:
    file_size_bytes = image_file.size
    file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB
    if file_size_mb > image_limit:
        st.error(f"文件大小超过限制：{image_limit} MB")
        image_file = None

user_prompt = st.text_input("📝 输入提示词，用于会议总结 (Optional)")

if st.button("🚀 处理") and (audio_file or image_file):
    transcription = None
    image_result = None
    has_next = True
    with st.spinner("处理中，请稍候..."):
        # 转录音频
        
        if audio_file:
            start = time.time()
            result = speech_fast_transcription.fast_transcript(audio_file)
            elapsed_audio = time.time() - start

            if result:
                transcription = result
                st.sidebar.success(f"音频转录完成，耗时 {elapsed_audio:.2f} 秒")
                st.subheader("🎤 音频转录")
                download_transcription()
            else:
                transcription = None
                st.sidebar.error("转录失败。请检查音频文件格式或质量。")
                has_next = False

        # 分析图像内容
        if image_file:
            start = time.time()
            image_result = llm_analysis.analysis_image(image_file)
            elapsed_image = time.time() - start
            
            if image_result:
                st.sidebar.success(f"图像分析完成，耗时 {elapsed_image:.2f} 秒")
            else:
                image_result = None
                st.sidebar.error("图像分析失败。请检查图像文件格式或质量。")
                has_next = False
        
        if has_next:
            # 总结内容
            summary_prompt = f"""
            音频转录：{transcription}
            图像分析：{image_result}

            请提供一份侧重于会议内容和待办事项的总结。
            """

            start = time.time()
            summary = llm_analysis.analysis_text(user_prompt,summary_prompt)
            elapsed_summary = time.time() - start
            st.sidebar.success(f"会议总结完成，耗时 {elapsed_summary:.2f} 秒")
        
            st.subheader("📝 会议纪要")
            with st.expander("点击查看会议纪要"):
                st.markdown(summary)

