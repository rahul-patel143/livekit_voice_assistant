from flask import Flask, render_template, request, send_file, jsonify
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing. Set GEMINI_API_KEY in .env.local.")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

# Convert Audio to Text (Speech-to-Text)
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)

# Trim Audio from Center (Max: 60 seconds)
def trim_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    max_duration = 60 * 1000  # 60 seconds in milliseconds

    if len(audio) > max_duration:
        start_trim = (len(audio) - max_duration) // 2
        end_trim = start_trim + max_duration
        trimmed_audio = audio[start_trim:end_trim]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        trimmed_audio.export(temp_file.name, format="wav")
        return temp_file.name
    return audio_file

# Generate AI Response and Convert to Audio
def generate_audio_from_text(text):
    model = genai.GenerativeModel("gemini-1.5-pro")
    text = text + """You are a voice assistant created by LiveKit. Your interface with users will be voice.
            You should use short and concise responses, and avoiding usage of unpronouncable punctuation.
            You were created as a demo to showcase the capabilities of LiveKit's agents framework."""
    response = model.generate_content(text)
    print(response.text)

    if not response.text:
        return None, "AI response is empty"

    # Convert response to audio
    tts = gTTS(response.text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tts.save(temp_file.name)

    # Trim if longer than 60 sec
    trimmed_file = trim_audio(temp_file.name)
    return trimmed_file, None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_audio", methods=["POST"])
def process_audio():
    """Receive audio input, process AI response, return audio output."""
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio_file.save(temp_audio.name)

    try:
        # Convert speech to text
        input_text = audio_to_text(temp_audio.name)
        input_text = input_text + ' note: do not add any programming related code.'
        
        # Process AI response
        audio_file, error = generate_audio_from_text(input_text)

        if error:
            return jsonify({"error": error}), 500

        return send_file(audio_file, mimetype="audio/wav", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
