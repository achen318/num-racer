<script lang="ts">
	import { createRoom, joinRoom } from '$lib/api/rooms';
	import type { Room } from '$lib/types';
	import { nonpassive } from 'svelte/legacy';

	let name = $state<string>('');
	let room = $state<string>('');
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

			ws.send(
				JSON.stringify({
					type: 'room_update',
					roomId: currentRoom.id,
					playerName: name,
					players: currentRoom.players
				})
			);
		} catch (error) {
			console.error(`Failed to join room: ${error}`);
		}
	}

	const ws = new WebSocket(`ws://localhost:8000/ws/Player ${Math.floor(Math.random() * 15)}`);
	let message = $state<string>('');
	let messages = $state<string[]>([]);

	function sendMessage() {
		ws.send(
			JSON.stringify({
				type: 'public_chat_message',
				playerName: name,
				message: message
			})
		);
		message = '';
	}

	ws.onmessage = (event) => {
		const data = JSON.parse(event.data);

		if (data.type === 'room_update' && currentRoom && currentRoom.id === data.roomId) {
			currentRoom.players = data.players;
		} else if (data.type === 'public_chat_message') {
			messages.push(`${data.playerName}: ${data.message}`);
		}
	};
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

<div>
	<h1>WebSocket Chat</h1>
	<input type="text" name="message" bind:value={message} />
	<button onclick={sendMessage}>Send</button>

	<ul>
		{#each messages as msg}
			<li>{msg}</li>
		{/each}
	</ul>
</div>
