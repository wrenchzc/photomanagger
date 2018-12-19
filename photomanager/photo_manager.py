import click
from photomanager.commands.index import CommandIndex
from photomanager.commands.list import CommandList

@click.group()
def photo_manager_cli():
    pass

@click.command()
@click.option('--force',  default=False, help="force update index of folder")
@click.option('--skip_existed',  default=False, help="skip existed index")
@click.argument('folder')
def index(folder, force, skip_existed):
    """ Index the photos in folder """
    command_index = CommandIndex(folder, {"force": force, "skip_existed": skip_existed})
    command_index.do()

@click.command()
@click.option('--tags',  default=False, help="list photo names with tags")
@click.option('--duplicate',  default=False, help="list duplicate photos")
@click.argument('folder')
def list(folder, tags, duplicate):
    """ List the images by condition"""
    command_index = CommandList(folder, {"tags": tags, "duplicate": duplicate})
    command_index.do()

@click.command()
def config():
    """ set or list the configuration """
    pass

@click.command()
@click.argument('files')
def tag():
    """ add tags to some photos"""
    pass

@click.command()
def show():
    """show photos"""
    pass

if __name__ == "__main__":
    photo_manager_cli.add_command(index)
    photo_manager_cli.add_command(list)
    photo_manager_cli.add_command(tag)
    photo_manager_cli.add_command(config)
    photo_manager_cli.add_command(show)
    photo_manager_cli()



