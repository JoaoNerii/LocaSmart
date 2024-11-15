import json
import os
from CRUD_Registro import *

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


def menu_seguro():
    dados = carregar_dados()
    print(f"=========== {Cor.CIANO}LocaSmart{Cor.RESET} ============")
    print(f"| [{Cor.CIANO}1{Cor.RESET}] - Ver painel de seguros    |")
    print(f"| [{Cor.CIANO}2{Cor.RESET}] - Contratar Seguro         |")
    print(f"| [{Cor.CIANO}3{Cor.RESET}] - Cancelar Seguro          |")
    print(f"| [{Cor.CIANO}0{Cor.RESET}] - Sair                     |")
    print("==================================")
    opcao = input(f"{Cor.AMARELO}Escolha a opção: {Cor.RESET}")

    match opcao:
        case '1':
            exibir_painel()
        case '2':
            contratar_seguro(dados)
        case '3':
            cancelar_seguro(dados)
        case '0':
            print(f"{Cor.CIANO}Saindo... Até logo!{Cor.RESET}")
        case _:
            print(f"{Cor.VERMELHO}Opção inválida! Tente novamente.{Cor.RESET}")


def exibir_painel(usuario): #ADM
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