# tremolisto

Source code for the processing and the UI of https://tremolisto.samyak.me/

Does not include the actual list.

## Usage

### Requirements

If you have nix (with flakes enabled), simply run:
```bash
nix develop
```

If you do not have nix:
- [just](https://github.com/casey/just).
- A python 3.11 virtual environment (ensure that it's activated before running the following commands).
- Node JS (tested with 21).

### Install dependencies

```bash
just setup
```

### Music list

The music list should be a markdown file in the following format:

```markdown
## Song1 - Artist1
Link: https://music.youtube.com/watch?v=qqqqqqqqqqq
- intro: 0:00 - 0:15
- solo: 2:30 - 4:30
- outro: 5:30 - 6:01
## Song2 - Artist2
Link: https://music.youtube.com/watch?v=qqqqqqqqqqq
- intro: 0:00 - 0:15
- solo: 2:30 - 4:30
- outro: 5:30 - 6:01
```

Create `.env` file with the following:
```env
MUSIC_LIST_FILE="/path/to/music-list.md
```

### Build

```bash
just build
```

This will retrieve the audio, cut it up in the sections specified and then build the website with that data.

The built website is in `ui/build/`. This is a static site. So the whole directory can simply be uploaded to any static site hosting provider.

To deploy through netlify, use `just deploy` (may need some more steps to set up).

## Code structure

The processing code is scattered in a bunch of python modules:
- `extractor.py`: main script which parses the music list markdown file, downloads audio and cuts it up into parts. To be invoked as a script: `python extractor.py /path/to/music-list.md`.
- `yt.py`: downloader.
- `audio.py`: uses pydub to cut audio.
- `cache.py`: decorator to cache the outputs of a function in a json file. Used to cache downloading and processing functions.
- `models.py`: pydantic models used across the other files.

The frontend is in [ui](/ui).
