import click
from huhk.case_project.version import version as _version


@click.command()
@click.option('-v', '--version', help='线索版本', nargs=0)
@click.option('-i', '--init', help='项目key', required=False)
@click.option('-u', '--update', help='项目key', required=False)
def main(version, init, update):
    """Simple program that greets NAME for a total of COUNT times."""
    if version:
        click.echo('版本：' + _version)
        click.echo(type(version))
    elif init:
        click.echo('init：' + _version)
        click.echo(type(init))
    elif update:
        click.echo('update：' + _version)
        click.echo(type(update))


if __name__ == '__main__':
    main()