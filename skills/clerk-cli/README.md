# clerk-cli

Vendored from [clerk/skills](https://github.com/clerk/skills) (`skills/core/clerk-cli`).

Operational guidance for the `clerk` CLI: auth, users, orgs, env keys, instance
config, impersonation, webhooks, deploy verification, and ad-hoc API calls.
Pairs with other Clerk skills in that repo (`clerk-setup`, `clerk-orgs`,
`clerk-billing`, etc.) when you need framework or feature depth.

**CLI requirement:** targets `clerk@latest` (currently 2.x). Upgrade globally:

```bash
npm i -g clerk@latest
clerk --version
```

To update this skill:

```bash
npx skills add clerk/skills -y --skill clerk-cli
cp -R .agents/skills/clerk-cli/* skills/clerk-cli/
```

Note: `clerk skill install` only exists in Clerk CLI 1.x. On 2.x+, use
`npx skills add clerk/skills` as above.
