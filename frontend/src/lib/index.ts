const API_BASE = 'http://localhost:8000';

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}, fetchFn: typeof fetch = fetch): Promise<T> {
	const url = `${API_BASE}${endpoint}`;

	const res = await fetchFn(url, options);

	if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);

	return res.json();
}
