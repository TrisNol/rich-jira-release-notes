# rich-jira-release-notes 📄🤖

![](./assets/demo.gif)
*Made with [Terminalizer](https://github.com/faressoft/terminalizer/)*

## Introduction

As of today Jira is not able to export auto-generated release notes with assets such as images (see: [Atlassion Support - Create release notes](https://support.atlassian.com/jira-cloud-administration/docs/create-release-notes/#:~:text=Release%20notes%20can%20include%20rich%20text%20and%20plain%20text%20fields.%20However%2C%20media%20such%20as%20images%2C%20videos%2C%20and%20other%20files%2C%20are%20not%20yet%20supported.)). 

The CLI provided by this repository is able to do so and serves as a workaround until Atlassian provides this functionality out-of-the-box.

## Installation

1. Install Python 3.12
2. Create a virtual environment: 

    `python3.12 -m venv ./.venv`

3. Activate the virtual environment: 

    `./.venv/scripts/activate`

4. Install the CLI: 

    `pip install git+https://github.com/TrisNol/rich-jira-release-notes.git@develop`

5. Check that the CLI is available: 

    `rich-jira-release-notes version`



## Usage

1. Create an `.env` file of the following structure

        JIRA_URL=<your_domain>.atlassian.net
        JIRA_USER=<mail of the service/human user providing the token>
        JIRA_TOKEN=<PAT>
        

    Alternatively, you can provide those values as regular env. variables

2. Create a [Jinja template](https://jinja.palletsprojects.com/en/stable/) in your project ([Example](./template.md.jinja)). You will have access to a variable called `issues` representing a list of objects of type `JiraIssue`:
    ```python
    class JiraIssue(BaseModel):
        id: str # Jira internal ticket ID
        key: str # Ticket number (<project>-<number>)
        type: str # one of: ["Bug", "Story", "Task", "Epic", "Sub-task"]
        fields: dict[str, JiraField] # Ticket fields retrieved
    ```
    A `JiraField` exposes an attribute `value` of different datatypes depending on the `type` of field selected:

    - `JiraFieldType.TEXT`: Contains raw text
    - `JiraFieldType.RICH_TEXT`: Contains rich text in Markdown format
    - `JiraFieldType.CHECKBOX`: Contains a list of strings representing the ticked checkboxes of the field


3. Construct a [JQL query](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/) fitting your use case; example:

    ```
    project = <Jira_Project_Key> AND fixVersion = "<Release_Version>"
    ```

    Replace placeholders like so:

    ```
    project = DEV and fixVersion = "4.2.0"
    ```

4. Determine the fields to export; example:

    ```
    Summary, Release Notes
    ```

3. Run
    ```sh
    rich-jira-release-notes generate 'YOUR_JQL_QUERY' fields="YOUR_FIELDS"
    ```

    Example:

    ```
    rich-jira-release-notes generate 'project = DEV and fixVersion = "0.0.0"' "Summary, Release Notes, Checkboxes"
    ```

4. Retrieve release notes from the `dist/` directory
