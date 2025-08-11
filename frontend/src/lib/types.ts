export interface Player {
    name: string;
}

export interface Match {
    status: string;
}

export interface Room {
    id: number;
    players: Player[];
    match : Match | null;
}
