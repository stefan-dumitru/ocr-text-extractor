from flask import Flask, render_template, request, jsonify
import os
import uuid
from pdf2image import convert_from_path
poppler_path = r"C:\Program Files\poppler-25.07.0\Library\bin"

from modules.text_extractor import extract_text_from_file
from modules.text_corrector import correct_text
from modules.generate_summary import generate_summary
from modules.translate_text import translate_text
from modules.tts import generate_tts_audio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    text = None
    corrected_text = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'Niciun fișier trimis.'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Niciun fișier selectat.'}), 400

        # save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # check file type
        if file.filename.lower().endswith('.pdf'):
            pages = convert_from_path(filepath, poppler_path=poppler_path)
            text = ""
            for page in pages:
                temp_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"page_{uuid.uuid4()}.png")
                page.save(temp_image_path, 'PNG')
                text += extract_text_from_file(temp_image_path) + "\n"
        else:
            text = extract_text_from_file(filepath)

        if text and text.strip():
            corrected_text = correct_text(text)

    languages = {
        "engleza": "en",
        "franceza": "fr",
        "italiana": "it",
        "spaniola": "es",
        "romana": "ro"
    }

    return render_template('index.html', text=text, corrected_text=corrected_text, summary=None, translated_text=None, languages=languages)

# endpoint for generating summary
@app.route('/generate_summary', methods=['POST'])
def generate_summary_endpoint():
    data = request.json
    corrected_text = data.get("corrected_text", "")
    if corrected_text.strip():
        summary = generate_summary(corrected_text)
        return jsonify({"summary": summary})
    return jsonify({"summary": "Textul corectat este gol."})

# endpoint for translating
@app.route('/translate', methods=['POST'])
def translate_endpoint():
    data = request.json
    corrected_text = data.get("corrected_text", "")
    target_lang = data.get("target_lang", "en")
    if corrected_text.strip():
        translated = translate_text(corrected_text, target_lang)
        return jsonify({"translated_text": translated})
    return jsonify({"translated_text": "Textul corectat este gol."})

# endpoint for TTS
@app.route('/tts', methods=['POST'])
def tts_endpoint():
    data = request.json
    corrected_text = data.get("corrected_text", "").strip()

    if not corrected_text:
        return jsonify({"error": "Textul corectat este gol."})

    result = generate_tts_audio(corrected_text)

    if result is None:
        return jsonify({"error": "Nu s-a putut genera fișierul audio."})

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)