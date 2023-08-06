import click

@click.command()
@click.argument('trecho')
@click.option(
    '--arquivo',
    default='texto.txt',
    help='Encontre a linha relacionada ao trecho em questão'
)
def greet(arquivo, trecho):
    try:
        with open(arquivo) as f:
            for line in f:
                if trecho.lower() in line.lower():
                    with open('resultado.txt', 'w') as f2:
                        f2.write(line)
    except FileNotFoundError:
        click.echo(f'O arquivo "{arquivo}" não foi encontrado.')

if __name__ == '__main__':
    greet()