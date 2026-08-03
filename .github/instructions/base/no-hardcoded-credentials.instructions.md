---
applyTo: '**'
description: 'Never hardcode credentials in test code — env vars and fake placeholders only.'
---

# No hardcoded credentials

- Never write real passwords, API keys, tokens, or connection strings into test
  code, feature files, fixtures, or any configuration committed to the repo.
- Secrets reach tests through environment variables (e.g. `${env:ZEPHYR_API_TOKEN}`
  interpolation in `.vscode/mcp.json`) or gitignored local files — never source.
- Test data that must look like a credential is obviously fake
  (`"not-a-real-password"`, `"test-user"`) — never copied from a real system.
- If you find a real credential in the repo: stop, report it to the human in your
  JIRA audit comment, and do not copy, move, or delete it on your own.
