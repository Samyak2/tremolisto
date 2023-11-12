export interface OrigMusic {
	title: string;
	artist: string;

	url: string | null;
	parts: OrigMusicPart[];
}

export class Music {
	id: number;
	title: string;
	artist: string;
	url: string | null;
	parts: MusicPart[];

	constructor(index: number, orig: OrigMusic) {
		this.id = index;
		this.title = orig.title;
		this.artist = orig.artist;
		this.url = orig.url;
		this.parts = orig.parts.map((part, index) => new MusicPart({ ...this }, index, part));
	}
}

export interface OrigMusicPart {
	start: string;
	end: string;
	typ: string;
	extra: string;
	filename: string;
}

export class MusicPart {
	id: number;
	start: string;
	end: string;
	typ: string;
	extra: string;
	filename: string;
	music: Music;

	constructor(music: Music, index: number, orig: OrigMusicPart) {
		this.music = music;
		this.id = index;
		this.start = orig.start;
		this.end = orig.end;
		this.typ = orig.typ;
		this.extra = orig.extra;
		this.filename = orig.filename;
	}

	private timeToSeconds(time: string) {
		let [mins, secs] = time.split(':');
		return parseInt(mins) * 60 + parseInt(secs);
	}

	start_seconds() {
		return this.timeToSeconds(this.start);
	}

	end_seconds() {
		return this.timeToSeconds(this.end);
	}

	length() {
		return this.end_seconds() - this.start_seconds();
	}
}
