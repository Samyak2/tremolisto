import os
import shutil
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from extractor import extract_data, process_audio

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def _get_env(key: str):
    if val := os.getenv(key):
        return val
    else:
        raise Exception(f"Required configuration {key} not found")


def _get_musics():
    with open(_get_env("MUSIC_LIST_FILE")) as f:
        contents = f.read()

    musics = process_audio(extract_data(contents))
    current_module_path = Path(__file__).resolve().parent.parent
    for music in musics:
        for part in music.parts:
            filepath = Path(part.filename)
            path_in_static = f"musics/{filepath.name}"
            new_path = current_module_path / "static" / path_in_static
            print(filepath, new_path)
            shutil.copy2(filepath, new_path)
            part.filename = path_in_static

    return musics


musics = _get_musics()
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
