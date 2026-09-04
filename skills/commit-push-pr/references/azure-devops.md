# Azure DevOps Services PR lifecycle

This reference replaces the GitHub forge commands in the main skill and its PR
mode description reference. Keep the common branch safety, commit/push, description
writing, narrower modes, and default follow-through contract.

Resolve organization, project and repository from the explicit Services URL, else
the selected remote and existing project configuration. Read configuration only;
never change global defaults. Services remotes include dev.azure.com,
ORG.visualstudio.com, and git@ssh.dev.azure.com:v3/ORG/PROJECT/REPO. Decode URL
components when passing them as CLI arguments; encode each component when building
URLs. A bare PR ID cannot establish organization or repository. Report conflicting
identity; do not probe guessed organizations or run gh against Azure. Custom Azure
DevOps Server hosts are outside this supported path.

## Find the current PR

Use explicit arguments rather than ambient Azure CLI defaults:

```bash
az repos pr list --organization "<org-url>" --project "<project>" --repository "<repository>" --source-branch "<source-branch>" --status active --detect false --output json
```

Zero results is NO_OPEN_PR; command failure is a blocker. Multiple matches need an
exact selection, not the first result. Verify repository.id/name and
repository.project.id/name, sourceRefName, targetRefName, pullRequestId, status and
isDraft. Preserve the existing target branch unless an authorized --base changes it.

For an explicit PR, `az repos pr show --organization "<org-url>" --id <id>
--detect false --output json` supplies metadata; verify its returned project and
repository against the requested identity before using or updating it. Its title,
description, sourceRefName and targetRefName replace GitHub's PR-mode fields. If it
is not active, report and stop. Read the appropriate local Git diff against that
target to compose the description; no gh fetch is involved.

## Create or update

Azure's description CLI argument is text, not GitHub's body-file option. Pass the
UTF-8 file content as a single subprocess argument. For creation, the command shape
is below; populate values from the verified identity and completed branch state.
Do not paste untrusted text into executable Python or shell source.

```python
import json, subprocess
from pathlib import Path
# spec is a JSON file written as data: org, project, repository, source, target,
# title, body_file, draft. It contains no credentials.
spec = json.loads(Path("<prepared-spec-file>").read_text())
result = subprocess.run([
    "az", "repos", "pr", "create", "--organization", spec["org"],
    "--project", spec["project"], "--repository", spec["repository"],
    "--source-branch", spec["source"], "--target-branch", spec["target"],
    "--title", spec["title"], "--description", Path(spec["body_file"]).read_text(),
    "--draft", str(spec["draft"]).lower(), "--detect", "false", "--output", "json"
], check=True, capture_output=True, text=True)
print(result.stdout)
```

Existing PR updates use the same argv/file-content technique with `az repos pr
update --organization <org-url> --id <verified-id> --title <title> --description
<body-text> --detect false --output json`. Apply the main skill's preview/authorization
rule. The update CLI does not expose --target-branch. For an explicitly authorized base
change outside a babysitter's no-retarget scope, use PR Update REST PATCH with only
`{"targetRefName":"refs/heads/<target>"}` in a prepared JSON file:

```bash
az devops invoke --organization "<org-url>" --area git --resource pullRequests --route-parameters "project=<project>" "repositoryId=<repository-id>" "pullRequestId=<pr-id>" --http-method PATCH --api-version 7.1 --in-file "<json-file>" --detect false --output json
```

Read back targetRefName afterward. Preserve drafts; metadata-only calls never push or
start an independent drive. Never set status completed, auto-complete, bypass-policy,
reviewer votes, or delete-source-branch flags.

Read back the created/updated PR and verify identity, head/source, target, draft
state, and description before reporting. Construct the full Services PR URL from
that verified organization/project/repository/ID, encoding each component. For a
normal completed non-draft delivery, invoke `babysit` with that URL, drive outcome,
and inherited action scope. Azure follows the same lifecycle as GitHub: finish any
agreed stack build first and resume an existing drive owner rather than starting a
second one. Report unsupported/inaccessible evidence as a limitation, never READY.

CLI contracts: [az repos pr list/create/show/update](https://learn.microsoft.com/en-us/cli/azure/repos/pr?view=azure-cli-latest).

REST contract: [PR Update](https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-requests/update?view=azure-devops-rest-7.1); [az devops invoke](https://learn.microsoft.com/en-us/cli/azure/devops?view=azure-cli-latest#az-devops-invoke).
