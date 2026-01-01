import type { PageLoad } from './$types';
import { getRoom } from '$lib/api/rooms';

export const load: PageLoad = async ({ fetch, params }) => {
	const room = await getRoom(params.slug, fetch);
	return { room };
};
