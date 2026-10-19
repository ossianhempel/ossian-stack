# Prior conversation

**User:** Add input validation to the `POST /api/recipes` endpoint in `apps/server/src/routes/recipes.ts`.

**Assistant:** Before I start, how would you like validation done?

- **A)** Use `zod` (already a dependency; `apps/server/src/routes/users.ts` and `apps/server/src/routes/auth.ts` validate with `z.object(...)` schemas)
- **B)** Add `valibot`, which is smaller
- **C)** Hand-roll checks inline

And should invalid requests return `400` with a list of field errors, or just a generic `400 Bad Request`?

# User's reply now
