from .tiktokData import *
from .instaData import *

import click
from setup import VERSION

@click.command()
@click.version_option(version=VERSION)
def cli():
    pass

__all__ = [name for name in globals() if not name.startswith('_')]

if __name__ == '__main__':
    cli()