from __future__ import annotations
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import os
import asyncio
import tempfile
import subprocess
import speech_recognition as sr
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
)
from gtts import gTTS
import requests

# Load environment variables
load_dotenv(dotenv_path=".env.local")

# Setup logger
logger = logging.getLogger("voice-assistant")
logger.setLevel(logging.INFO)

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing. Set GEMINI_API_KEY in .env.local.")

genai.configure(api_key=GEMINI_API_KEY)

recognizer = sr.Recognizer()

async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    # Subscribe to audio track
    participant.on_track_subscribed = lambda track, _: asyncio.create_task(process_audio(track))

    await run_gemini_agent(ctx, participant)

async def process_audio(audio_track: rtc.AudioStreamTrack):
    """Processes the incoming audio track"""
    logger.info("Listening for audio input...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio_data = recognizer.listen(source,timeout=20, phrase_time_limit=10)
                text = recognizer.recognize_google(audio_data)
                if text:
                    logger.info(f"Recognized: {text}")
                    return text
            except sr.UnknownValueError:
                logger.warning("Could not understand the audio")
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")

async def run_gemini_agent(ctx: JobContext, participant: rtc.RemoteParticipant):
    logger.info("Starting voice assistant with Gemini API")

    model = genai.GenerativeModel("gemini-1.5-pro")

    # Initial greeting
    text_response = "Hello! How can I assist you today?"
    await send_audio_response(ctx, text_response)

    while True:
        user_input = await process_audio(participant)
        if not user_input:
            continue

        # Generate AI response
        response = model.generate_content(user_input)

        if response.text:
            await send_audio_response(ctx, response.text)
            logger.info("Gemini AI response sent as audio!")

async def send_audio_response(ctx: JobContext, text: str):
    """Convert text to speech, validate with Flask API, and play the audio."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts = gTTS(text)
            tts.save(temp_audio.name)

        # Send to Flask API for validation
        with open(temp_audio.name, "rb") as audio_file:
            files = {"audio": ("audio.mp3", audio_file, "audio/mpeg")}
            response = requests.post("http://127.0.0.1:5000/validate_audio", files=files)

        if response.status_code == 200:
            # Save validated audio
            validated_audio_path = "validated_response.mp3"
            with open(validated_audio_path, "wb") as f:
                f.write(response.content)

            # Play the validated audio
            subprocess.run(["mpg123", validated_audio_path])

            logger.info(f"Sent validated audio response: {text}")

            os.remove(validated_audio_path)

        else:
            logger.error(f"Flask API error: {response.json()}")

        os.remove(temp_audio.name)

    except Exception as e:
        logger.error(f"Failed to generate audio: {e}")

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
