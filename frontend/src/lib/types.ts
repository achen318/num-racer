enum Operation {
	ADD = '+',
	SUB = '-',
	MUL = '*',
	DIV = '/'
}

export interface Problem {
	num1: number;
	num2: number;
	operation: Operation;
	result: number;
}

export interface OpBounds {
	bounds_1: [number, number];
	bounds_2: [number, number];
}

export interface MatchSettings {
	operations: Operation[];
	addBounds: OpBounds;
	mulBounds: OpBounds;
	duration: number;
}

export interface Player {
	name: string;
	score: number;
	currentProblem: Problem | null;
}

export interface MatchResult {
	winner: Player;
	finalScores: Map<string, number>;
}

export interface Match {
	players: Map<string, Player>;
	settings: MatchSettings;
	active: boolean;
	result: MatchResult | null;
}

export interface Room {
	id: string;
	host: Player | null;
	players: Map<string, Player>;
	settings: MatchSettings;
	match: Match | null;
}
