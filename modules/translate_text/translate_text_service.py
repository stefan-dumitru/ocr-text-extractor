from deep_translator import GoogleTranslator

def translate_text(text, target_lang):
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print("Eroare la traducere:", e)
        return "Nu s-a putut traduce textul."