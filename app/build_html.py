import os
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from extractor import extract_data, process_audio


def _get_env(key: str):
    if val := os.getenv(key):
        return val
    else:
        raise Exception(f"Required configuration {key} not found")


def get_musics():
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


def main():
    musics = get_musics()

    env = Environment(
        loader=FileSystemLoader("templates"), autoescape=select_autoescape()
    )
    template = env.get_template("app.html")

    def url_for(dir: str, path: str):
        path = path.lstrip("/")
        return f"/{dir}/{path}"

    rendered = template.render({"musics": musics, "url_for": url_for})

    build_dir = Path("build")

    os.makedirs(build_dir, exist_ok=True)

    with open(build_dir / "index.html", "w") as f:
        f.write(rendered)

    shutil.copytree(Path("static"), build_dir, dirs_exist_ok=True)

    print(f"Successfully built in {build_dir}")


if __name__ == "__main__":
    main()
