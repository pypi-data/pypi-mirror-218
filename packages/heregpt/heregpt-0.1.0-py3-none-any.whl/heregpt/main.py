import typer
from rich import print
from rich.console import Console

from heregpt import utils
from heregpt.models import TaskBase

app = typer.Typer()

console = Console()


@app.command()
def main(tool: str, task: str):
    if not utils.set_openai_api_key():
        console.print(
            "The environment variable OPENAI_API_KEY is not defined. More details here:"
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
