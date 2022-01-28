import click
import os

def ls_base(path):
    pass


@click.command("ls")
def ls():
    print("ls invoked, dont worry")