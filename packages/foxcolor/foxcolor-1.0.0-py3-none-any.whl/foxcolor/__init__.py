import argparse
from colorama import init, Fore, Style

init(autoreset=True)

class Cores:
    azul = '\033[94m'
    verde = '\033[92m'
    vermelho = '\033[91m'
    amarelo = '\033[93m'
    roxo = '\033[95m'
    ciano = '\033[96m'
    cinza = '\033[90m'
    preto = '\033[30m'
    branco = '\033[97m'
    laranja = '\033[38;5;208m'
    rosa = '\033[38;5;205m'
    violeta = '\033[38;5;165m'
    marrom = '\033[38;5;130m'
    turquesa = '\033[38;5;45m'
    prata = '\033[38;5;188m'
    dourado = '\033[38;5;214m'
    lavanda = '\033[38;5;183m'
    esmeralda = '\033[38;5;46m'
    cobre = '\033[38;5;160m'
    coral = '\033[38;5;209m'
    jade = '\033[38;5;83m'
    oliva = '\033[38;5;58m'
    lima = '\033[38;5;154m'
    ametista = '\033[38;5;129m'
    safira = '\033[38;5;69m'
    rubi = '\033[38;5;160m'
    platina = '\033[38;5;188m'
    cinza_claro = '\033[38;5;250m'
    incolor = '\033[0m'

    def rgb(self, texto):
        resultado = ''
        for i, letra in enumerate(texto):
            cor_atual = getattr(Fore, f'RGB_{i % 6 + 1}')
            resultado += f'{cor_atual}{letra}'
        return resultado + Style.RESET_ALL

    def listar_cores(self):
        atributos = dir(self)
        cores = [attr for attr in atributos if not attr.startswith('__') and not callable(getattr(self, attr))]
        return cores

cor = Cores()

def main():
    parser = argparse.ArgumentParser(prog='foxcolor', description='Biblioteca de cores para Python')
    parser.add_argument('-c', '--cores', action='store_true', help='Exibe a lista de cores disponíveis')

    args = parser.parse_args()

    if args.cores:
        cores_disponiveis = cor.listar_cores()
        print('Cores disponíveis:')
        for cor_nome in cores_disponiveis:
            print(getattr(cor, cor_nome) + cor_nome + cor.incolor)

    print(cor.rgb('Exemplo de gradiente RGB'))
