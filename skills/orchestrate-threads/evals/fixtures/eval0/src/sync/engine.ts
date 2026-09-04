// Bidirectional sync between WatermelonDB and Convex.
// Known problem: pullChanges and pushChanges share mutable cursor state and
// three retry paths, each with its own backoff. ~600 lines in the real app.
export async function pullChanges(lastPulledAt: number) { /* ... */ }
export async function pushChanges(changes: unknown) { /* ... */ }
export async function retryWithBackoff(fn: () => Promise<void>) { /* ... */ }
