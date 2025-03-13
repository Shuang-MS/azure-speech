import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import time
import logging
from utils import constants

load_dotenv()
SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
endpoint_string = "wss://{}.stt.speech.microsoft.com/speech/universal/v2".format(SPEECH_REGION)



def get_speech_client(audio_file, target_lang, src_lang):
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=SPEECH_KEY,
        endpoint=endpoint_string
    )
    speech_translation_config.add_target_language(target_lang)

    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    if src_lang:
        speech_translation_config.speech_recognition_language = src_lang
        return speechsdk.translation.TranslationRecognizer(
            translation_config=speech_translation_config,             
            audio_config=audio_config
        )
    else: 
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig()
        return speechsdk.translation.TranslationRecognizer(
            translation_config=speech_translation_config,
            audio_config=audio_config,
            auto_detect_source_language_config=auto_detect_source_language_config
        )     

def recognize_from_file(audio_file, target_lang, src_lang=None):
    print("Starting speech translation...")
    recognizer = get_speech_client(audio_file, target_lang, src_lang)
    start = time.time()
    result = recognizer.recognize_once()
    elapsed_time =time.time() - start
    recognized = result.text
    translation = result.translations.get(target_lang, None)
    
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        recognized = result.text
        translation = result.translations[target_lang]
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized = result.text
        source_lang = result.properties[speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Translation canceled: {}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(result.cancellation_details.error_details))

    return recognized, translation, elapsed_time

def synthesize_text(translation, language):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = {
        "zh-CN": "zh-CN-XiaoxiaoMultilingualNeural",
        "en-US": "en-US-AvaMultilingualNeural",
        "ja-JP": "ja-JP-NanamiNeural",
        "ko-KR": "ko-KR-SunHiNeural",
        "de-DE": "de-DE-KatjaNeural",
        "fr-FR": "fr-FR-DeniseNeural",
        "es-ES": "es-ES-ElviraNeural"
    }.get(language, "en-US-AvaMultilingualNeural")

    audio_config = speechsdk.audio.AudioOutputConfig(filename=f"/tmp/synthesized.wav")
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


    result = synthesizer.speak_text_async(translation).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        print("Speech synthesis failed: {}".format(result.reason))
        return None