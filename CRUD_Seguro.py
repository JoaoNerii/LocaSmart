import json
import os

arquivo = "usuarios.json"

class Cor:
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    AMARELO = '\033[93m'
    VERDE = '\033[92m'
    RESET = '\033[0m'


def carregar_dados():
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r") as infile:
                return json.load(infile)
        except json.JSONDecodeError:
            print(f"{Cor.VERMELHO}Erro ao carregar o arquivo JSON.{Cor.RESET}")
            return []
    return []


def salvar_dados(dados):
    with open(arquivo, 'w') as outfile:
        json.dump(dados, outfile, indent=4)


def mostrar_menu():
    print(f"=========== {Cor.CIANO}LocaSmart{Cor.RESET} ============")
    print(f"| [{Cor.CIANO}1{Cor.RESET}] - Fazer Login              |")
    print(f"| [{Cor.CIANO}2{Cor.RESET}] - Ver painel de alugueis   |")
    print(f"| [{Cor.CIANO}3{Cor.RESET}] - Alugar Carro             |")
    print(f"| [{Cor.CIANO}4{Cor.RESET}] - Devolver Carro           |")
    print(f"| [{Cor.CIANO}5{Cor.RESET}] - Sair                     |")
    print("==================================")

def fazer_login(dados):
    nome = input(f"{Cor.AMARELO}Digite seu nome completo: {Cor.RESET}")
    cpf = input(f"{Cor.AMARELO}Digite seu CPF: {Cor.RESET}")

    for usuario in dados:
        if usuario["nome"] == nome and usuario["cpf"] == cpf:
            print(f"{Cor.VERDE}Bem-vindo, {usuario['nome']}!{Cor.RESET}")
            return usuario
    print(f"{Cor.VERMELHO}Nome ou CPF não encontrados!{Cor.RESET}")
    return None


def exibir_painel(usuario):
    if usuario:
        print(f"\n{Cor.CIANO}=====================")
        print(f"  Painel de {usuario['nome']}")
        print("====================={Cor.RESET}")
        if usuario["carro_alugado"]:
            print(f"Você está alugando um carro: {usuario['carro_modelo']} - Placa: {usuario['carro_placa']}")
        else:
            print("Você não tem nenhum carro alugado no momento.")
    else:
        print(f"{Cor.VERMELHO}Você precisa estar logado para acessar o painel.{Cor.RESET}")


def alugar_carro(usuario, dados):
    if usuario:
        if usuario["carro_alugado"]:
            print(f"{Cor.VERMELHO}Você já tem um carro alugado!{Cor.RESET}")
            return

        modelo_carro = input(f"{Cor.AMARELO}Digite o modelo do carro que deseja alugar: {Cor.RESET}")
        placa_carro = input(f"{Cor.AMARELO}Digite a placa do carro: {Cor.RESET}")

        usuario["carro_alugado"] = True
        usuario["carro_modelo"] = modelo_carro
        usuario["carro_placa"] = placa_carro

        salvar_dados(dados)
        print(f"{Cor.VERDE}Carro {modelo_carro} com placa {placa_carro} alugado com sucesso!{Cor.RESET}")
    else:
        print(f"{Cor.VERMELHO}Você precisa estar logado para alugar um carro.{Cor.RESET}")


def devolver_carro(usuario, dados):
    if usuario:
        if not usuario["carro_alugado"]:
            print(f"{Cor.VERMELHO}Você não tem um carro alugado para devolver.{Cor.RESET}")
            return

        usuario["carro_alugado"] = False
        usuario["carro_modelo"] = None
        usuario["carro_placa"] = None

        salvar_dados(dados)
        print(f"{Cor.VERDE}Carro devolvido com sucesso!{Cor.RESET}")
    else:
        print(f"{Cor.VERMELHO}Você precisa estar logado para devolver um carro.{Cor.RESET}")


def main():
    dados = carregar_dados()
    usuario_logado = None

    while True:
        mostrar_menu()
        opcao = input(f"{Cor.AMARELO}Escolha a opção: {Cor.RESET}")

        match opcao:
            case '1':
                usuario_logado = fazer_login(dados)
            case '2':
                exibir_painel(usuario_logado)
            case '3':
                alugar_carro(usuario_logado, dados)
            case '4':
                devolver_carro(usuario_logado, dados)
            case '5':
                print(f"{Cor.CIANO}Saindo... Até logo!{Cor.RESET}")
                break
            case _:
                print(f"{Cor.VERMELHO}Opção inválida! Tente novamente.{Cor.RESET}")


if __name__ == "__main__":
    main()
