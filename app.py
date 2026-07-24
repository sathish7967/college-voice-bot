import os
import json
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from deep_translator import GoogleTranslator
from gtts import gTTS

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://huggingface.co"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

with open("college_data.json", "r") as f:
    college_context = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
        
    user_text = data["text"]

    try:
        # 1. Translate Input Text to English
        detector = GoogleTranslator(source='auto', target='en')
        text_in_english = detector.translate(user_text)
        detected_lang = detector.source

        # 2. Query Llama 3 on Hugging Face
        system_prompt = f"System: You are an advisor. Use only this data: {json.dumps(college_context)}. Answer in 2 sentences max."
        payload = {
            "inputs": f"{system_prompt}\n\nUser: {text_in_english}\nAssistant:",
            "parameters": {"max_new_tokens": 100, "return_full_text": False}
        }
        
        hf_response = requests.post(HF_API_URL, headers=headers, json=payload)
        engine_reply_en = hf_response.json()['generated_text'].strip()

        # 3. Translate Response back to User's Native Language
        final_reply_text = engine_reply_en
        if detected_lang != 'en':
            final_reply_text = GoogleTranslator(source='en', target=detected_lang).translate(engine_reply_en)

        # 4. Synthesize voice audio track
        tts = gTTS(text=final_reply_text, lang=detected_lang)
        output_audio_path = "response.mp3"
        tts.save(output_audio_path)

        return send_file(output_audio_path, mimetype="audio/mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
