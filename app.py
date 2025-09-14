from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyfiglet import Figlet, FigletFont

app = FastAPI()

templates = Jinja2Templates(directory="templates")


fonts = FigletFont.getFonts()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    fonts.sort()
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts, "ascii_art": ""})


@app.post("/", response_class=HTMLResponse)
async def generate_art(request: Request, text: str = Form(...), font: str = Form(...)):
    ascii_art = ""
    if text and font:
        try:
            fig = Figlet(font=font)
            ascii_art = fig.renderText(text)
        except FontNotFound:
            ascii_art = "Font not found!"
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts, "ascii_art": ascii_art})
