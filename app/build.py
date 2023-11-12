import os
import shutil
import subprocess
from pathlib import Path

from tqdm import tqdm

from extractor import extract_data, process_audio
from models import music_list_type


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
    for music in tqdm(musics, desc="Copying music"):
        for part in music.parts:
            filepath = Path(part.filename)
            path_in_static = f"musics/{filepath.name}"
            new_path = current_module_path / "static" / path_in_static
            # print(filepath, new_path)
            shutil.copy2(filepath, new_path)
            part.filename = path_in_static

    return musics


def main():
    musics = get_musics()

    with open(Path("ui") / "src" / "music.json", "w") as f:
        f.write(music_list_type.dump_json(musics).decode())

    shutil.copytree(
        Path("static") / "musics", Path("ui") / "static" / "musics", dirs_exist_ok=True
    )

    subprocess.run("""cd ui && npm run build""", shell=True)

    print("Successfully built in ui/build")


if __name__ == "__main__":
    main()
