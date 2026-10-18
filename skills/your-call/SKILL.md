---
name: your-call
description: Reply to an agent's question with "you decide": it makes the call itself and keeps working.
disable-model-invocation: true
---

# Your call

You just asked the user something: which option, which approach, whether to go
ahead, what they prefer. They answered: _your call_. They expect you to judge it
at least as well as they would, because the code and the context are in front of
you. Make the decision, own it, and keep the work moving.

## Scope

The call covers every decision open in your last message. Text after the
invocation steers it: a named exception ("except the naming") stays with the
user, a constraint ("keep it cheap") binds your choices, and "rest" hands you
every later decision in this task too, so decide those as they come up instead
of asking.

The call delegates _decisions_, not _permissions_. An action that cannot be
undone or that reaches outside the workspace (deleting data, force-pushing,
publishing, sending messages, spending money) keeps the confirmation it already
needed: get it ready, then ask for that one go-ahead.

## Deciding

Take each decision in turn:

1. If you already gave a recommendation, adopt it, unless something you learned
   since then outweighs it.
2. Otherwise ground the choice in evidence: the code, the project's conventions,
   and what the user has said earlier in this conversation. Look facts up rather
   than guessing at them. Break ties toward what is easier to reverse, then what
   the project already does, then what is simpler.
3. When evidence is thin and the choice is expensive to reverse, take the option
   that keeps the others open, and flag it.

## Reply

Lead with the decisions, one line each: what was decided, your choice, the
reason. Mark close calls and one-way doors with ⚠️ so the user can overrule them
at a glance. Then resume the work that was waiting on the answer.

When the question was one round of a series (an interview, a review, a
step-by-step plan), record your choices as settled and continue the series.
Under "rest", answer the remaining rounds yourself and close with the full set
of decisions.

Done when every decision in scope has a stated choice and a reason, and the work
that was blocked on it is moving again.
