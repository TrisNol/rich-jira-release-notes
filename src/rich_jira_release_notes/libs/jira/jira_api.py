import json
import requests

from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from enum import Enum


class JiraCredentialsModel(BaseModel):
    username: str
    token: str


class JiraFieldType(Enum):
    TEXT = "TEXT"
    RICH_TEXT = "RICH_TEXT"
    DATE = "DATE"
    NUMBER = "NUMBER"
    CHECKBOX = "CHECKBOX"


class JiraField(BaseModel):
    type: JiraFieldType
    value: str | list  # to account for different types of fields

    @property
    def is_rendered(self) -> bool:
        return self.type == JiraFieldType.RICH_TEXT

    @is_rendered.setter
    def is_rendered(self, value: bool) -> None:
        raise AttributeError("Cannot set attribute 'is_rendered'")

    @property
    def content(self) -> str:
        return str(self.value)

    @content.setter
    def content(self, value: str) -> None:
        self.value = value


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
                        value=issue["renderedFields"][field_value],
                        type=JiraFieldType.RICH_TEXT,
                    )
                elif (
                    field_value in issue["fields"]
                    and issue["fields"][field_value] is not None
                ):
                    print(issue["fields"][field_value])
                    if isinstance(issue["fields"][field_value], list):
                        entry["fields"][field_key] = JiraField(
                            value=[
                                entry["value"] for entry in issue["fields"][field_value]
                            ],
                            type=JiraFieldType.CHECKBOX,
                        )
                    else:
                        entry["fields"][field_key] = JiraField(
                            value=issue["fields"][field_value], type=JiraFieldType.TEXT
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
