from typing import Any, Optional, cast

from pydantic import BaseModel, TypeAdapter
from yt_dlp import YoutubeDL

from cache import cached

audio_file_input = TypeAdapter(str)


class AudioInput(BaseModel):
    url: str


class DownloadedAudio(BaseModel):
    filename: str
    info: dict[str, Any]


@cached
def get_audio_file(input: AudioInput) -> DownloadedAudio:
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
        info = ydl.extract_info(input.url)
        info = ydl.sanitize_info(info)

    if final_filename is None:
        raise Exception("progress hook did not run!")

    return DownloadedAudio(filename=final_filename, info=cast(dict[str, Any], info))
