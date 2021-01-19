import click

from save_scummer.config import read_config, write_config


@click.group()
def ssc():
    pass


@ssc.command()
def add():
    pass


@ssc.command()
def backup():
    pass


@ssc.command()
def ls():
    pass


@ssc.command()
def restore():
    pass
