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

<h1 class="text-xl font-bold">Guitar Music</h1>

<select name="artist" id="artist-dropdown" on:input={filterByArtist}>
	<option value="select-artist">-Select Artist-</option>
	{#each allArtists as artist}
		<option value={artist}>{artist}</option>
	{/each}
</select>

{#if loading}
  <p>Loading...</p>
{/if}

<table class="border-black border-2">
	<colgroup>
		<col class="w-1/2" />
		<col class="w-20" />
		<col />
	</colgroup>
	<tr class="border-black border-2">
		<th class="border-black border-2">&nbsp;</th>
		<th class="border-black border-2">Length</th>
		<th class="border-black border-2">Audio</th>
	</tr>
	{#each musics as music (music.id)}
		<tr>
			<td colspan="3"
				><h2 class="text-lg">
					{music.title} - {music.artist}
				</h2></td
			>
		</tr>

		{#each music.parts as part, index ((music.id, part.id))}
			<tr class="border-black" class:border-b-2={index === music.parts.length - 1}>
				<td>{part.typ} {part.extra}</td>
				<td>{part.length()}s</td>
				<td><audio controls preload="none" src="/{part.filename}" /></td>
			</tr>
		{/each}
	{/each}
</table>

<div />
