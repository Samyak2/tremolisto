import re
import sys

from dataclasses import dataclass, field
from typing import Optional
from pprint import pprint


@dataclass
class MusicPart:
    start: str
    end: str
    typ: str
    extra: str


@dataclass
class Music:
    title: str
    artist: str

    url: Optional[str] = None
    parts: list[MusicPart] = field(default_factory=list)


_PART_RE = re.compile(r"(.*):\s*(\d+:\d+)\s*-\s*(\d+:\d+)\s*(\(.*\))*")


def extract_data(file_contents: str) -> list[Music]:
    sections: list[Music] = []
    current_section = Music(title="", artist="")

    for line in file_contents.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("##"):
            heading = line.lstrip("##").lstrip()
            title, artist = heading.rsplit("-", maxsplit=1)
            current_section = Music(title=title.strip(), artist=artist.strip())
            sections.append(current_section)
        elif (url := line.lower()).startswith("link:"):
            url = url.lstrip("link:").lstrip()
            current_section.url = url
        elif line.startswith("-"):
            part = line.lstrip("-").lstrip()
            if part.startswith("extra:"):
                music_part = MusicPart(
                    start="", end="", typ="extra", extra=part.lstrip("extra:").lstrip()
                )
                current_section.parts.append(music_part)
                continue

            match = _PART_RE.match(part)
            if match is None:
                raise Exception(f"Invalid part: {part}")
            typ = match.group(1)
            start = match.group(2)
            end = match.group(3)
            extra = match.group(4)
            music_part = MusicPart(start=start, end=end, typ=typ, extra=extra)
            current_section.parts.append(music_part)

    return sections


def main():
    filename = sys.argv[1]
    with open(filename) as f:
        contents = f.read()

    sections = extract_data(contents)
    pprint(sections)


if __name__ == "__main__":
    main()
