import click
from huhk.case_project.version import version as _version


@click.group()
def main():
    pass


@click.command()
@click.option('-v', '--version', help='线索版本')
@click.option('-i', '--init', help='项目key', prompt=True)
@click.option('-u', '--update', help='项目key')
def main(version=None, init=None, update=None):
    """Simple program that greets NAME for a total of COUNT times."""
    if version:
        click.echo('版本：' + _version)
    elif init:
        click.echo('init：' + _version)
    elif update:
        click.echo('update：' + _version)


if __name__ == '__main__':
    main()