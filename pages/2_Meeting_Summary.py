import streamlit as st
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import time
from apis import speech_fast_transcription, meeting_llm_analysis

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

# 设置页面配置
st.set_page_config(page_title="会议录转摘", page_icon="🗓️", layout="centered")
st.title("🗓️ 会议录转摘")

# 上传文件，添加图标
audio_file = st.file_uploader("🎤 上传音频文件", type=["wav", "mp3", "m4a"])
image_file = st.file_uploader("🖼️ 上传图像文件", type=["jpg", "jpeg", "png"])

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
            image_result = meeting_llm_analysis.analysis_image(image_file)
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
            summary = meeting_llm_analysis.analysis_text(user_prompt,summary_prompt)
            elapsed_summary = time.time() - start
            st.sidebar.success(f"会议总结完成，耗时 {elapsed_summary:.2f} 秒")
        
            st.subheader("📝 会议纪要")
            with st.expander("点击查看会议纪要"):
                st.markdown(summary)

