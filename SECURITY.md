# Security Policy

## Reporting a Vulnerability

This repository contains educational code examples. If you find a security issue
in any of the examples (e.g., accidental credential exposure, unsafe patterns),
please report it by [opening a private security advisory](https://github.com/flaviomilan/posts.codebase/security/advisories/new).

Do **not** open a public issue for security vulnerabilities.

## Scope

- Code examples in this repository are **for educational purposes only**
- They use simulated data and are not intended for production use
- API keys should **never** be committed — use environment variables

## Best Practices

When running the examples:

1. **Never commit API keys** — use `export OPENAI_API_KEY="..."` or a `.env` file
2. **Use virtual environments** — isolate dependencies with `python -m venv .venv`
3. **Pin dependencies** — use the provided `requirements.txt`
4. **Review code before running** — understand what each script does
