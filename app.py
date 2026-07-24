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

# Load the local json knowledge file
try:
    with open("college_data.json", "r") as f:
        college_context = json.load(f)
except Exception:
    college_context = {
        "college_name": "Siddhartha Institute of Engineering and Technology",
        "courses": ["Computer Science Engineering", "Data Science", "Artificial Intelligence"]
    }

@app.route("/chat", methods=["POST"])
def chat():
    # Strict validation of incoming content
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "No text content found"}), 400
        
    user_text = str(data["text"]).strip()
    if not user_text:
        user_text = "hello"

    try:
        # 1. Handle Language Translation safely
        try:
            detector = GoogleTranslator(source='auto', target='en')
            text_in_english = detector.translate(user_text)
            detected_lang = detector.source
        except Exception:
            text_in_english = user_text
            detected_lang = 'en'

        # 2. Query Llama API with a total fail-safe try block
        engine_reply_en = ""
        if HF_TOKEN:
            try:
                system_prompt = f"System: You are an advisor. Use only this data: {json.dumps(college_context)}. Answer in 2 sentences max."
                payload = {
                    "inputs": f"{system_prompt}\n\nUser: {text_in_english}\nAssistant:",
                    "parameters": {"max_new_tokens": 100, "return_full_text": False}
                }
                hf_response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=5)
                res_data = hf_response.json()
                
                if isinstance(res_data, list) and len(res_data) > 0:
                    engine_reply_en = res_data[0].get('generated_text', '').strip()
                elif isinstance(res_data, dict):
                    engine_reply_en = res_data.get('generated_text', '').strip()
            except Exception:
                engine_reply_en = ""

        # 3. Local hardcoded answer generation if Hugging Face API limits or tokens fail
        if not engine_reply_en:
            clean_query = text_in_english.lower()
            if "fee" in clean_query or "cost" in clean_query:
                engine_reply_en = "The tuition fee for Computer Science Engineering is $8,000 per year, and Data Science is $8,500 per year."
            elif "course" in clean_query or "branch" in clean_query:
                engine_reply_en = "Siddhartha Institute offers Computer Science Engineering and Data Science programs."
            elif "placement" in clean_query or "job" in clean_query or "package" in clean_query:
                engine_reply_en = "Our highest placement package reached $45,000 per year, with top recruiters including Google, Microsoft, and Amazon."
            else:
                engine_reply_en = "Welcome to Siddhartha Institute of Engineering and Technology. How can I assist you with admissions, courses, or placement questions today?"

        # 4. Translate response text back to original spoken tongue
        try:
            final_reply_text = engine_reply_en
            if detected_lang and detected_lang != 'en':
                final_reply_text = GoogleTranslator(source='en', target=detected_lang).translate(engine_reply_en)
        except Exception:
            final_reply_text = engine_reply_en

        # 5. Build voice track output
        output_audio_path = "response.mp3"
        if os.path.exists(output_audio_path):
            try: os.remove(output_audio_path)
            except Exception: pass
            
        tts = gTTS(text=final_reply_text, lang=detected_lang if detected_lang else 'en')
        tts.save(output_audio_path)

        return send_file(output_audio_path, mimetype="audio/mp3")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
