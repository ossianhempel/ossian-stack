# Prior conversation

**User:** Clean up the price formatting in `src/lib/` and tidy the branch history before I open the PR.

**Assistant:** I found three ad-hoc price formatters in `src/lib/cart.ts`, `src/lib/checkout.ts`, and `src/lib/receipt.ts`. The project already has `src/lib/format.ts` exporting `formatDate` and `formatDuration`. Two questions:

1. Should the consolidated helper be named `formatPrice` (in `format.ts`) or `toCurrency` (in a new `currency.ts`)?
2. The branch `feat/checkout-polish` has 14 WIP commits, already pushed to origin. Should I squash them into one and force-push?

# User's reply now
