from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyfiglet import Figlet, FigletFont, FontNotFound
from starlette.middleware.session import SessionMiddleware

app = FastAPI()

# Add session middleware
# IMPORTANT: Change this secret key in a production environment
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

templates = Jinja2Templates(directory="templates")


fonts = FigletFont.getFonts()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    fonts.sort()
    # Get values from session if they exist
    text = request.session.get("text", "")
    font = request.session.get("font", fonts[0] if fonts else "")
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts, "ascii_art": "", "text": text, "selected_font": font})


@app.post("/", response_class=HTMLResponse)
async def generate_.art(request: Request, text: str = Form(...), font: str = Form(...)):
    ascii_art = ""
    if text and font:
        try:
            fig = Figlet(font=font)
            ascii_art = fig.renderText(text)
            # Store values in session
            request.session["text"] = text
            request.session["font"] = font
        except FontNotFound:
            ascii_art = "Font not found!"
    return templates.TemplateResponse("index.html", {"request": request, "fonts": fonts, "ascii_art": ascii_art, "text": text, "selected_font": font})