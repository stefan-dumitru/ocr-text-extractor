import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_handwriting_text(filepath):
    try:
        # read image as base64
        with open(filepath, "rb") as f:
            img_bytes = f.read()
        b64_image = base64.b64encode(img_bytes).decode()

        # call OpenAI Vision
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extrage tot textul scris de mână din această imagine, păstrându-l în limba în care e scris. Returnează doar textul extras."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Eroare la Vision OCR:", e)
        return ""