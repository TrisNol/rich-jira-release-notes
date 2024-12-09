import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Callback function that will be called before running any command.
    """


@app.command()
def generate():
    """
    Generate release notes
    """
    typer.echo("Generating release notes")
