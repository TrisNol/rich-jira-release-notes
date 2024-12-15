import typer

from src.rich_jira_release_notes.libs.jira.config import (
    get_jira_api_from_env,
    get_jira_api_from_json,
)
from src.rich_jira_release_notes.core.generator import generate_release_notes


app = typer.Typer()


@app.command()
def version():
    typer.echo("rich-jira-release-notes 0.0.0")


@app.command()
def generate(
    jql_query: str = typer.Argument(help="JQL query to search for issues"),
    fields: str = typer.Argument(
        "Summary, Release Notes",
        help="Comma separated list of fields to include in the release notes",
        show_default=True,
    ),
    convert_to_markdown: bool = typer.Option(
        True, help="Convert HTML to Markdown", show_default=True
    ),
    output_dir: str = typer.Argument(
        "dist", help="Output directory", show_default=True
    ),
    template_file: str = typer.Argument(
        "./template.md.jinja", help="Template file to use", show_default=True
    ),
    config_file: str = typer.Argument(
        None, help="Path to JSON configuration file", show_default=False
    ),
):
    """
    Generate release notes
    """
    if config_file:
        api = get_jira_api_from_json(config_file)
    else:
        api = get_jira_api_from_env()

    generate_release_notes(
        api,
        jql_query,
        [field.strip() for field in fields.split(",")],
        convert_to_markdown,
        output_dir,
        template_file,
    )
