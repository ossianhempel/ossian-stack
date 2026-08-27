---
name: grill-me
description: Grill the user relentlessly about a plan, decision, or idea until shared understanding. Use when the user wants to stress-test a plan or design, or mentions "grill me", "grill this", or "grilling".
disable-model-invocation: true
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask *now* without guessing at answers you have not heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>
➡️ <your recommended answer>
```

Each round the user's answers reshape the tree — settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding *facts* is the agent's job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), look it up rather than asking the user for something you could verify yourself. The *decisions* are the user's — put each to them and wait.

Do not act on it until I confirm we have reached a shared understanding.
