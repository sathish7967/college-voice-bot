import os
import json
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

# Free API Configurations
HF_TOKEN = os.environ.get("HF_TOKEN") # Set your Hugging Face Token here
HF_API_URL = "https://huggingface.co"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Load immutable college knowledge bank
with open("college_data.json", "r") as f:
    college_context = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    audio_file = request.files["audio"]
    webm_path = "user_input.webm"
    wav_path = "user_input.wav"
    audio_file.save(webm_path)

    try:
        # 1. Convert WebM (Browser standard) to standard WAV format
        sound = AudioSegment.from_file(webm_path)
        sound.export(wav_path, format="wav")

        # 2. Free Speech to Text via Google Web Speech Engine
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            # Language 'auto' isn't supported here, so we capture text directly
            user_text = recognizer.recognize_google(audio_data)

        # 3. Detect & Translate Input to English
        # We identify language and translate it using deep-translator
        detector = GoogleTranslator(source='auto', target='en')
        text_in_english = detector.translate(user_text)
        detected_lang = detector.source # Captured source language

        # 4. Generate Answer using Free Llama 3 on Hugging Face
        system_prompt = f"System: You are a college helper bot. Use only this data: {json.dumps(college_context)}. Answer in 2 sentences max."
        payload = {
            "inputs": f"{system_prompt}\n\nUser: {text_in_english}\nAssistant:",
            "parameters": {"max_new_tokens": 100, "return_full_text": False}
        }
        
        hf_response = requests.post(HF_API_URL, headers=headers, json=payload)
        response_json = hf_response.json()
        engine_reply_en = response_json[0]['generated_text'].strip()

        # 5. Translate Response back to User's Native Language
        final_reply_text = engine_reply_en
        if detected_lang != 'en':
            final_reply_text = GoogleTranslator(source='en', target=detected_lang).translate(engine_reply_en)

        # 6. Free Text to Speech via gTTS
        tts = gTTS(text=final_reply_text, lang=detected_lang)
        output_audio_path = "response.mp3"
        tts.save(output_audio_path)

        return send_file(output_audio_path, mimetype="audio/mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Cleanup server storage files
        for path in [webm_path, wav_path]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
