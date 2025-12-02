import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_text(text):
    try:
        prompt = f"Corectează eventualele greșeli de ortografie și gramatică din textul următor, fără a modifica sensul:\n\n{text}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ești un asistent care corectează textul într-un mod natural și precis."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Eroare la corectare:", e)
        return text