import click
from flask.cli import AppGroup, FlaskGroup

from app import create_app

cli = FlaskGroup(create_app=create_app)

@cli.command()
@click.argument('name')
def bob(name):
    print(name)

if __name__ == '__main__':
    # run python cli.py {function} {arguement}
    cli()
