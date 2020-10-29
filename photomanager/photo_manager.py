import click
from photomanager.commands.index import CommandIndex
from photomanager.commands.display import CommandList
from photomanager.commands.remove_dup import CommandRemoveDuplicate
from photomanager.commands.config import CommandConfig


@click.group()
def photo_manager_cli():
    pass


@click.command()
@click.option('--force', is_flag=True, help="force update index of folder")
@click.option('--skip_existed', is_flag=True, help="skip existed index")
@click.option('--clean', is_flag=True, help="delete obsolete records")
@click.argument('folder')
def index(folder, force, skip_existed, clean):
    """ Index the photos in folder """
    command_index = CommandIndex(folder, {"force": force, "skip_existed": skip_existed, "clean": clean})
    command_index.do()

@click.command()
@click.option('--geoinfo', is_flag=True, help="update address by geoinfo")
@click.argument('folder')
def update():
    command_index = CommandIndex(folder, {"force": force, "skip_existed": skip_existed, "clean": clean})
    command_index.do()




@click.command()
@click.argument('folder', type=click.Path(exists=True), nargs=1)
@click.argument('filters', nargs=-1)
@click.option('--limit', default=0, help="image limit for one search, 0 is unlimited")
def display(folder, filters, limit):
    """ List the images by condition"""
    command_index = CommandList(folder, {"filters": filters})
    command_index.do()


@click.command()
@click.argument('folder', default="./")
def remove_dup(folder):
    """ remove duplicate files"""
    command_remove_dup = CommandRemoveDuplicate(folder, {})
    command_remove_dup.do()


@click.command()
@click.argument('folder', default="./")
def config(folder, backup_dir):
    """ set or list the configuration """
    command_config = CommandConfig(folder, {"backup_dir", backup_dir})
    command_config.do()


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
    photo_manager_cli.add_command(display)
    photo_manager_cli.add_command(tag)
    photo_manager_cli.add_command(config)
    photo_manager_cli.add_command(show)
    photo_manager_cli.add_command(remove_dup)
    photo_manager_cli()
