from dataclasses import field
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, TypeAdapter


def _time_to_millis(time: str) -> int:
    """Convert time in mm:ss to milliseconds."""
    mins, secs = time.split(":", maxsplit=1)
    mins = int(mins)
    secs = int(secs)

    return mins * 60 * 1000 + secs * 1000


class MusicPart(BaseModel):
    start: str
    end: str
    typ: str
    extra: str

    def has_time(self) -> bool:
        return bool(self.start) and bool(self.end)

    def start_millis(self) -> int:
        return _time_to_millis(self.start)

    def end_millis(self) -> int:
        return _time_to_millis(self.end)


class MusicPartWithFile(MusicPart):
    filename: str

    @classmethod
    def from_music_part(cls, music_part: MusicPart, filename: str):
        return MusicPartWithFile(**music_part.model_dump(), filename=filename)


M = TypeVar("M", bound=MusicPart)


class Music(BaseModel, Generic[M]):
    title: str
    artist: str

    url: Optional[str] = None
    parts: list[M] = field(default_factory=list)


music_list_type = TypeAdapter(list[Music[MusicPartWithFile]])
