from flask import Flask, request, send_file
from gtts import gTTS
import tempfile

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")

    if not text:
        return {"error": "No text provided"}, 400

    tts = gTTS(text=text, lang="es")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)

    return send_file(tmp.name, mimetype="audio/mpeg")

@app.route("/")
def home():
    return "TTS Server is running"