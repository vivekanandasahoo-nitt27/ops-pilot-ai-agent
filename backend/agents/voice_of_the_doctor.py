import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv

load_dotenv()

def text_to_speech_with_elevenlabs(text, output_path="doctor_voice.mp3"):
    
    api_key = os.getenv("ELEVENLABS_API_KEY")

    client = ElevenLabs(api_key=api_key)

    audio = client.text_to_speech.convert(
        voice_id="bRXVSWfGAX7wzEoX7iZ7",
        model_id="eleven_flash_v2_5",
        text=text
    )

    save(audio, output_path)

    return output_path