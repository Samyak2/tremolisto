<script lang="ts">
	import origMusics from '../music.json';
	import { Music, MusicPart } from '$lib/types';

	const allMusics: Music[] = origMusics.map((orig, index) => new Music(index, orig));
	const allArtists: string[] = Array.from(new Set(allMusics.map((music) => music.artist))).sort(
		(a, b) => a.localeCompare(b)
	);

	let parts: MusicPart[] = allMusics.map((music) => music.parts).flat();

	let musics: Music[] = allMusics;

	let loading = false;

	$: {
		loading = true;
		const foundMusics: Map<number, Music> = new Map();
		for (const part of parts) {
			const foundMusic = foundMusics.get(part.music.id);
			if (foundMusic) {
				foundMusic.parts.push(part);
			} else {
				const music = { ...part.music };
				music.parts = [part];
				foundMusics.set(part.music.id, music);
			}
		}
		musics = Array.from(foundMusics.values());
		loading = false;
	}

	function filterByArtist(
		e: Event & {
			currentTarget: HTMLSelectElement;
		}
	) {
		const artist = e.currentTarget.value;
		if (artist === 'select-artist') {
			parts = allMusics.map((music) => music.parts).flat();
		} else {
			parts = allMusics
				.filter((music) => music.artist === artist)
				.map((music) => music.parts)
				.flat();
		}
	}

	console.log(musics);
</script>

<h1 class="text-xl font-bold p-2">Guitar Music</h1>

<div class="flex flex-row mt-2">
	<div class="ml-4">
		<select name="artist" id="artist-dropdown" on:input={filterByArtist}>
			<option value="select-artist">-Select Artist-</option>
			{#each allArtists as artist}
				<option value={artist}>{artist}</option>
			{/each}
		</select>
	</div>
</div>

{#if loading}
	<p>Loading...</p>
{/if}

<div class="sm:px-4 mt-4">
	<table class="border-black border-2 w-full">
		<colgroup>
			<col />
			<col />
			<col class="w-40" />
			<col class="w-20" />
			<col />
		</colgroup>
		<tr class="border-black border-2">
			<th class="border-black border-2">Song</th>
			<th class="border-black border-2">Artist</th>
			<th class="border-black border-y-2">Type</th>
			<th class="border-black border-y-2">Length</th>
			<th class="border-black border-y-2">Audio</th>
		</tr>
		{#each musics as music (music.id)}
			<tr>
				<td rowspan={music.parts.length + 1} class="border-black border-r-2 text-center"
					><h2 class="py-2 px-4 text-lg">
						{music.title}
					</h2></td
				>
				<td rowspan={music.parts.length + 1} class="border-black border-r-2 text-center"
					><h2 class="py-2 px-4 text-lg">
						{music.artist}
					</h2></td
				>
			</tr>

			{#each music.parts as part, index ((music.id, part.id))}
				<tr class="border-black" class:border-b-2={index === music.parts.length - 1}>
					<td class="border-black border-b-2 text-center">{part.typ} {part.extra}</td>
					<td class="border-black border-b-2 text-center">{part.length()}s</td>
					<td class="border-black border-b-2"
						><audio controls preload="none" src="/{part.filename}" /></td
					>
				</tr>
			{/each}
		{/each}
	</table>
</div>

<div />
