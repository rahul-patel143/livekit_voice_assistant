# AI Voice Assistant using LiveKit & Google Gemini & OpenAI

🚀 **An advanced AI-powered voice assistant** that enables real-time **voice-to-voice communication** using **LiveKit, Google Gemini AI, OpenAI, Flask, and Node.js**. This assistant **listens to speech, processes responses using AI, and speaks back** – all in an interactive manner.

---

## 🌟 Features
✅ **Real-Time Voice Communication** using **LiveKit**  
✅ **Speech Recognition** with `speech_recognition` for audio-to-text conversion  
✅ **AI-Powered Responses** using **Google Gemini API**  
✅ **Text-to-Speech (TTS)** conversion with `gTTS`  
✅ **Audio Validation**: Ensures audio responses are **≤ 60 seconds**  
✅ **Web-Based Interaction** with **Node.js frontend**  

---

## 💁️ Project Structure

```
agent/
│── venv/                        # Python virtual environment
│── voice_assistant/
│   ├── templates/               # Contains `index.html`
│   ├── .env.local               # Environment variables (ignored in Git)
│   ├── app.py                   # Flask app for uploading audio and receiving responses
│   ├── audio_api.py             # Flask API for audio validation & trimming
│   └── gemini_agent.py          # LiveKit AI agent for real-time voice interaction
│── voice_assistant_frontend/    # Node.js frontend for user interactions
│── .gitignore                   # Ignored files
│── requirements.txt             # Python dependencies
│── README.md                    # Documentation (You are here 🌟)
```

---

## ⚡ Installation Guide

### 1⃣ Clone the Repository
```bash
git clone https://github.com/rahul-patel143/livekit_voice_assistant.git
```

### 2⃣ Setup Python Virtual Environment
```bash
cd agent
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3⃣ Setup Environment Variables
Create a **`.env.local`** file inside `voice_assistant/` and add:
```
GEMINI_API_KEY=your_google_gemini_api_key
```
> ⚠️ **Important:** Ensure your API key is valid for Google Gemini.

### 4⃣ Install Node.js Dependencies (Frontend)
```bash
cd voice_assistant_frontend
npm install
```

---

## 🎯 Running the Project

### 🚀 1. Start the **LiveKit AI Agent**
This runs the assistant that **listens to audio, processes AI responses, and speaks back**.
```bash
cd agent/voice_assistant
python3 gemini_agent.py dev
```

### 🎧 2. Run the **Flask Audio API**
The audio API **validates and trims** responses longer than 60 seconds.
```bash
python3 audio_api.py
```

### 🔊 3. Run the **Flask Web Interface**
This allows users to **upload audio files** and receive AI-generated responses.
```bash
python3 app.py
```

### 🌐 4. Start the **Node.js Frontend**
The frontend provides a **web-based interface** for the assistant.
```bash
cd voice_assistant_frontend
npm run dev
```

---

## ⚙️ Additional Commands

### 🌍 Running with Gunicorn (Production Deployment)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 📊 Running Flask in Debug Mode
```bash
FLASK_APP=app.py FLASK_ENV=development flask run
```

### 🔕 Stopping Processes
```bash
CTRL + C  # Stop running processes
```

---

## 🚫 Troubleshooting

### 🔹 **Mpg123 Not Found (Linux/macOS)**
If you get an error while playing audio, install `mpg123`:
```bash
sudo apt install mpg123  # Debian/Ubuntu
brew install mpg123      # macOS
```

### 🔹 **Google Gemini API Key Error**
Ensure your **`.env.local`** file contains a **valid API key**.

### 🔹 **Port Conflicts**
If Flask or Node.js fails to start due to port issues, try:
```bash
lsof -i :5000   # Check for processes using port 5000
kill -9 <PID>   # Kill the process using that port
```
---

## 👨‍💻 Author
**Rahul Patel**  
🚀 Python Developer @ Qrious Tech  
📞 [LinkedIn](https://www.linkedin.com/in/rahul-patel)
