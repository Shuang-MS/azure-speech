from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import logging
import time

load_dotenv()
translation_key = os.getenv("TRANSLATOR_KEY")
translation_region = os.getenv("TRANSLATOR_REGION")
doc_translation_endpoint = os.getenv("DOC_TRANSLATOR_ENDPOINT")

logger = logging.getLogger()

def azure_text_translate(text, target_lang, source_lang):
    
    client = TextTranslationClient(
        credential=AzureKeyCredential(translation_key),
        region=translation_region)

    if source_lang:
        return _text_translate(client, text, target_lang, source_lang)
    else:
        return _text_translate_auto(client, text, target_lang)

def _text_translate(client, text, target_lang, source_lang):
    try:
        start = time.time()
        response = client.translate(body=[text], to_language=[target_lang], from_language=source_lang)
        elapsed_time = time.time() - start
        translation = response[0] if response else None
        result = []
        if translation:
            for translated in translation.translations:
                result.append(translated.text)
        return {
            "translated_text": result,
            "source_language": source_lang
        }, elapsed_time
    except Exception as e:
        logger.info(f"Translation error: {str(e)}")
        return {
            "error": f"Translation error: {str(e)}"
        }, 0

def _text_translate_auto(client, text, target_lang):
    try:
        start = time.time()
        response = client.translate(body=[text], to_language=[target_lang])
        elapsed_time = time.time() - start
        translation = response[0] if response else None
        result = []
        if translation:
            detected_lang = translation.detected_language
            for translated in translation.translations:
                result.append(translated.text)
        return {
            "translated_text": result,
            "source_language": detected_lang
        }, elapsed_time
    except Exception as e:
        logger.info(f"Translation error: {str(e)}")
        return {
            "error": f"Translation error: {str(e)}"
        }, 0