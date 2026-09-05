# Demo Data

Read for missing or inadequate marketing seed data. Follow the scope and safety contract in the skill entry point.

## Creating a Demo Data Seeder

If the app has no existing demo data mechanism, create one. Place it in `<AppName>/Debug/DemoDataSeeder.swift`, wrapped in `#if DEBUG`.

Guidelines:
- Seed **enough data that every captured screen looks populated**. Audit the screen list against the seed.
- Use realistic content: real place names, plausible numbers, varied states (some items "running low", some "fresh", some with images, some without).
- If the app uses SwiftData, write directly to the `ModelContext`. If Core Data, use the managed object context. If a REST backend, seed via the local cache/store layer.
- Make seeding **idempotent** — check if data already exists before inserting. The store persists across simulator relaunches, and re-seeding per locale causes CloudKit sync churn and crashes.
- Include enough variety to fill different UI states: empty states should NOT appear unless they're a marketing screen.

Minimal shape:
```swift
#if DEBUG
enum DemoDataSeeder {
    static func seedIfEmpty(in context: ModelContext) {
        let existing = (try? context.fetchCount(FetchDescriptor<Item>())) ?? 0
        guard existing == 0 else { return }

        // Items with varied states
        let items = [
            Item(name: "...", status: .active, ...),
            Item(name: "...", status: .lowStock, ...),
            // ...enough to fill every screen
        ]
        items.forEach { context.insert($0) }
        try? context.save()
    }
}
#endif
```
