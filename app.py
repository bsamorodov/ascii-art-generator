from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pyfiglet

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# A list of some common figlet fonts
fonts = [
    'standard',
    'slant',
    '3-d',
    '3x5',
    '5lineoblique',
    'alphabet',
    'banner3-d',
    'doh',
    'isometric1',
    'letters',
    'alligator',
    'dotmatrix',
    'bubble',
    'bulbhead',
    'digital',
    'block'
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    fonts.sort()
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts, "ascii_art": ""})

@app.post("/", response_class=HTMLResponse)
async def generate_art(request: Request, text: str = Form(...), font: str = Form(...)):
    ascii_art = ""
    if text and font:
        try:
            fig = pyfiglet.Figlet(font=font)
            ascii_art = fig.renderText(text)
        except pyfiglet.FontNotFound:
            ascii_art = "Font not found!"
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts, "ascii_art": ascii_art})
