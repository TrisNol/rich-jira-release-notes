# CHANGELOG


## v0.1.0-rc.1 (2024-12-17)

### Bug Fixes

- **core**: Falsy import
  ([`8f2221a`](https://github.com/TrisNol/rich-jira-release-notes/commit/8f2221a5978e09ea7450860952bc296a00e20e46))

- **docs**: Remove leftovers
  ([`1b167bc`](https://github.com/TrisNol/rich-jira-release-notes/commit/1b167bcef8638ff5680234ee1f6a7f5508ff2298))

### Build System

- Add DevContainer config ([#1](https://github.com/TrisNol/rich-jira-release-notes/pull/1),
  [`238665d`](https://github.com/TrisNol/rich-jira-release-notes/commit/238665dc2d2bed455ee38d7006b08495aacdcbbb))

- Init app ([#2](https://github.com/TrisNol/rich-jira-release-notes/pull/2),
  [`e2bb579`](https://github.com/TrisNol/rich-jira-release-notes/commit/e2bb5795fef47d4ece28f2569c2600ec02c68eb5))

* build: init repo

* build: Typer app

- **docs**: Mkdocs integration incl. GH workflow
  ([`ba95c1e`](https://github.com/TrisNol/rich-jira-release-notes/commit/ba95c1e94cc4f62f4423bd67b7b866ac5abf8c4d))

* build: MkDocs config + pipeliine

* ci: Enable manual trigger for docs. build pipeline

### Documentation

- Extend docs
  ([`87dabee`](https://github.com/TrisNol/rich-jira-release-notes/commit/87dabeef39024949477225a1327be4aa8d10455a))

* docs: include GIF of CLI usage

* build: update link to README in pyproject.toml

### Features

- **core**: Provide main function
  ([`d22c458`](https://github.com/TrisNol/rich-jira-release-notes/commit/d22c458a4551295772831eec0966018d784ad997))

* checkpoint: retrieve issues from Jira

* checkpoint: export release notes via Jinja template

* checkpoint: convert all rendered fields to Markdown

* checkpoint: switch to markdownify for proper nested lists

* refactor: move core function into core module

* checkpoint: integrate generate command to CLI

* refactor: remove leftovers, add docs
