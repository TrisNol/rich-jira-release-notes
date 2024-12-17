import os
import json

from dotenv import load_dotenv

from rich_jira_release_notes.libs.jira.jira_api import JiraAPI, JiraCredentialsModel


def get_jira_api_from_env() -> JiraAPI:
    """Initializes the JiraAPI object using environment variables

    Raises:
        ValueError: If any of the required environment variables are missing

    Returns:
        JiraAPI: The JiraAPI object
    """
    load_dotenv(override=True)

    base_url = os.getenv("JIRA_URL")
    username = os.getenv("JIRA_USER")
    token = os.getenv("JIRA_TOKEN")

    if any(v is None for v in [base_url, username, token]):
        raise ValueError("Missing environment variables")

    api = JiraAPI(
        str(base_url), JiraCredentialsModel(username=str(username), token=str(token))
    )
    return api


def get_jira_api_from_json(config_file_path: str) -> JiraAPI:
    """Initializes the JiraAPI object using a JSON configuration file

    Raises:
        ValueError: If any of the required variables are missing

    Returns:
        JiraAPI: The JiraAPI object
    """
    with open(config_file_path, "r") as f:
        config = json.load(f)

    base_url = config.get("jira", {}).get("base_url")
    username = config.get("jira", {}).get("username")
    token = config.get("jira", {}).get("token")

    if any(v is None for v in [base_url, username, token]):
        raise RuntimeError("Missing environment variables")

    api = JiraAPI(
        str(base_url), JiraCredentialsModel(username=str(username), token=str(token))
    )
    return api
