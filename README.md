# Multilingual AI Voice Chatbot for College Inquiries

A production-ready, 100% cost-free voice assistant that allows prospective students to ask questions about college admissions, courses, fees, and placements using natural speech in any language. The system automatically detects the spoken language, queries an immutable local knowledge base via an open-source LLM, and speaks the answer back in the user's native tongue.

Live Demo Frontend: [Insert your GitHub Pages Link Here]
Live API Backend: [Insert your Render Service Link Here]

## 🚀 Key Features
*   **Zero-Touch Voice Interface:** High-fidelity web audio capture utilizing browser native media APIs.
*   **Zero-Cost Architecture:** Leverages entirely free cloud infrastructure, bypassing enterprise API licensing overheads.
*   **Universal Multilingual Support:** Seamless real-time input localization and response translation using the Google Translate engine.
*   **Deterministic Knowledge Guardrails:** Combines a localized JSON knowledge graph with strict system prompt contexts to completely eliminate LLM hallucinations regarding official institutional parameters.
*   **Enterprise-Grade Security:** Utilizes server-side runtime environment variables (`os.environ`) to prevent secret exposure or API key leakage in open-source code repositories.

---

## 🛠️ System Architecture & Workflow

[HTML5 User Mic Input] ➔ [SpeechRecognition (WAV Conversion)] ➔ [Auto-Language Detection Engine]│[Translate to English]│[User Audio Response] 🖙 [gTTS Audio Engine] 🖙 [Translate to User Lang] 🖙 [Llama 3 AI Inference API]
---

## 💻 Tech Stack
*   **Frontend UI:** Vanilla JavaScript, HTML5 Web Audio API, Responsive Minimal CSS.
*   **Application Backend:** Python, Flask, Flask-CORS, Gunicorn WSGI HTTP Server.
*   **Generative AI Engine:** Meta Llama-3-8B-Instruct (via Hugging Face Serverless Inference API).
*   **Voice & Translation Pipelines:** Google Web Speech Recognition API (`SpeechRecognition`), `gTTS` (Google Text-to-Speech), `deep-translator`.
*   **Cloud Deployment:** Render (Free Web Service Tier), GitHub Pages (Static Hosting).

---

## 📁 Repository Structure
```text
├── app.py                # Main Flask API containing transcription, processing, and translation logic
├── college_data.json     # Controlled institutional knowledge base (Admissions, Fees, Placements)
├── index.html            # Web-based frontend single-button voice capture user interface
├── requirements.txt      # Server application dependencies and production packages
└── README.md             # Project documentation and deployment guide
```

---

## 🛠️ Local Development Setup

### 1. Clone and Prepare Environment
```bash
git clone https://github.com
cd college-voice-bot
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials
Get a free Read access token from [huggingface.co](https://huggingface.co) and export it to your terminal:
```bash
export HF_TOKEN="your_hugging_face_token_here"
# On Windows Command Prompt: set HF_TOKEN="your_hugging_face_token_here"
```

### 4. Run the Servers
Launch the backend server:
```bash
python app.py
```
Open the `index.html` file in any browser to test your audio recording inputs.

---

## 🌐 Production Deployment Flow

### Backend (Render)
1. Hosted as a free Python Web Service on **Render.com** linked directly to the `main` branch.
2. Built using python packages listed in `requirements.txt`.
3. Executed dynamically via production command: `gunicorn app:app`.
4. API access managed securely through Render's internal **Environment Variables** dashboard container using the `HF_TOKEN` key.

### Frontend (GitHub Pages)
1. Hosted globally via **GitHub Pages**.
2. Leverages complete static asset extraction directly out of the project repository.
3. Automatically served via **HTTPS**, fulfilling production browser criteria necessary to unlock user microphone permissions.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
