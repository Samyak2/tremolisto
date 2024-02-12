<script lang="ts">
	import origMusics from '../music.json';
	import { Music, MusicPart } from '$lib/types';
	import Select from 'svelte-select';

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

	let selectedArtist: string = '';

	type SortingType = `${string};${'desc' | 'asc'}`;
	const sortingOptions: { value: SortingType; label: string }[] = [
		{ value: 'input-order;desc', label: 'Newly added' },
		{ value: 'input-order;asc', label: 'Oldest added' },
		{ value: 'length;desc', label: 'Longest' },
		{ value: 'length;asc', label: 'Shortest' }
	];
	let selectedSorting: SortingType | null = sortingOptions[0].value;

	function filterByArtist(initialParts: MusicPart[], artist: string) {
		if (artist === '' || artist === null || artist === undefined) {
			parts = initialParts;
		} else {
			parts = initialParts.filter((part) => part.music.artist === artist);
		}
		return parts;
	}

	function inputOrderReverseSorter(a: MusicPart, b: MusicPart): number {
		if (a.music.id === b.music.id) {
			// correct order within a music: parts listed as they were obtained
			return a.id - b.id;
		} else {
			// reverse order of music: show newly added first
			return b.music.id - a.music.id;
		}
	}

	function sortBy(initialParts: MusicPart[], sortingStr: SortingType | null) {
		const sorting = sortingStr?.split(';', 2);

		if (sorting === null || sorting === undefined) {
			parts = [...initialParts].sort(inputOrderReverseSorter);
		} else if (sorting[0] === 'input-order') {
			if (sorting[1] === 'asc') {
				parts = initialParts;
			} else {
				parts = [...initialParts].sort(inputOrderReverseSorter);
			}
		} else if (sorting[0] === 'length') {
			parts = initialParts.sort((a, b) =>
				sorting[1] === 'desc' ? b.length() - a.length() : a.length() - b.length()
			);
		}
		return parts;
	}

	function updateFiltersSorting(selectedArtist: string, selectedSorting: SortingType | null) {
		console.log('selection changed', selectedArtist, selectedSorting);

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

<div class="flex justify-center">
	<div class="md:w-[80rem]">
		<h1 class="text-xl font-bold p-2">Guitar Music</h1>

		<div class="text-primary-100 ml-4 max-w-[50rem]">
			<details>
				<summary class="cursor-pointer">faq</summary>

				<div class="grid grid-cols-[1.2rem_1fr]">
					<div class="text-primary-700">q:</div>
					<div>what is it?</div>
					<div class="text-primary-700">a:</div>
					<div class="mb-2">
						a list of songs with the parts of them that use guitar. mostly electric guitar solos,
						but includes riffs, acoustic guitar and rhythm guitar too.
					</div>

					<div class="text-primary-700">q:</div>
					<div>what do the "Type"s means?</div>
					<div class="text-primary-700">a:</div>
					<div>
						<ul class="list-disc ml-4">
							<li><span class="font-bold">solo:</span> a guitar solo, or a short riff</li>
							<li>
								<span class="font-bold">intro:</span> a guitar solo or a riff that's a part of the song's
								beginning
							</li>
							<li>
								<span class="font-bold">outro:</span> a guitar solo or a riff that's a part of the song's
								ending
							</li>
							<li><span class="font-bold">background:</span> guitar that appears behind vocals</li>
							<li>
								<span class="font-bold">multo:</span> a word I made up to mean multiple guitars or a
								guitar accompanied by other instruments
							</li>
						</ul>
					</div>
				</div>
			</details>
		</div>

		<div class="flex flex-row flex-wrap mt-2 mr-4">
			<div class="ml-4 w-64 mb-2">
				<Select
					placeholder="Select artist"
					items={allArtists.map((artist) => {
						return { value: artist, label: artist };
					})}
					class="bg-primary-900 text-primary-50"
					bind:justValue={selectedArtist}
					inputStyles="cursor: pointer;"
					containerStyles="cursor: pointer;"
					listAutoWidth={false}
				/>
			</div>

			<div class="ml-4 w-64">
				<Select
					placeholder="No sorting"
					value={selectedSorting}
					items={sortingOptions}
					class="bg-primary-900 text-primary-50"
					bind:justValue={selectedSorting}
					inputStyles="cursor: pointer;"
					containerStyles="cursor: pointer;"
				/>
			</div>
		</div>

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
						<tr class="px-2">
							<td
								data-th=""
								rowspan={music.numParts() + 1}
								class="border-primary-700 text-center py-2 md:px-4"
								><span class="text-xl font-bold">
									{music.title}
								</span></td
							>
							<td
								data-hyphen-before=""
								data-th=""
								rowspan={music.numParts() + 1}
								class="border-primary-700 md:border-r-2 text-center py-2 md:pl-2 md:px-4"
								><span class="text-xl font-bold pl-2 md:pl-0">
									{music.artist}
								</span></td
							>
						</tr>

						{#each music.getParts() as part, index ((music.id, part.id))}
							<tr
								class="border-primary-700 mb-2 md:mb-0"
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
								<td data-th="" class="border-primary-700 md:border-b-2 w-full md:w-[50%]"
									><audio
										class="w-full min-w-[300px]"
										controls
										preload="none"
										src="/{part.filename}"
									/></td
								>
							</tr>
						{/each}
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>

<style>
	/* ref: https://css-tricks.com/responsive-data-tables/ */
	/* 
Max width before this PARTICULAR table gets nasty
This query will take effect for any screen smaller than 760px
and also iPads specifically.
*/
	@media (max-width: 768px) {
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
			text-align: center;
		}

		td {
			display: inline-flex;
			align-items: center;
		}

		td[data-th]:before {
			content: attr(data-th);
		}

		td[data-hyphen-before]:before {
			content: '-';
		}
	}
</style>
