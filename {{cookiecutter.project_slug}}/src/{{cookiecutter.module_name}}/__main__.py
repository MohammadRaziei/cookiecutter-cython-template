"""Command-line interface for {{ cookiecutter.project_slug }}."""

import click
from {{ cookiecutter.module_name }} import Curl


@click.command()
@click.argument('url')
def main(url):
    """Simple command-line tool to make HTTP requests using {{ cookiecutter.project_slug }}."""
    curl = Curl()
    response = curl.get(url)
    click.echo(f"Status: {response.status_code}")
    click.echo(f"Body: {response.text}")


if __name__ == "__main__":
    main()