import json
import requests

from requests.auth import HTTPBasicAuth
from pydantic import BaseModel


class JiraCredentialsModel(BaseModel):
    username: str
    token: str


class JiraField(BaseModel):
    is_rendered: bool
    content: str


class JiraIssue(BaseModel):
    id: str
    key: str
    fields: dict[str, JiraField]


class ReleaseNotes(BaseModel):
    version: str
    issues: list[JiraIssue]


class JiraAPI:
    def __init__(self, base_url: str, credentials: JiraCredentialsModel) -> None:
        self.base_url = base_url
        self.credentials = credentials

    def get_issues(self, jql_query: str, fields: list[str]) -> list:
        """Get issues from Jira utilizing https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get

        Args:
            jql_query (str): JQL query to search for issues

        Returns:
            list: List of issues
        """
        url = f"{self.base_url}/rest/api/3/search/jql"
        auth = HTTPBasicAuth(self.credentials.username, self.credentials.token)

        headers = {"Accept": "application/json"}

        query = {
            "jql": jql_query,
            "fields": "*all",
            "fieldsByKeys": "true",
            "expand": "renderedFields,names",
        }

        response = requests.request(
            "GET", url, headers=headers, params=query, auth=auth
        )

        data = json.loads(response.text)
        print(
            json.dumps(
                json.loads(response.text),
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        )
        with open("response.json", "w") as f:
            f.write(
                json.dumps(
                    json.loads(response.text),
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )
            )

        # Resolve Jira internal field names to clear text representation of desired fields
        field_maps = {}
        for field, value in data["names"].items():
            if value in fields:
                field_maps[value] = field

        # Extract desired fields from issues
        result = []
        for issue in data["issues"]:
            entry = {"id": issue["id"], "key": issue["key"], "fields": {}}
            for field_key, field_value in field_maps.items():
                if (
                    field_value in issue["renderedFields"]
                    and issue["renderedFields"][field_value] is not None
                ):
                    entry["fields"][field_key] = JiraField(
                        is_rendered=True, content=issue["renderedFields"][field_value]
                    )
                elif (
                    field_value in issue["fields"]
                    and issue["fields"][field_value] is not None
                ):
                    entry["fields"][field_key] = JiraField(
                        is_rendered=False, content=issue["fields"][field_value]
                    )
                else:
                    raise ValueError(
                        f"Field {field_value} not found in issue {issue['key']}"
                    )
            result.append(entry)
        return [JiraIssue(**issue) for issue in result]

    def download_attachment(self, url: str, output_path: str) -> None:
        """Get attachment specified by id utilizing https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments#api-group-issue-attachments

        Args:
            id (str): ID of attachment
            output_dir (str): Output directory to save attachment to
        """
        url = f"{self.base_url}{url}"
        auth = HTTPBasicAuth(self.credentials.username, self.credentials.token)

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers, auth=auth)

        with open(output_path, "wb") as f:
            f.write(response.content)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv(override=True)

    base_url = os.getenv("JIRA_URL")
    username = os.getenv("JIRA_USER")
    token = os.getenv("JIRA_TOKEN")

    if any(v is None for v in [base_url, username, token]):
        raise RuntimeError("Missing environment variables")

    api = JiraAPI(
        str(base_url), JiraCredentialsModel(username=str(username), token=str(token))
    )

    jql_query = 'project = DEV and fixVersion = "0.0.0"'
    fields = ["Summary", "Release Notes"]  # Key and ID will always be included

    issues = api.get_issues(jql_query, fields)

    from bs4 import BeautifulSoup
    import pyhtml2md

    output_dir = "./dist"
    os.makedirs("./dist/images", exist_ok=True)
    for issue in issues:
        for field_key, field_content in issue.fields.items():
            if field_content.is_rendered:
                soup = BeautifulSoup(field_content.content, "html.parser")
                images = soup.find_all("img")
                for image in images:
                    path = f"{output_dir}/images/{image.get('alt')}"
                    api.download_attachment(image.get("src"), path)
                    image["src"] = "images/" + image.get("alt")
                issue.fields[field_key].content = pyhtml2md.convert(soup.prettify())

    # TODO - When templating the is_rendered field does not matter, model data differently
    from jinja2 import Template

    with open("./template.md.jinja") as template_file:
        template = Template(template_file.read())
        with open("./dist/release_notes.md", "w") as f:
            f.write(template.render(issues=issues))
