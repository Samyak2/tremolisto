from pathlib import Path
from typing import Callable, Optional, TypeVar
from yt_dlp import YoutubeDL
import os
import json

_MODULE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
_CACHE_FILE = _MODULE_DIR / ".music_cache.json"
_CACHE_FILE_BKP = _MODULE_DIR / ".music_cache.backup.json"

RetType = TypeVar("RetType")


def cached(func: Callable[..., RetType]) -> Callable[..., RetType]:
    def wrapper(url: str) -> RetType:
        _CACHE_FILE.touch()
        with open(_CACHE_FILE) as f:
            data = f.read()
        cache = json.loads(data or "{}")
        if url in cache:
            return cache[url]
        else:
            ret = func(url)
            cache[url] = ret

            _CACHE_FILE_BKP.touch()
            with open(_CACHE_FILE) as f_orig, open(_CACHE_FILE_BKP, "a") as f_bkp:
                f_bkp.write("\n")
                f_bkp.write(f_orig.read())

            with open(_CACHE_FILE, "w") as f:
                json.dump(cache, f)

            return ret

    return wrapper


@cached
def get_audio_file(url: str):
    final_filename: Optional[str] = None

    def _yt_dlp_progress_hook(d: dict):
        nonlocal final_filename

        if d["status"] == "finished":
            final_filename = d.get("filename")

    with YoutubeDL(
        {
            "check_formats": "selected",
            "extract_flat": "discard_in_playlist",
            "format": "bestaudio/best",
            # "fragment_retries": 10,
            # "ignoreerrors": "only_download",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    # "nopostoverwrites": False,
                    "preferredcodec": "best",
                    "preferredquality": "0",
                },
                # {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"},
            ],
            # "retries": 10,
            "progress_hooks": [_yt_dlp_progress_hook],
        }
    ) as ydl:
        info = ydl.extract_info(url)
        info = ydl.sanitize_info(info)

    return final_filename, info
