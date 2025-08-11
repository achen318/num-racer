<script lang="ts">
	import { createRoom, joinRoom } from '$lib/api/rooms';
	import type { Room } from '$lib/types';

	let name = $state('');
	let room = $state('');
	let currentRoom = $state<Room | null>(null);

	async function handleCreateRoom() {
		try {
			currentRoom = await createRoom();
			room = currentRoom.id.toString();
		} catch (error) {
			console.error(`Failed to create room: ${error}`);
		}
	}

	async function handleJoinRoom() {
		try {
			currentRoom = await joinRoom(parseInt(room), name);
		} catch (error) {
			console.error(`Failed to join room: ${error}`);
		}
	}
</script>

<div>
	<label for="name">Display Name:</label>
	<input type="text" name="name" bind:value={name} />
</div>

<div>
	<label for="room">Room Code:</label>
	<input type="text" name="room" bind:value={room} />
</div>

<div>
	<button onclick={handleCreateRoom}>Create Room</button>
	<button onclick={handleJoinRoom}>Join Room</button>
</div>

{#if currentRoom}
	<div>
		<h1>Room {currentRoom.id}</h1>
		<ul>
			{#each currentRoom.players as player}
				<li>{player.name}</li>
			{/each}
		</ul>
	</div>
{/if}
