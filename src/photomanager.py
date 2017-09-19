import click

@click.group()
def photo_manager_cli():
    pass

@click.command()
@click.option('--force',  default=False, help="force update index of folder")
@click.argument('folder')
def index(force):
    """ Index the photos in folder """
    pass

@click.command()
@click.option('--tags',  default=False, help="list photo names with tags")
@click.argument('folder')
def list():
    """ List the images by condition"""
    pass

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



