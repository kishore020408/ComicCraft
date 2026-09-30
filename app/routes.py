from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><body style="font-family:sans-serif; text-align:center; padding:30px">
    <h1>ComicCraft Ready Da! 😎</h1>
    <form action="/generate" method="post">
    <input name="prompt" placeholder="Story idea" style="width:300px;padding:10px"><br><br>
    <input name="character" placeholder="Character" value="Tom"><br><br>
    <input name="setting" placeholder="Setting" value="Chennai"><br><br>
    <input name="tone" value="Funny"><br><br>
    <input name="art" value="Cartoon"><br><br>
    <button type="submit" style="padding:10px 20px">Generate Comic</button>
    </form></body></html>
    """

@router.post("/generate", response_class=HTMLResponse)
def generate_comic(prompt: str = Form(...), character: str = Form(...), setting: str = Form(""), tone: str = Form(""), art: str = Form("")):
    outline = generate_outline(prompt, character, setting, tone, art)
    story = generate_story(outline, character)
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.gemini_image import generate_comic_image

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><head><style>body{font-family:sans-serif;text-align:center;padding:20px;background:#f0f0f0} input{width:300px;padding:10px;margin:5px} button{padding:12px 25px;background:#ff4757;color:white;border:none;border-radius:5px;font-size:16px;cursor:pointer}</style></head>
    <body><h1>🎨 ComicCraft + AI Images 🔥</h1>
    <form action="/generate" method="post">
    <input name="prompt" placeholder="Story idea - ex: Tom lost in Chennai" required><br>
    <input name="character" placeholder="Character" value="Tom, orange fox"><br>
    <input name="setting" placeholder="Setting" value="Chennai jungle"><br>
    <input name="tone" value="Funny"><br>
    <input name="art" value="Cartoon, vibrant"><br><br>
    <button type="submit">Generate Comic With Images</button>
    </form></body></html>
    """

@router.post("/generate", response_class=HTMLResponse)
def generate_comic(prompt: str = Form(...), character: str = Form(...), setting: str = Form(""), tone: str = Form(""), art: str = Form("")):
    outline = generate_outline(prompt, character, setting, tone, art)
    story = generate_story(outline, character)
    html = "<html><head><style>body{font-family:sans-serif;padding:20px;background:#fff}.panel{border:2px solid #ddd;margin:20px;padding:15px;border-radius:12px;background:#fafafa} img{max-width:400px;border-radius:10px;margin-top:10px} </style></head><body><h1>Your Comic:</h1><a href='/'>⬅️ Back</a><br><br>"
    for i, p in enumerate(story, 1):
        img_path = generate_comic_image(p.get('image_prompt','cartoon scene'), i)
        img_tag = f"<br><img src='{img_path}'><br>" if img_path else "<br><i>(Image generating... try again if not visible)</i><br>"
        html += f"<div class='panel'><h3>Panel {p.get('panel', i)}: {p.get('title','')}</h3><p><b>Scene:</b> {p.get('scene_description','')}</p><p><b>Dialogue:</b> {p.get('dialogue','')}</p>{img_tag}<p style='font-size:12px;color:gray'>Prompt: {p.get('image_prompt','')}</p></div>"
    html += "</body></html>"
    return html