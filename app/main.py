from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.build_html import get_musics

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


musics = get_musics()
print(musics)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "musics": musics,
        },
    )
