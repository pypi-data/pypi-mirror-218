import click

@click.command()
@click.argument('trecho')
@click.option(
    '--arquivo',
    required=True,
    default='texto.txt',
    help='Arquivo na qual o trecho vai ser buscado.'
    
)
@click.option(
    '--extrair',
    is_flag=True,
    help='Define se acontecerá extração do arquivo original.'
    
)
def parse(arquivo, trecho, extrair):
    if extrair:
        linhas = []
        resultados = []
        try:
            with open(arquivo) as f1, open('resultado.txt', 'w') as f2:
                for line in f1:
                    if trecho.lower() in line.lower():
                        resultados.append(line)
                    else:
                        linhas.append(line)
                        
                conteudo = ''.join(resultados)
                f2.write(conteudo)
                
            with open(arquivo, 'w') as f:
                conteudo = ''.join(linhas)
                f.write(conteudo)

                
            click.echo('Arquivo raspado com sucesso!')
            click.echo('Resultado:')
            for line in resultados:
                click.echo(line)
                    
        except FileNotFoundError:
            click.echo(f'O arquivo "{arquivo}" não foi encontrado.')
            
    else:
        results = []
        try:
            with open(arquivo) as f1:
                for line in f1:
                    if trecho.lower() in line.lower():
                        results.append(line)
                        
            with open('resultado.txt', 'w') as f2:
                conteudo = ''.join(results)
                f2.write(conteudo)
                
                click.echo('Arquivo raspado com sucesso!')
                click.echo('Resultado:')
                for line in results:
                    click.echo(line.strip())
                    
        except FileNotFoundError:
            click.echo(f'O arquivo "{arquivo}" não foi encontrado.')

if __name__ == '__main__':
    parse()