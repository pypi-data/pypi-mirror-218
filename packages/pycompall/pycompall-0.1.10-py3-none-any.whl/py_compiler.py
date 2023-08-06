from pathlib import Path
import click
from app.application import compile_command


@click.group()
def cli():
    pass


@cli.command()
@click.option('-recursive', '-r', is_flag=True, default=True, help='Recurse through subdirectories.')
@click.option('--in-place', is_flag=True, default=False, help='Remove .py and replace them with compiled .pyc files.')
@click.option('--create-empty-init', is_flag=True, default=False, help='Create an empty __init__.py file in the path specified after compilation. Useful for interacting with tools such as colcon.')
@click.argument('path', type=click.Path(exists=True))
def compile(path, recursive, in_place, create_empty_init):
    click.echo(create_empty_init)
    compile_command(
        Path(path),
        recursive=recursive,
        in_place=in_place,
        create_empty_init=create_empty_init
    )
