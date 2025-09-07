import os
import requests
import speech_recognition as sr
import pyttsx3
from playsound import playsound
from app.llm_huggingface import generate_response

def speech_to_text(audio_file_path):
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "I couldn't understand. Could you please try again?"
    except sr.RequestError as e:
        return f"API error: {e}"

def text_to_speech_local(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def text_to_speech_cloud(text):
    NARAKEET_API_URL = "https://api.narakeet.com/text-to-speech"
    CHILD_VOICE_NAME = "child-female-english"
    api_key = os.getenv("NARAKEET_API_TOKEN")
    if not api_key:
        print("No Narakeet API key set. Falling back to local TTS.")
        text_to_speech_local(text)
        return
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"voice": CHILD_VOICE_NAME, "text": text, "outputFormat": "mp3"}
    try:
        resp = requests.post(NARAKEET_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        with open("output/output.mp3", 'wb') as f:
            f.write(resp.content)
        playsound("output/output.mp3")
    except Exception as e:
        print(f"NARAKEET API error: {e}")
        text_to_speech_local(text)

def interactive_loop():
    question = speech_to_text()
    print("Transcribed:", question)
    answer = generate_response(question)
    print("Assistant:", answer)
    text_to_speech_cloud(answer)
