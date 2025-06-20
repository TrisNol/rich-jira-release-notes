import os
import markdownify

from jinja2 import Template
from rich import print
from bs4 import BeautifulSoup

from rich_jira_release_notes.libs.jira.jira_api import JiraAPI


def generate_release_notes(
    api: JiraAPI,
    query: str,
    fields: list[str],
    convert_to_markdown: bool = True,
    output_dir: str = "dist",
    template_file: str = "./template.md.jinja",
) -> None:
    issues = api.get_issues(query, fields)
    if len(issues) == 0:
        print("🤖 - No issues found")
        return
    print(f"🤖 - Retrieved {len(issues)} issues")

    assets_dir_path = f"{output_dir}/assets"
    os.makedirs(assets_dir_path, exist_ok=True)
    for issue in issues:
        for field_key, field_content in issue.fields.items():
            if field_content.is_rendered:
                soup = BeautifulSoup(field_content.content, "html.parser")

                # Fix images
                images = soup.find_all("img")
                for image in images:
                    path = f"{assets_dir_path}/{image.get('alt')}"
                    api.download_attachment(image.get("src"), path)
                    image["src"] = "assets/" + image.get("alt")

                    print(f"🤖 - {image.get('alt')} has been downloaded")

                # Convert deprecated <tt> tags to <code> tags
                for tt in soup.find_all("tt"):
                    tt.name = "code"
                    tt["class"] = "jira-code"
                if convert_to_markdown is True:
                    issue.fields[field_key].content = markdownify.markdownify(
                        soup.prettify(),
                        heading_style="ATX",
                        escape_underscores=False,
                        escape_asterisks=False,
                    )

    # TODO - When templating the is_rendered field does not matter, model data differently
    with open(template_file) as template_file_object:
        template = Template(template_file_object.read())

        output_path = f"{output_dir}/release_notes.md"
        with open(output_path, "w") as f:
            f.write(template.render(issues=issues))
        print(f"📄 - Release notes exported to {output_path}")
