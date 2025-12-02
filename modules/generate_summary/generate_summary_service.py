import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text):
    try:
        prompt = f"Generează un rezumat concis și complet al următorului text:\n\n{text}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ești un asistent care realizează rezumate clare și concise, păstrând toate informațiile importante."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Eroare la generarea rezumatului:", e)
        return "Nu s-a putut genera rezumatul."