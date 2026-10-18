# Security

## What this repository holds

This repository is a static website: a home page and a privacy policy, each in
Turkish and English, and a not-found page. It is published with GitHub Pages,
and that is all it does.

- **No code runs on a server.** The pages are plain HTML and CSS. There is no
  JavaScript, no form, no cookie and no analytics.
- **Nothing is loaded from another origin.** Every page declares a Content
  Security Policy that allows only styles and images from the site itself, and
  the check in `.github/scripts/check_site.py` fails the build if a page breaks
  that rule.
- **There are no secrets here.** No key, token, password or server address is
  part of this repository, and none ever will be. Secret scanning and push
  protection are enabled to keep it that way.
- **The workflow has the least access it needs.** It reads the repository and,
  only on `main`, deploys to Pages. Every action is pinned to a full commit
  hash, and Dependabot proposes updates.

## Supported versions

Only the live site, built from `main`, is supported.

## Reporting a vulnerability

Please report it privately through the
[Security tab](https://github.com/OzcanOrhanDemirci/sunucu-yedek/security) of
this repository ("Report a vulnerability"). Do not open a public discussion
about it. You can expect a reply within a week.
