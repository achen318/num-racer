import type { Room } from '../types';
import { apiRequest } from '../index';

export async function getRooms(): Promise<Room[]> {
	return apiRequest<Room[]>('/rooms');
}

export async function createRoom(): Promise<Room> {
	return apiRequest<Room>('/rooms', {
		method: 'POST'
	});
}

export async function getRoom(roomId: number): Promise<Room> {
	return apiRequest<Room>(`/rooms/${roomId}`);
}

export async function deleteRoom(roomId: number): Promise<void> {
	return apiRequest<void>(`/rooms/${roomId}`, {
		method: 'DELETE'
	});
}

export async function joinRoom(roomId: number, player: string): Promise<Room> {
	return apiRequest<Room>(`/rooms/join?room_id=${roomId}&player=${player}`, {
		method: 'POST'
	});
}

export async function leaveRoom(roomId: number, player: string): Promise<Room> {
	return apiRequest<Room>(`/rooms/leave?room_id=${roomId}&player=${player}`, {
		method: 'POST'
	});
}

export async function startGame(roomId: number): Promise<Room> {
	return apiRequest<Room>(`/rooms/start?room_id=${roomId}`, {
		method: 'POST'
	});
}
