import re
import sys
from pprint import pprint

import audio
import yt
from models import Music, MusicPart

_LINK_RE = re.compile(r"^link:\s+", re.IGNORECASE)
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
        elif line.lower().startswith("link:"):
            url = _LINK_RE.sub("", line)
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
            music_part = MusicPart(start=start, end=end, typ=typ, extra=extra or "")
            current_section.parts.append(music_part)

    return sections


def process_audio(musics: list[Music]):
    for music in musics:
        if music.url is None:
            raise Exception(f"Could not find URL for: {music}")
        out = yt.get_audio_file(yt.AudioInput(url=music.url))

        for part in music.parts:
            if not part.has_time():
                continue

            cut_audio_out = audio.cut_audio(
                audio.CutAudioInput(filename=out.filename, part=part)
            )

            print(cut_audio_out)


def main():
    filename = sys.argv[1]
    with open(filename) as f:
        contents = f.read()

    sections = extract_data(contents)
    pprint(sections)

    process_audio(sections)


if __name__ == "__main__":
    main()
