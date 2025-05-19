required_credentials = {
    "SPEECH": {
        "AZURE_SPEECH_KEY": {
            "label": "Azure Speech Service Key",
            "type": "password"
        },
        "AZURE_SPEECH_REGION": {
            "label": "Azure Speech Service Region",
        },
    },
    "AOAI": {
        "AZURE_OPENAI_API_KEY": {
            "label": "Azure OpenAI API Key",
            "type": "password"
        },
        "AZURE_OPENAI_API_ENDPOINT": {
            "label": "Azure OpenAI API Endpoint",
        },
        "AZURE_OPENAI_API_VERSION": {
            "label": "Azure OpenAI API Version",
        },
        "GPT4-1_DEPLOYMENT_NAME": {
            "label": "GPT-4.1 Deployment Name",
        },
        "GPT4-1_MINI_DEPLOYMENT_NAME": {
            "label": "GPT-4.1-mini Deployment Name",
        },
    },
    "TRANSLATOR": {
        "AZURE_TRANSLATOR_KEY": {
            "label": "Azure Translator Key",
            "type": "password"
        },
        "AZURE_TRANSLATOR_REGION": {
            "label": "Azure Translator Region",
        },
        "AZURE_DOC_TRANSLATOR_ENDPOINT": {
            "label": "Azure Document Translator Endpoint",
        }
    }
}

features = [ 
    { 
        "title": "🗣️ 语音翻译", 
        "description": "实时翻译语音内容，支持多语言互译",     
        "page": "pages/1_Speech_Translation.py",
        "key": "speech_translation"
     }, 
     { 
        "title": "📝 文本翻译", 
        "description": "快速翻译文本内容，支持多种语言", 
        "page": "pages/3_Text_Translation.py",
        "key": "text_translation"
    }, 
    {
        "title": "📆 会议摘要", 
        "description": "自动生成记录和摘要，快速了解要点", 
        "page": "pages/2_Meeting_Summary.py",
        "key": "meeting_summary"
    }, 
    {
        "title": "🤖 个人助手", 
        "description": "智能查询天气、新闻等信息", 
        "page": "pages/4_Personal_Assistant.py",
        "key": "personal_assistant"
    }
]

language_map = {
    "中文": "zh-CN",
    "英文": "en-US",
    "日文": "ja-JP",
    "韩文": "ko-KR",
    "德文": "de-DE",
    "法文": "fr-FR",
    "西班牙文": "es-ES"
}