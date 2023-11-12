<script lang="ts">
	import origMusics from '../music.json';
	import { Music, MusicPart } from '$lib/types';

	const allMusics: Music[] = origMusics.map((orig, index) => new Music(index, orig));
	const allArtists: string[] = Array.from(new Set(allMusics.map((music) => music.artist))).sort(
		(a, b) => a.localeCompare(b)
	);

	function getInitialParts() {
		return allMusics.map((music) => music.getParts()).flat();
	}
	let parts: MusicPart[] = getInitialParts();

	let musics: Music[] = allMusics;

	let loading = false;

	function updateMusicParts() {
		loading = true;
		let lastMusic: Music | null = null;
		const foundMusics: Music[] = [];
		for (const part of parts) {
			if (lastMusic !== null && lastMusic.id === part.music.id) {
				lastMusic.addPart(part);
			} else {
				if (lastMusic !== null) {
					foundMusics.push(lastMusic);
				}
				lastMusic = part.music.copy();
				lastMusic.setParts([part]);
			}
		}
		if (lastMusic !== null) {
			foundMusics.push(lastMusic);
		}
		musics = foundMusics;
		console.log('new musics', musics);
		loading = false;
	}

	let selectedArtist: string;
	let selectedSorting: string;

	function filterByArtist(initialParts: MusicPart[], artist: string) {
		if (artist === 'select-artist') {
			parts = initialParts;
		} else {
			parts = initialParts.filter((part) => part.music.artist === artist);
		}
		return parts;
	}

	function sortBy(initialParts: MusicPart[], sorting: string) {
		if (sorting === 'default') {
			parts = initialParts;
		} else if (sorting === 'length') {
			parts = initialParts.sort((a, b) => b.length() - a.length());
		}
		return parts;
	}

	function updateFiltersSorting(selectedArtist: string, selectedSorting: string) {
		console.log('selection changed', selectedArtist, selectedSorting);
		if (selectedArtist === undefined) {
			return;
		}

		const initialParts = getInitialParts();
		let newParts = initialParts;

		newParts = filterByArtist(newParts, selectedArtist);
		sortBy(newParts, selectedSorting);

		updateMusicParts();
	}

	$: {
		updateFiltersSorting(selectedArtist, selectedSorting);
	}

	console.log(musics);
</script>

<h1 class="text-xl font-bold p-2">Guitar Music</h1>

<div class="flex flex-row mt-2">
	<div class="ml-4">
		<select class="p-1" name="artist" id="artist-dropdown" bind:value={selectedArtist}>
			<option value="select-artist">-Select Artist-</option>
			{#each allArtists as artist}
				<option value={artist}>{artist}</option>
			{/each}
		</select>
	</div>

	<div class="ml-4">
		<select class="p-1" name="sorting" id="sorting-dropdown" bind:value={selectedSorting}>
			<option value="default">No sorting</option>
			<option value="length">Length</option>
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
		{#each musics as music (music.key)}
			<tr>
				<td rowspan={music.numParts() + 1} class="border-black border-r-2 text-center"
					><h2 class="py-2 px-4 text-lg">
						{music.title}
					</h2></td
				>
				<td rowspan={music.numParts() + 1} class="border-black border-r-2 text-center"
					><h2 class="py-2 px-4 text-lg">
						{music.artist}
					</h2></td
				>
			</tr>

			{#each music.getParts() as part, index ((music.id, part.id))}
				<tr class="border-black" class:border-b-2={index === music.numParts() - 1}>
					<td class="border-black border-b-2 text-center">{part.typ} {part.extra}</td>
					<td class="border-black border-b-2 text-center">{part.lengthPretty()}</td>
					<td class="border-black border-b-2"
						><audio controls preload="none" src="/{part.filename}" /></td
					>
				</tr>
			{/each}
		{/each}
	</table>
</div>

<div />
