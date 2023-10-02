from dataclasses import field
from typing import Optional

from pydantic import BaseModel


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


class Music(BaseModel):
    title: str
    artist: str

    url: Optional[str] = None
    parts: list[MusicPart] = field(default_factory=list)
