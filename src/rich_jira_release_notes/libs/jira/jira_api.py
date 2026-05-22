import json
import requests

from requests.auth import HTTPBasicAuth
from pydantic import BaseModel
from enum import Enum

RequestParam = str | bytes | int | float | None
RequestParams = dict[str, RequestParam]


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
    type: str
    fields: dict[str, JiraField]


class ReleaseNotes(BaseModel):
    version: str
    issues: list[JiraIssue]


class JiraAPI:
    def __init__(self, base_url: str, credentials: JiraCredentialsModel) -> None:
        self.base_url = base_url
        self.credentials = credentials

    @staticmethod
    def _build_field_maps_from_names(
        names: dict | None, selected_fields: list[str]
    ) -> dict[str, str]:
        if not isinstance(names, dict):
            return {}

        return {
            display_name: field_key
            for field_key, display_name in names.items()
            if display_name in selected_fields
        }

    @staticmethod
    def _get_system_field_key(field_name: str) -> str | None:
        return {
            "summary": "summary",
            "description": "description",
        }.get(field_name.lower())

    def _search_field_id(
        self, field_name: str, headers: dict[str, str], auth: HTTPBasicAuth
    ) -> str | None:
        field_search_url = f"{self.base_url}/rest/api/3/field/search"
        params: RequestParams = {"query": field_name, "maxResults": 50}
        response = requests.request(
            "GET",
            field_search_url,
            headers=headers,
            params=params,
            auth=auth,
        )
        response.raise_for_status()
        values = response.json().get("values", [])

        for value in values:
            if value.get("name", "").lower() == field_name.lower():
                return value["id"]
        return None

    def _resolve_field_maps(
        self,
        data: dict,
        fields: list[str],
        headers: dict[str, str],
        auth: HTTPBasicAuth,
    ) -> dict[str, str]:
        field_maps = self._build_field_maps_from_names(data.get("names"), fields)

        missing_fields = [field for field in fields if field not in field_maps]
        for field_name in missing_fields:
            system_key = self._get_system_field_key(field_name)
            if system_key is not None:
                field_maps[field_name] = system_key
                continue

            field_id = self._search_field_id(field_name, headers, auth)
            if field_id is not None:
                field_maps[field_name] = field_id

        return field_maps

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

        query: RequestParams = {
            "jql": jql_query,
            "fields": "*all",
            "fieldsByKeys": "true",
            "expand": "renderedFields,names",
        }

        response = requests.request(
            "GET", url, headers=headers, params=query, auth=auth
        )
        response.raise_for_status()

        data = json.loads(response.text)

        # Resolve Jira internal field names to clear text representation of desired fields
        field_maps = self._resolve_field_maps(data, fields, headers, auth)

        # Extract desired fields from issues
        result = []
        for issue in data["issues"]:
            entry = {
                "id": issue["id"],
                "key": issue["key"],
                "type": issue["fields"]["issuetype"]["name"],
                "fields": {},
            }
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
        """Download an attachment from Jira using its URL utilizing https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-attachments#api-group-issue-attachments

        Args:
            url (str): URL of attachment
            output_path (str): Output path to save attachment to
        """
        auth = HTTPBasicAuth(self.credentials.username, self.credentials.token)

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers, auth=auth)

        with open(output_path, "wb") as f:
            f.write(response.content)
