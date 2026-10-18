# Contributing

This repository holds the information and privacy pages of a personal tool,
and it is maintained by its owner alone. Outside contributions are not
accepted, and issues are turned off.

If you find a security problem, please follow [SECURITY.md](SECURITY.md).

## For the maintainer

- Every change goes through a pull request; `main` accepts squash merges only,
  after the `check` job passes.
- Run `python3 .github/scripts/check_site.py site` before opening one.
- Keep the Turkish (`site/`) and English (`site/en/`) pages in step.
- When the privacy policy changes, change its effective date in both languages.
- Commit messages follow Conventional Commits, in English and in the imperative
  mood, with a subject of at most 72 characters.
