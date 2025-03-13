from openai import AzureOpenAI
from dotenv import load_dotenv
import base64
import os
import json
import time

load_dotenv()
GPT4o_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
GPT4o_DEPLOYMENT_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
GPT4o_DEPLOYMENT_NAME = os.getenv("GPT4o_DEPLOYMENT_NAME")
GPT4o_MINI_DEPLOYMENT_NAME = os.getenv("GPT4o_MINI_DEPLOYMENT_NAME")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
  azure_endpoint = GPT4o_DEPLOYMENT_ENDPOINT, 
  api_key=GPT4o_API_KEY,  
  api_version=API_VERSION
)

def call_openAI(text, model=GPT4o_DEPLOYMENT_NAME):
    print(f"deploy is {model}")
    response = client.chat.completions.create(
        model=model,
        messages = text,
        temperature=0.0
    )
    return response.choices[0].message.content

def encode_image(image):
    
    return base64.b64encode(image).decode("utf-8")
    
def analysis_image(image):
    
    question = "Please provide a detailed explanation of the image."
    encoded_image = encode_image(image.getvalue())
    messages=[
        {"role": "system", "content": "You are a helpful assistant that responds in image. Help me with my meeting recording image!"},
        {"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{encoded_image}"}
            }
        ]}
    ]
    result = call_openAI(messages)
    
    print(f"Image analysis result: {result}")
    return result

def analysis_text(userPrompt,text):
    question = "请提供一份侧重于会议内容和待办事项的总结. 使用良好的中文格式输出"
    messages=[
        {"role": "system", "content": "You are a helpful assistant that responds in text. Help me with my meeting recording text!"},
        {"role": "user", "content": [
            {"type": "text", "text": question + userPrompt},
            {"type": "text", "text": text}
        ]}
    ]
    result = call_openAI(messages)
    
    print(f"Text analysis result: {result}")
    return result

def text_translate(text, target_lang, source_lang):
    if source_lang:
        question = """Input text: `{text}`
        Target language: {target_lang}
        Source language: {source_lang}"""
    else:
        question = """Input text: `{text}`
        Target language: {target_lang}"""
    
    messages=[
        {"role": "system", "content": "You are a professional multilingual translator. Translate the text into the target language. Identify the source language if not provided. Output in strict JSON format including **source_language** and **translated_text**."},
        {"role": "user", "content": [
            {"type": "text", "text": question.format(
                text=text,
                target_lang=target_lang,
                source_lang=source_lang
            )},
        ]}
    ]
    try:
        start = time.time()
        response = client.chat.completions.create(
            model=GPT4o_MINI_DEPLOYMENT_NAME,
            messages = messages,
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        output = response.choices[0].message.content
        output = json.loads(output)
        elapsed_time = time.time() - start
        return {
            "translated_text": output.get("translated_text"),
            "source_language": output.get("source_language")
        }, elapsed_time
    except json.JSONDecodeError as e:
        return {
            "error": f"{output}\n{e}"
        }, 0
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return {
            "error": f"Translation error: {e}"
        }, 0