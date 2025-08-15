<script lang="ts">
	import type { PageProps } from './$types';
	import { onMount, onDestroy } from 'svelte';

	let { data }: PageProps = $props();
	let ws: WebSocket | null = null;

	onMount(() => {
		// ws = new WebSocket(`ws://localhost:8000/ws/rooms/${data.roomId}`);
		console.log('Joining');
	});

	onDestroy(() => {
		// ws?.close();
		console.log('Leaving');
	});
</script>

<h1>{data.roomId}</h1>
