import os
import uuid
from langdetect import detect
from gtts import gTTS

def generate_tts_audio(text, output_dir="static/tts"):
    try:
        # Detect language
        try:
            detected_lang = detect(text)
        except Exception:
            detected_lang = "en"

        # Prepare output filepath
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(output_dir, filename)

        # Ensure folder exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate audio
        tts = gTTS(text=text, lang=detected_lang)
        tts.save(filepath)

        return {
            "audio_url": f"/{filepath.replace(os.sep, '/')}",
            "detected_lang": detected_lang
        }

    except Exception as e:
        print("Eroare la generarea TTS:", e)
        return None