from flask import Flask, request, send_file
from gtts import gTTS
import tempfile
import os

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json

    text = data.get("text", "")
    source = data.get("source", "")  # نام منبع خبر

    if not text:
        return {"error": "No text provided"}, 400

    # --- ساخت نام فایل از 5 کلمه اول تیتر ---
    words = text.split()
    first_five = "_".join(words[:5]).lower()
    filename = f"{first_five}_....mp3"
    tmp_path = f"/tmp/{filename}"

    # --- تولید فایل صوتی ---
    tts = gTTS(text=text, lang="es")
    tts.save(tmp_path)

    # --- افزودن متادیتا (Artist + Title + Source + Genre) ---
    try:
        audio = MP3(tmp_path, ID3=EasyID3)
    except:
        audio = MP3(tmp_path)
        audio.add_tags()

    audio["artist"] = f"Spain News Today | Source: {source}"    # نام کانال
    audio["title"] = text                     # تیتر کامل + خلاصه
    audio["album"] = f"Source: {source}"      # نام منبع خبر
    audio["genre"] = "News"                   # حرفه‌ای‌تر

    audio.save()

    # --- ارسال فایل ---
    return send_file(tmp_path, mimetype="audio/mpeg", download_name=filename)

@app.route("/")
def home():
    return "TTS Server is running"

