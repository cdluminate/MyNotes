import click

@click.command()
@click.option('--count', default=1, help='Number of greetings')
@click.option('--name', prompt='Your name', help='the person to greet')
def hello(count, name):
    for x in range(count):
        click.echo('Hello %s' % name)

@click.group()
def cli():
    pass

@cli.command()
@click.option('-c', '--count', 'count', default=1, type=click.INT, help='num')
def aaa(count):
    for i in range(count):
        click.echo('aaa')

@cli.command()
def bbb():
    click.echo('bbb')

if __name__ == '__main__':
    #hello()
    cli()
