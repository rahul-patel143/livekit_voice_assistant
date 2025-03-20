from flask import Flask, request, send_file
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/validate_audio', methods=['POST'])
def validate_audio():
    """Validate and trim audio if longer than 60 seconds."""
    if 'audio' not in request.files:
        return {"error": "No audio file provided"}, 400
    
    audio_file = request.files['audio']
    audio = AudioSegment.from_file(audio_file)

    if len(audio) > 60000:  # Convert milliseconds to seconds (60s)
        start_trim = (len(audio) - 60000) // 2  # Trim center
        audio = audio[start_trim:start_trim + 60000]

    output_io = io.BytesIO()
    audio.export(output_io, format="mp3")
    output_io.seek(0)

    return send_file(output_io, mimetype="audio/mp3")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
