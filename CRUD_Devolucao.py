import json
import os
import re
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

arquivo = "devolucoes.json"
arquivo_locacao = "locacoes.json"
arquivo_multas = "multas.json"

class cor:
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    RESET = '\033[0m'

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r") as infile:
                return json.load(infile)
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo JSON.")
            return {}
    return {}

def salvar_dados(dados, arquivo):
    with open(arquivo, "w") as outfile:
        json.dump(dados, outfile, indent=4)

def gerar_id(dados):
    return max(map(int, dados.keys()), default=0) + 1

def registrar_multa(cliente_id):
    multas = carregar_dados(arquivo_multas)
    multa_id = gerar_id(multas)
    multas[multa_id] = {
        "cliente_id": cliente_id,
        "motivo": "Atraso na devolução do veículo"
    }
    salvar_dados(multas, arquivo_multas)
    print(Fore.RED + f"Uma multa foi gerada para o cliente {cliente_id} devido ao atraso na devolução.")


def validar_data(data):
    padrao = r"^\d{2}-\d{2}-\d{4}$"
    if re.match(padrao, data):
        try:
            datetime.strptime(data, "%d-%m-%Y")
            return True
        except ValueError:
            print(Fore.RED + "Data inválida. Verifique se o dia é válido para o mês e o ano informados.")
            return False
    else:
        print(Fore.RED + "Formato de data incorreto. O formato correto é DD-MM-AAAA.")
        return False

def cadastrar_devolucao():
    devolucoes = carregar_dados(arquivo)
    locacoes = carregar_dados(arquivo_locacao)

    carro_id = input(Fore.YELLOW + "Modelo do Carro: ")
    cliente_id = input(Fore.YELLOW + "Nome do Cliente: ")

    while True:
        cpf = input(Fore.YELLOW + "CPF do Cliente: ")
        break

    while True:
        data_devolucao = input(Fore.YELLOW + "Data de Devolução (DD-MM-AAAA): ")
        if validar_data(data_devolucao):
            break

    while True:
        danos = input(Fore.YELLOW + "Descrição dos Danos (se houver): ")
        if danos.strip():
            break
        print(Fore.RED + "A descrição dos danos não pode estar vazia. Insira algo.")

    devolucao_id = gerar_id(devolucoes)
    print(Fore.CYAN + f"Seu ID é {devolucao_id}")

    locacao = locacoes.get(cliente_id)
    if locacao:
        data_fim_locacao = datetime.strptime(locacao["data_fim"], "%d-%m-%Y")
        data_devolucao_dt = datetime.strptime(data_devolucao, "%d-%m-%Y")
        
        if data_devolucao_dt > data_fim_locacao:
            registrar_multa(cliente_id)

    devolucao = {
        "carro_id": carro_id,
        "cliente_id": cliente_id,
        "cpf": cpf,
        "data_devolucao": data_devolucao,
        "danos": danos
    }

    devolucoes[devolucao_id] = devolucao
    salvar_dados(devolucoes, arquivo)
    print(Fore.GREEN + f"Devolução cadastrada com sucesso! ID da Devolução: {devolucao_id}")

def listar_devolucoes_por_cpf():
    devolucoes = carregar_dados(arquivo)
    
    while True:
        cpf = input(Fore.YELLOW + "Informe o CPF do Cliente para listar as devoluções: ")
        break

    encontrou = False
    for devolucao_id, devolucao in devolucoes.items():
        if devolucao.get("cpf") == cpf:
            print(Fore.CYAN + f"\nID Devolução: {devolucao_id}")
            print(Fore.CYAN + f"ID Carro: {devolucao['carro_id']}")
            print(Fore.CYAN + f"Nome Cliente: {devolucao['cliente_id']}")
            print(Fore.CYAN + f"Data de Devolução: {devolucao['data_devolucao']}")
            print(Fore.CYAN + f"Danos: {devolucao['danos']}")
            encontrou = True

    if not encontrou:
        print(Fore.RED + "Nenhuma devolução encontrada para esse CPF.")

def atualizar_devolucao():
    devolucoes = carregar_dados(arquivo)
    devolucao_id = input(Fore.YELLOW + "Informe o ID da devolução que deseja atualizar: ")

    if devolucao_id in devolucoes:
        carro_id = input(Fore.YELLOW + "Novo modelo do Carro: ")
        cliente_id = input(Fore.YELLOW + "Novo nome do Cliente: ")

        while True:
            cpf = input(Fore.YELLOW + "Novo CPF do Cliente (XXX.XXX.XXX-XX): ")
            if re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf):
                break
            else:
                print(Fore.RED + "CPF inválido. O formato correto é XXX.XXX.XXX-XX.")

        while True:
            data_devolucao = input(Fore.YELLOW + "Nova Data de Devolução (DD-MM-AAAA): ")
            if validar_data(data_devolucao):
                break

        while True:
            danos = input(Fore.YELLOW + "Nova Descrição dos Danos (se houver): ")
            if danos.strip():
                break
            print(Fore.RED + "A descrição dos danos não pode estar vazia. Insira algo.")

        devolucoes[devolucao_id] = {
            "carro_id": carro_id,
            "cliente_id": cliente_id,
            "cpf": cpf,
            "data_devolucao": data_devolucao,
            "danos": danos
        }

        salvar_dados(devolucoes, arquivo)
        print(Fore.GREEN + "Devolução atualizada com sucesso!")
    else:
        print(Fore.RED + "ID de devolução não encontrado.")

def excluir_devolucao():
    devolucoes = carregar_dados(arquivo)
    devolucao_id = input(Fore.YELLOW + "Informe o ID da devolução que deseja excluir: ")

    if devolucao_id in devolucoes:
        del devolucoes[devolucao_id]
        salvar_dados(devolucoes, arquivo)
        print(Fore.GREEN + "Devolução excluída com sucesso!")
    else:
        print(Fore.RED + "ID de devolução não encontrado.")

def menu_dev():
    while True:
        print(f"=============== {cor.CIANO}LocaSmart{cor.RESET} ==============")
        print(f"| [{cor.CIANO}1{cor.RESET}] - Cadastrar Devolução            |")
        print(f"| [{cor.CIANO}2{cor.RESET}] - Listar Devoluções por CPF      |")
        print(f"| [{cor.CIANO}3{cor.RESET}] - Atualizar Devolução            |")
        print(f"| [{cor.CIANO}4{cor.RESET}] - Excluir Devolução              |")
        print(f"| [{cor.CIANO}0{cor.RESET}] - Sair                           |")
        print("=" * 40)
        
        opcao = input(Fore.CYAN + "Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_devolucao()
        elif opcao == "2":
            listar_devolucoes_por_cpf()
        elif opcao == "3":
            atualizar_devolucao()
        elif opcao == "4":
            excluir_devolucao()
        elif opcao == "0":
            print(Fore.GREEN + "Saindo do sistema de devoluções...")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")