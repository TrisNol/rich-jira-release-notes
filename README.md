# rich-jira-release-notes 📄🤖

As of today Jira is not able to export auto-generated release notes with assets such as images (see: [Atlassion Support - Create release notes](https://support.atlassian.com/jira-cloud-administration/docs/create-release-notes/#:~:text=Release%20notes%20can%20include%20rich%20text%20and%20plain%20text%20fields.%20However%2C%20media%20such%20as%20images%2C%20videos%2C%20and%20other%20files%2C%20are%20not%20yet%20supported.)).

The CLI provided by this repository is able to do so and serves as a workaround until Atlassian provides this functionality out-of-the-box.

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
