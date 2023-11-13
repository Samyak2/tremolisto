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
	<table class="w-full">
		<colgroup>
			<col />
			<col />
			<col class="sm:w-40" />
			<col class="sm:w-20" />
			<col />
		</colgroup>
		<thead>
			<tr>
				<th class="border-primary-700 border-y-2">Song</th>
				<th class="border-primary-700 border-y-2 border-r-2">Artist</th>
				<th class="border-primary-700 border-y-2">Type</th>
				<th class="border-primary-700 border-y-2">Length</th>
				<th class="border-primary-700 border-y-2">Audio</th>
			</tr>
		</thead>
		<tbody>
			{#each musics as music (music.key)}
				<tr>
					<td data-th="" rowspan={music.numParts() + 1} class="border-primary-700 text-center"
						><span class="py-2 pl-4 md:px-4 text-xl font-bold">
							{music.title}
						</span></td
					>
					<td
						data-hyphen-before=""
						data-th=""
						rowspan={music.numParts() + 1}
						class="border-primary-700 md:border-r-2 text-center"
						><span class="py-2 pl-2 md:px-4 text-xl font-bold">
							{music.artist}
						</span></td
					>
				</tr>

				{#each music.getParts() as part, index ((music.id, part.id))}
					<tr
						class="border-primary-700 pl-2 md:pl-0 mb-2 md:mb-0"
						class:border-b-2={index === music.numParts() - 1}
					>
						<td data-th="" class="border-primary-700 md:border-b-2 text-center"
							>{part.typ} {part.extra}</td
						>
						<td
							data-hyphen-before=""
							data-th=""
							class="border-primary-700 md:border-b-2 text-center"
							><span class="pl-1 md:pl-0">{part.lengthPretty()}</span></td
						>
						<br class="block md:hidden" />
						<td data-th="" class="border-primary-700 md:border-b-2"
							><audio controls preload="none" src="/{part.filename}" /></td
						>
					</tr>
				{/each}
			{/each}
		</tbody>
	</table>
</div>

<style>
	/* ref: https://css-tricks.com/responsive-data-tables/ */
	/* 
Max width before this PARTICULAR table gets nasty
This query will take effect for any screen smaller than 760px
and also iPads specifically.
*/
	@media only screen and (max-width: 768px),
		(min-device-width: 768px) and (max-device-width: 1024px) {
		/* Force table to not be like tables anymore */
		table,
		thead,
		tbody,
		th,
		td,
		tr {
			display: block;
		}

		/* Hide table headers (but not display: none;, for accessibility) */
		thead tr {
			position: absolute;
			top: -9999px;
			left: -9999px;
		}

		tr {
			/* border: 1px solid #ccc; */
			text-align: center;
		}

		td {
			/* Behave  like a "row" */
			/* border: none; */
			/* border-bottom: 1px solid #eee; */
			/*
			position: relative;
			padding-left: 50%;
      */
			display: inline-flex;
			align-items: center;
		}

		td:before {
			/* Now like a table header */
			/* position: absolute; */
			/* Top/left values mimic padding */
			/*
			top: 6px;
			left: 6px;
			width: 45%;
			padding-right: 10px;
			white-space: nowrap;
      */
		}

		td[data-th]:before {
			content: attr(data-th);
		}

		td[data-hyphen-before]:before {
			content: '-';
		}
	}
</style>
