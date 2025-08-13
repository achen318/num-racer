type DynamicRoutes = {
	"/rooms/[slug]": { slug: string }
};

type Layouts = {
	"/": { slug?: string };
	"/rooms": { slug?: string };
	"/rooms/[slug]": { slug: string }
};

export type RouteId = "/" | "/rooms" | "/rooms/[slug]";

export type RouteParams<T extends RouteId> = T extends keyof DynamicRoutes ? DynamicRoutes[T] : Record<string, never>;

export type LayoutParams<T extends RouteId> = Layouts[T] | Record<string, never>;

export type Pathname = "/" | "/rooms" | `/rooms/${string}` & {};

export type ResolvedPathname = `${"" | `/${string}`}${Pathname}`;

export type Asset = "/robots.txt";