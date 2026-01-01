<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type { PageData } from './$types';

	export let data: PageData;
	const { room } = data;

	// let ws: WebSocket | null = null;

	onMount(() => {
		// ws = new WebSocket(`ws://localhost:8000/ws/Player ${Math.floor(Math.random() * 15)}`);
		console.log('Joining');
	});

	onDestroy(() => {
		// ws?.close();
		console.log('Leaving');
	});
</script>

<h1>Room {room.id}</h1>

<ul>
	{#each Object.values(room.players) as player}
		<li>{player.name}</li>
	{/each}
</ul>
