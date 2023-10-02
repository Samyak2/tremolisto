import os

from pydantic import BaseModel
from pydub import AudioSegment

from cache import cached
from models import MusicPart

_PART_DIR = ".music_parts"


class CutAudioInput(BaseModel):
    filename: str
    part: MusicPart


class CutAudioOutput(BaseModel):
    filename: str


@cached
def cut_audio(input: CutAudioInput) -> CutAudioOutput:
    os.makedirs(_PART_DIR, exist_ok=True)

    without_ext = input.filename.rsplit(".", maxsplit=1)[0]
    output_file = os.path.join(
        _PART_DIR,
        (
            f"{without_ext}_{input.part.start.replace(':', '-')}"
            + f"_{input.part.end.replace(':', '-')}.mp3"
        ),
    )

    audio_file = AudioSegment.from_file(input.filename)
    audio_file = audio_file[input.part.start_millis() : input.part.end_millis()]

    audio_file.export(output_file, format="mp3")

    return CutAudioOutput(filename=output_file)
