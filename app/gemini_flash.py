import os, json
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_outline(prompt, character, setting, tone, art):
    full_prompt = f"Create 5 panel comic JSON array. Idea:{prompt}, Char:{character}, Setting:{setting}, Tone:{tone}, Art:{art}. Each object must have panel,title,scene_description,image_prompt,dialogue. Return ONLY JSON, no markdown."

    for model_name in ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.5-flash", "gemini-flash-latest"]:
        try:
            print(f"Trying {model_name}...")
            res = client.models.generate_content(model=model_name, contents=full_prompt)
            text = res.text.replace("```json","").replace("```","").strip()
            s=text.find('['); e=text.rfind(']')+1
            if s!=-1: text=text[s:e]
            data = json.loads(text)
            print(f"SUCCESS with {model_name}!")
            return data
        except Exception as e:
            print(f"Failed {model_name}: {e}")
            continue

    return [{"panel":1,"title":"Error","scene_description":"API failed","image_prompt":"error","dialogue":"Try again"}]