import click

import subprocess
import sys

from dotenv import load_dotenv

from .config import get_project_base_dir
from .generator import generate_project, generate_app
from .context import ProjectContext, AppContext


@click.group()
def cli():
    pass


@cli.command()
def run():
    project_base_dir = get_project_base_dir()
    load_dotenv(project_base_dir / "env.env")
    subprocess.run(
        [sys.executable, project_base_dir / "main.py"]
    )


@cli.command()
@click.argument("app_name")
def startapp(app_name: str):
    context = AppContext(app_name=app_name)
    try:
        generate_app(context)
    except TypeError:
        click.echo("Вы находитесь не в директории проекта curcheck!")


@cli.command()
@click.argument("project_name")
@click.option('--full', 'project_size', flag_value='full')
@click.option(
    '--mini', 'project_size', flag_value='mini', default=True
)
def startproject(project_name: str, project_size: str):
    if project_size == "full": is_full = True
    else: is_full = False
    context = ProjectContext(
        project_name=project_name,
        is_full=is_full
    )
    generate_project(context)
