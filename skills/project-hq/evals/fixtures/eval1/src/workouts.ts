export type Workout = { id: string; date: string; sets: { exercise: string; reps: number; kg: number }[] };
export function listWorkouts(): Workout[] { return []; }
