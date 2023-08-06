import click
import shutil
from pathlib import Path
from tidydata.config import Config  # Assumption that you have a Config class in config module of your package
from tidydata.core import TidySource, TidyExport

@click.group()
def tidydata():
    pass

@tidydata.command()
@click.argument('name')
def new(name):
    """Creates a new project with the given name."""
    base_dir = Path(name)
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / ".data/raw").mkdir(parents=True, exist_ok=True)
    (base_dir / ".data/preload").mkdir(parents=True, exist_ok=True)

    yaml_file = base_dir / "data.yaml"
    with yaml_file.open("w") as f:
        f.write("sources:")

@tidydata.command()
@click.argument('name')
def remove(name):
    """Removes an existing project with the given name."""
    base_dir = Path(name)
    if base_dir.exists():
        shutil.rmtree(base_dir)
    else:
        click.echo(f"The project '{name}' does not exist.")

@tidydata.command()
def run():
    """Checks for the existence of data.yaml in the current directory and creates a Config object if it exists."""
    yaml_file = Path('data.yaml')
    if not yaml_file.exists():
        click.echo("The file 'data.yaml' does not exist in the current directory.")
    else:
        config = Config.from_yaml(yaml_file)
        TidySource(config)
        TidyExport(config)
        click.echo("The file 'data.yaml' are successfully load to a Config object")

if __name__ == "__main__":
    tidydata()
