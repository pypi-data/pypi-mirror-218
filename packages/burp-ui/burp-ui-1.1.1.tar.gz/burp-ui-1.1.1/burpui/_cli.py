import click

from flask import Flask
from flask.cli import FlaskGroup


def create_app():
    app = Flask("burp-ui")
    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def burp_ui():
    """Burp-UI CLI"""
    click.echo("COUCOU")
