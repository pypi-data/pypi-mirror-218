import os

import typer
from rich import print
from rich.console import Console
from typing_extensions import Annotated

from heregpt import utils
from heregpt.models import TaskBase

app = typer.Typer()

console = Console()


@app.command()
def main(
    tool: Annotated[str, typer.Argument(help="Name of the tool you want to use")],
    task: Annotated[str, typer.Argument(help="Describe the task you want to execute")],
    openai_key: Annotated[
        str, typer.Option(help="Manually provided API key for OpenAI")
    ] = None,
):
    if openai_key is not None:
        os.environ["OPENAI_API_KEY"] = openai_key
    if openai_key is None:
        if not utils.set_openai_api_key():
            console.print(
                "The environment variable OPENAI_API_KEY is not defined. More details"
                " here:"
            )
            console.print(utils.set_openai_api_key.__doc__)
            raise typer.Exit(42)
    task = TaskBase(tool=tool, task=task)
    task.build_prompt()
    console.print("About to send the following prompt🚀", style="#5f5fff")
    print(task.prompt)
    console.print("End of prompt", style="#5f5fff")
    abort = typer.confirm("Abort?", default=True)
    if abort:
        print("Aborting!")
        raise typer.Exit(10)

    response = utils.get_completion(task.prompt)
    console.print(response)
