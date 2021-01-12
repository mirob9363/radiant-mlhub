import configparser
from pathlib import Path

import click

from .__version__ import __version__


@click.group()
@click.version_option(version=__version__)
def mlhub():
    """CLI tool for the radiant_mlhub Python client."""


@mlhub.command()
@click.option('--profile', default='default', help='The name of the profile to configure.')
@click.option('--api-key', prompt='API Key')
def configure(profile, api_key):
    """Interactively set up radiant_mlhub configuration file."""

    config_path = Path.home() / '.mlhub' / 'profiles'

    config = configparser.ConfigParser()
    config.read(config_path)

    existing_api_key = config.get(profile, 'api_key', fallback=None)

    if existing_api_key and not click.confirm(f'Overwrite existing API Key (****{existing_api_key[-6:]})'):
        raise click.Abort

    if not config.has_section(profile):
        config[profile] = {}
    config[profile]['api_key'] = api_key

    # Create the parent directory if it does not exist
    config_path.parent.mkdir(exist_ok=True)

    with config_path.open('w') as dst:
        config.write(dst)

    print(f'Wrote profile to {config_path}')
