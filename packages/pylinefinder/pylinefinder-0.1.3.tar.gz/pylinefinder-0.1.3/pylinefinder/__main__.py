import click

@click.command()
@click.argument('trecho')
@click.option(
    '--arquivo',
    default='texto.txt',
    help='Encontre a linha relacionada ao trecho em questão'
)
def greet(arquivo, trecho):
    results = []
    try:
        with open(arquivo) as f:
            for line in f:
                if trecho.lower() in line.lower():
                    results.append(line)
                    
        with open('resultado.txt', 'w') as f2:
            conteudo = ''.join(results)
            f2.write(conteudo)
            
            click.echo('Arquivo raspado com sucesso!')
            click.echo('Resultado:')
            for line in results:
                click.echo(line)
                
    except FileNotFoundError:
        click.echo(f'O arquivo "{arquivo}" não foi encontrado.')

if __name__ == '__main__':
    greet()