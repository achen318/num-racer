<script lang="ts">
	import { onMount } from 'svelte';
	import { getRoom } from '$lib/api/rooms';
	// import type { Room } from '$lib/types';

	// let room: Room | null = null;
	let room = null;

	onMount(async () => {
		const response = await getRoom($slug);
		room = response.data;
	});
</script>

<h1>
	Room {room.id}
</h1>
