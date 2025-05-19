from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")
transcribe_deployment = os.getenv("gpt-4o-transcribe")
tts_deployment = os.getenv("gpt-4o-mini-tts")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        
client = AzureOpenAI(
    api_key=api_key,  
    api_version=api_version,
    azure_endpoint=endpoint
)

def transcribe(file_path, model, stream=False):
    with open(file_path, "rb") as audio_file:
        try:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model=model,
                response_format="json",
                stream=stream
            )

            if stream:
                transcript = ""
                for event in response:
                    if hasattr(event, "delta"):
                        transcript += event.delta
                        print(f"\r{transcript}", end="", flush=True)
                print()
                result = transcript
            else:
                result = response.text
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    return result