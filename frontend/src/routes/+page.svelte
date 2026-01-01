<script lang="ts">
	import { goto } from '$app/navigation';
	import { createRoom, addPlayer } from '$lib/api/rooms';

	let name = $state<string>('');
	let room = $state<string>('');

	// ws.onmessage = (event) => {
	// 	const data = JSON.parse(event.data);

	// 	if (data.type === 'room_update' && currentRoom && currentRoom.id === data.roomId) {
	// 		currentRoom.players = data.players;
	// 	}
	// };

	async function handleCreateRoom() {
		try {
			const roomId = await createRoom(name);
			goto(`/rooms/${roomId}`);
		} catch (error) {
			console.error(`Failed to create room. ${error.message}`);
		}
	}

	async function handleJoinRoom() {
		try {
			await addPlayer(room, name);

			// ws.send(
			// 	JSON.stringify({
			// 		type: 'room_update',
			// 		roomId: currentRoom.id,
			// 		playerName: name,
			// 		players: currentRoom.players
			// 	})
			// );

			goto(`/rooms/${room}`);
		} catch (error) {
			console.error(`Failed to join room. ${error.message}`);
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
