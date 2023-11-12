import lodash from 'lodash';

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
	private parts: MusicPart[];
	key: string;

	constructor(index: number, orig: OrigMusic) {
		this.id = index;
		this.title = orig.title;
		this.artist = orig.artist;
		this.url = orig.url;
		this.parts = orig.parts.map((part, index) => new MusicPart(this.copy(), index, part));
		this.key = this.computeKey();
	}

	computeKey(): string {
		return `${this.id}-${this.parts.map((part) => part.id).join(',')}`;
	}

	numParts(): number {
		return this.parts.length;
	}

	getParts(): MusicPart[] {
		return [...this.parts];
	}

	setParts(parts: MusicPart[]) {
		this.parts = parts;
		this.key = this.computeKey();
	}

	addPart(part: MusicPart) {
		this.parts.push(part);
		this.key = this.computeKey();
	}

	copy(): Music {
		return lodash.cloneDeep(this);
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

	startSeconds() {
		return this.timeToSeconds(this.start);
	}

	endSeconds() {
		return this.timeToSeconds(this.end);
	}

	length() {
		return this.endSeconds() - this.startSeconds();
	}

	lengthPretty() {
		const length = this.length();
		if (length >= 60) {
			const mins = Math.trunc(length / 60);
			const secs = length % 60;
			return `${mins}m ${secs}s`;
		} else {
			return `${length}s`;
		}
	}
}
