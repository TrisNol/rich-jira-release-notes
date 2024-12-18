# CHANGELOG


## v0.1.1-rc.1 (2024-12-17)

### Bug Fixes

- **docs**: Resolve MkDocs issue
  ([`2c1232f`](https://github.com/TrisNol/rich-jira-release-notes/commit/2c1232f8d6f72a1650335d1c601e875f132280d2))

### Build System

- Configure remote token for python-semantic-release
  ([`622e60c`](https://github.com/TrisNol/rich-jira-release-notes/commit/622e60cf13578e8815e015eeb1685f704385a097))

### Chores

- Merge branch 'main' into develop
  ([`3f12a5b`](https://github.com/TrisNol/rich-jira-release-notes/commit/3f12a5bac02eb44157cd3d753afa305a7eebdaf7))


## v0.1.0 (2024-12-17)

### Chores

- Merge 'develop' into 'main' #7
  ([`b3b8d52`](https://github.com/TrisNol/rich-jira-release-notes/commit/b3b8d52fa67c06f8eb6eb345eecb469dbdcb6fb5))

- **release**: V0.1.0 [skip ci]
  ([`a6df0c9`](https://github.com/TrisNol/rich-jira-release-notes/commit/a6df0c9eb58d6ad43038ce95030037c4103563ed))


## v0.1.0-rc.1 (2024-12-17)

### Bug Fixes

- **core**: Falsy import
  ([`8f2221a`](https://github.com/TrisNol/rich-jira-release-notes/commit/8f2221a5978e09ea7450860952bc296a00e20e46))

- **docs**: Remove leftovers
  ([`1b167bc`](https://github.com/TrisNol/rich-jira-release-notes/commit/1b167bcef8638ff5680234ee1f6a7f5508ff2298))

### Build System

- Add DevContainer config ([#1](https://github.com/TrisNol/rich-jira-release-notes/pull/1),
  [`238665d`](https://github.com/TrisNol/rich-jira-release-notes/commit/238665dc2d2bed455ee38d7006b08495aacdcbbb))

- Fetch entire repo history in release pipeline
  ([`1f048f7`](https://github.com/TrisNol/rich-jira-release-notes/commit/1f048f7f528006638b094fba86a05071cc46c983))

- Give pipeline id-token permission
  ([`8c60510`](https://github.com/TrisNol/rich-jira-release-notes/commit/8c60510d3bfa09b202d74a463d47008204ab1955))

- Give release pipeline write permissions
  ([`0ab7065`](https://github.com/TrisNol/rich-jira-release-notes/commit/0ab7065be06b94aebda77c6b29ed9e501844ac6d))

- Init app ([#2](https://github.com/TrisNol/rich-jira-release-notes/pull/2),
  [`e2bb579`](https://github.com/TrisNol/rich-jira-release-notes/commit/e2bb5795fef47d4ece28f2569c2600ec02c68eb5))

* build: init repo

* build: Typer app

- Integrate python-semantic-release #6
  ([`7677b9c`](https://github.com/TrisNol/rich-jira-release-notes/commit/7677b9c2de14c72ee201fd0f7e21c0f4109e6e30))

- Remove repo_dir from semantic_release config
  ([`b2a2114`](https://github.com/TrisNol/rich-jira-release-notes/commit/b2a2114a7b50303cfa0796e16edb0270f6360074))

- Resolve branch trigger typo
  ([`2c671a9`](https://github.com/TrisNol/rich-jira-release-notes/commit/2c671a9f65c2ecf8a0c24e58684726243c1c3c49))

- Resolve python-semantic-release issue
  ([`8e385e2`](https://github.com/TrisNol/rich-jira-release-notes/commit/8e385e225c193f75152478a7b9d883663562dc25))

- **docs**: Mkdocs integration incl. GH workflow
  ([`ba95c1e`](https://github.com/TrisNol/rich-jira-release-notes/commit/ba95c1e94cc4f62f4423bd67b7b866ac5abf8c4d))

* build: MkDocs config + pipeliine

* ci: Enable manual trigger for docs. build pipeline

### Chores

- **release**: V0.1.0-rc.1 [skip ci]
  ([`c310593`](https://github.com/TrisNol/rich-jira-release-notes/commit/c310593468970cc78d15391995962ad331551813))

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
