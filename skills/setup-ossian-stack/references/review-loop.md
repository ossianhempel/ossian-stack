# Review standards and evals

Read when setting up a project, after step 6. Follow the scope and safety contract in the skill entry point.

`learn-from-miss` turns each caught mistake into a guardrail. Two of its outputs live in project files that most repos do not have yet. Offer both once; create them only on a yes.

## `CODING_STANDARDS.md`

The reviewer's standing brief. `autoreview` reads it from the repository root on every review, because its reviewer runs isolated and never sees the project's agent instructions. It holds judgment rules only: what a reviewer must check that no lint or type can.

Unlike `GLOSSARY.md`, this file is created up front: the reviewer reads it whether or not it exists, and a stated purpose tells the next agent where review rules go. Seed it with the judgment rules the project already states (in its agent instructions, contributing guide, or docs), each moved rather than copied, so one rule keeps one home. Leave mechanical rules to the project's linter. With nothing to seed, write the header alone:

```markdown
# Coding standards

Judgment rules for code review. The reviewer reads this file on every review.
Mechanical rules belong in the linter or CI, not here. Each rule is general
(it names the pattern, never one case) and comes from a real miss; its eval
case in `evals/cases/` proves the reviewer catches it.
```

## `evals/`

Regression cases for agent behaviour, one per miss whose fix was prose. Create:

- `evals/README.md`:

  ```markdown
  # Evals

  Regression cases for agent behaviour. Each case in `cases/` is a real miss: a
  mistake an agent made that a human caught. A case replays the state where the
  miss should have been caught and checks that the agent now catches or avoids it.
  Add a case whenever an instruction, standard, or skill is changed to fix a miss;
  the case must fail before the change and pass after it. Replay results go to
  `results/`, which is not committed.
  ```

- `evals/cases/` with a `.gitkeep`.
- `evals/results/` in the project's `.gitignore`.

Report what you created. Never invent standards or cases to fill the files.
