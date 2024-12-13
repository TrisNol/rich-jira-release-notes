# rich-jira-release-notes
Generate rich Jira release notes📄🤖

## How to

1. Create an `.env` file of the following structure
```js
JIRA_URL=
JIRA_USER=
JIRA_TOKEN=
```
2. Create a [Jinja template](https://jinja.palletsprojects.com/en/stable/) in your project ([Example](./template.md.jinja))
3. Install the CLI
4. Run
    ```sh
    rich-jira-release-notes generate 'project = DEV and fixVersion = 0.0.0' fields="Summary, Release Notes"
    ```
5. Retrieve release notes from the [./dist directory](./dist)
