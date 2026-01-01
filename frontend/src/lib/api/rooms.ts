import type { Room } from '../types';
import { apiRequest } from '../index';

export async function getRoom(roomId: string, fetchFn: typeof fetch = fetch): Promise<Room> {
	return apiRequest<Room>(`/rooms/${roomId}`, {}, fetchFn);
}

export async function getRooms(fetchFn: typeof fetch = fetch): Promise<Room[]> {
	return apiRequest<Room[]>('/rooms', {}, fetchFn);
}

export async function createRoom(host: string, fetchFn: typeof fetch = fetch): Promise<string> {
	return apiRequest<string>(`/rooms?host=${host}`, { method: 'POST' }, fetchFn);
}

export async function deleteRoom(roomId: string, fetchFn: typeof fetch = fetch): Promise<void> {
	return apiRequest<void>(`/rooms/${roomId}`, { method: 'DELETE' }, fetchFn);
}

export async function addPlayer(
	roomId: string,
	player: string,
	fetchFn: typeof fetch = fetch
): Promise<boolean> {
	return apiRequest<boolean>(`/rooms/add/${roomId}?player=${player}`, { method: 'POST' }, fetchFn);
}

export async function removePlayer(
	roomId: string,
	player: string,
	fetchFn: typeof fetch = fetch
): Promise<void> {
	return apiRequest<void>(`/rooms/remove/${roomId}?player=${player}`, { method: 'POST' }, fetchFn);
}

export async function startMatch(roomId: string, fetchFn: typeof fetch = fetch): Promise<void> {
	return apiRequest<void>(`/rooms/start/${roomId}`, { method: 'POST' }, fetchFn);
}

export async function endMatch(roomId: string, fetchFn: typeof fetch = fetch): Promise<void> {
	return apiRequest<void>(`/rooms/end/${roomId}`, { method: 'POST' }, fetchFn);
}

export async function handleAnswer(
	roomId: string,
	player: string,
	answer: number,
	fetchFn: typeof fetch = fetch
): Promise<boolean> {
	return apiRequest<boolean>(
		`/rooms/answer/${roomId}?player=${player}&answer=${answer}`,
		{ method: 'POST' },
		fetchFn
	);
}
