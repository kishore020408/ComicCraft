import os, requests, time
from dotenv import load_dotenv
load_dotenv()

def generate_comic_image(prompt, panel_num):
    safe_prompt = prompt.replace(" ", "%20")[:400]
    os.makedirs("app/static", exist_ok=True)
    path = f"app/static/panel_{panel_num}.png"

    # METHOD 1: Try Google Imagen 3 (if your key supports)
    try:
        from google import genai
        from PIL import Image
        from io import BytesIO
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        # New correct model name
        result = client.models.generate_images(
            model="imagen-3.0-generate-001",
            prompt=f"cartoon comic style, vibrant, {prompt}"
        )
        if result.generated_images:
            image_bytes = result.generated_images[0].image.image_bytes
            with open(path, "wb") as f:
                f.write(image_bytes)
            print(f"Imagen Success panel {panel_num}")
            return f"/static/panel_{panel_num}.png?t={int(time.time())}"
    except Exception as e:
        print(f"Imagen failed panel {panel_num}: {e}")

    # METHOD 2: 100% Free Backup - Pollinations (No API Key)
    try:
        print(f"Trying free image for panel {panel_num}...")
        url = f"https://image.pollinations.ai/prompt/cartoon%20comic%20vibrant%20{safe_prompt}?width=512&height=512&nologo=true&model=turbo"
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"Free image success panel {panel_num}")
            return f"/static/panel_{panel_num}.png?t={int(time.time())}"
    except Exception as e:
        print(f"Free image failed {e}")

    return None