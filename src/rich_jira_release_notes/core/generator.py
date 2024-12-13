import os
import markdownify

from jinja2 import Template
from bs4 import BeautifulSoup

from rich_jira_release_notes.libs.jira.jira_api import JiraAPI


def generate_release_notes(
    api: JiraAPI,
    query: str,
    fields: list[str],
    convert_to_markdown: bool = True,
    output_dir: str = "dist/",
    template_file: str = "./template.md.jinja",
):
    issues = api.get_issues(query, fields)

    assets_dir_path = f"{output_dir}/assets"
    os.makedirs(assets_dir_path, exist_ok=True)
    for issue in issues:
        for field_key, field_content in issue.fields.items():
            if field_content.is_rendered:
                soup = BeautifulSoup(field_content.content, "html.parser")
                images = soup.find_all("img")
                for image in images:
                    path = f"{assets_dir_path}/{image.get('alt')}"
                    api.download_attachment(image.get("src"), path)
                    image["src"] = "assets/" + image.get("alt")
                if convert_to_markdown is True:
                    issue.fields[field_key].content = markdownify.markdownify(
                        soup.prettify(), heading_style="ATX"
                    )

    # TODO - When templating the is_rendered field does not matter, model data differently
    with open(template_file) as template_file_object:
        template = Template(template_file_object.read())
        with open(f"{output_dir}/release_notes.md", "w") as f:
            f.write(template.render(issues=issues))


if __name__ == "__main__":
    from rich_jira_release_notes.libs.jira.config import get_jira_api_from_env

    api = get_jira_api_from_env()
    jql_query = 'project = DEV and fixVersion = "0.0.0"'
    fields = ["Summary", "Release Notes"]  # Key and ID will always be included
    generate_release_notes(api, jql_query, fields)
