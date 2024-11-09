import json
import os

arquivo = "usuarios.json"
carros = "carros.json"

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


def carregar_carros():
    if os.path.exists(carros):
        try:
            with open(carros, "r") as infile:
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
    print(f"| [{Cor.CIANO}2{Cor.RESET}] - Ver painel de seguros    |")
    print(f"| [{Cor.CIANO}3{Cor.RESET}] - Contratar Seguro         |")
    print(f"| [{Cor.CIANO}4{Cor.RESET}] - Cancelar Seguro          |")
    print(f"| [{Cor.CIANO}5{Cor.RESET}] - Sair                     |")
    print("==================================")


def fazer_login(dados):
    cpf = input(f"{Cor.AMARELO}Digite seu CPF: {Cor.RESET}")
    senha = input(f"{Cor.AMARELO}Digite sua senha: {Cor.RESET}")

    for usuario in dados:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            print(f"{Cor.VERDE}Bem-vindo, {usuario['nome']}!{Cor.RESET}")
            return usuario
    print(f"{Cor.VERMELHO}CPF ou senha incorretos!{Cor.RESET}")
    return None


def exibir_painel(usuario):
    if usuario:
        print(f"\n{Cor.CIANO}=====================")
        print(f"  Painel de {usuario['nome']}")
        print("====================={Cor.RESET}")
        if usuario.get("seguro_contratado", False):
            print(f"Você possui um seguro contratado para o carro: {usuario['carro_modelo']} - Placa: {usuario['carro_placa']}")
        else:
            print("Você não possui seguro contratado no momento.")
    else:
        print(f"{Cor.VERMELHO}Você precisa estar logado para acessar o painel.{Cor.RESET}")


def contratar_seguro(usuario, dados):
    if usuario:
        if usuario.get("seguro_contratado", False):
            print(f"{Cor.VERMELHO}Você já possui um seguro contratado!{Cor.RESET}")
            return

        modelo_carro = input(f"{Cor.AMARELO}Digite o modelo do carro para contratar o seguro: {Cor.RESET}")
        placa_carro = input(f"{Cor.AMARELO}Digite a placa do carro: {Cor.RESET}")

        usuario["seguro_contratado"] = True
        usuario["carro_modelo"] = modelo_carro
        usuario["carro_placa"] = placa_carro

        salvar_dados(dados)
        print(f"{Cor.VERDE}Seguro para o carro {modelo_carro} com placa {placa_carro} contratado com sucesso!{Cor.RESET}")
    else:
        print(f"{Cor.VERMELHO}Você precisa estar logado para contratar um seguro.{Cor.RESET}")


def cancelar_seguro(usuario, dados):
    if usuario:
        if not usuario.get("seguro_contratado", False):
            print(f"{Cor.VERMELHO}Você não possui um seguro para cancelar.{Cor.RESET}")
            return

        usuario["seguro_contratado"] = False
        usuario["carro_modelo"] = None
        usuario["carro_placa"] = None

        salvar_dados(dados)
        print(f"{Cor.VERDE}Seguro cancelado com sucesso!{Cor.RESET}")
    else:
        print(f"{Cor.VERMELHO}Você precisa estar logado para cancelar um seguro.{Cor.RESET}")


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
                contratar_seguro(usuario_logado, dados)
            case '4':
                cancelar_seguro(usuario_logado, dados)
            case '5':
                print(f"{Cor.CIANO}Saindo... Até logo!{Cor.RESET}")
                break
            case _:
                print(f"{Cor.VERMELHO}Opção inválida! Tente novamente.{Cor.RESET}")


if __name__ == "__main__":
    main()