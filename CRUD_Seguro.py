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
    print(f"| [{Cor.CIANO}1{Cor.RESET}] - Contratar Seguro         |")
    print(f"| [{Cor.CIANO}2{Cor.RESET}] - Cancelar Seguro          |")
    print(f"| [{Cor.CIANO}0{Cor.RESET}] - Sair                     |")
    print("==================================")


def contratar_seguro(usuario, dados):
    modelo_carro = input(f"{Cor.AMARELO}Digite o modelo do carro para contratar o seguro: {Cor.RESET}")

    print(f"\n{Cor.VERDE}Você está contratando um seguro para um(a) {modelo_carro}.{Cor.RESET}")
    print(f"O Valor total do seguro é de {Cor.VERDE}R$ 250,00{Cor.RESET}\n")

    validacao_seguro = input("Deseja Contratar o seguro? (S/N) ")
    
    if validacao_seguro == "s" or validacao_seguro == "S":
        print(f"{Cor.VERDE}Seguro contratado com sucesso!{Cor.RESET}")
    elif validacao_seguro == "n" or validacao_seguro == "N":
        print(f"{Cor.VERDE}Locação sem seguro concluída com sucesso...{Cor.RESET}")
    else:
        print("Opção Inválida")

    usuario["seguro_contratado"] = True
    usuario["carro_modelo"] = modelo_carro

    salvar_dados(dados)


def cancelar_seguro(usuario, dados):
    usuario["seguro_contratado"] = False
    usuario["carro_modelo"] = None

    salvar_dados(dados)
    print(f"{Cor.VERDE}Seguro cancelado com sucesso!{Cor.RESET}")

def main_seguro():
    while True:
        dados = carregar_dados()
        mostrar_menu()
        opcao = input(f"{Cor.AMARELO}Escolha a opção: {Cor.RESET}")

        if dados:
            usuario = dados[0]
        else:
            print(f"{Cor.VERMELHO}Nenhum usuário encontrado!{Cor.RESET}")
            break

        match (opcao):
            case '1':
                contratar_seguro(usuario, dados)
            case '2':
                cancelar_seguro(usuario, dados)
            case '0':
                print(f"{Cor.CIANO}Saindo...{Cor.RESET}")
                break
            case _:
                print(f"{Cor.VERMELHO}Opção inválida! Tente novamente.{Cor.RESET}")


if __name__ == "__main__":
    main_seguro()