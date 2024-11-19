import requests
import json
import os
from datetime import datetime
from CRUD_Registro import *
from CRUD_Seguro import *

usuarios = "usuarios.json"
carros_locados = "carros_locados.json"
carros_lista = "carros.json"

def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        try:
            with open(arquivo, 'r') as infile:
                return json.load(infile)
        except json.JSONDecodeError:
            print('Erro ao ler o arquivo JSON')
            return []
    return []

def salvar_dados(dados,arquivo):
    with open(arquivo, 'w') as outfile:
        json.dump(dados, outfile, indent = 4)

def checar_cpf(cpf):
    dados_usuario = carregar_dados(usuarios)
    for usuario in dados_usuario:
        if usuario['cpf'] == cpf:
            return True 

    print('Usuario não encontrado. Realizando novo cadastro...')
    nome = input('Digite seu nome: ')
    cpf_novo = input('Digite seu cpf: ')
    telefone = input("Digite seu telefone: ")
    endereco = input('Digite seu endereço: ')
    cep = input('Digite seu cep: ')
    email = input('Digite seu email: ')
    senha = input('Digite sua senha: ')
    idade = input('Digite sua idade: ')

    adicionar_usuario(nome, cpf_novo, telefone, endereco, cep, email, senha, idade)
    return True

def menu_locacao():
    print(f'======= {cor.CIANO}LocaSmart{cor.RESET} =======')
    print(f'| [{cor.CIANO}1{cor.RESET}] Locar Carro       |')
    print(f'| [{cor.CIANO}0{cor.RESET}] Sair              |')
    print('=========================\n')

def menu_buscar_carro():
    print(f'========== {cor.CIANO}LocaSmart{cor.RESET} ==========')
    print(f'| [{cor.CIANO}1{cor.RESET}] Buscar Carros por Marca |')
    print(f'| [{cor.CIANO}2{cor.RESET}] Buscar Carros por Tipo  |')
    print(f'| [{cor.CIANO}0{cor.RESET}] Sair                    |')
    print('===============================\n')

def info_carro(marca_carro, modelo_carro):
    carros = carregar_dados(carros_lista)
    for carro in carros:
        if carro['marca'] == marca_carro.capitalize():
            for modelo in carro['modelos']:
                if modelo['modelo'] == modelo_carro.capitalize():
                    codigo_fipe = modelo['codigo_fipe']

    resposta_ano = requests.get(f'https://fipe.parallelum.com.br/api/v2/cars/{codigo_fipe}/years')
    if resposta_ano.status_code == 200:
        info_ano = resposta_ano.json()
        ano_carro = ''
        for ano in info_ano:
            if '32000' in ano['code']:
                continue
            else:
                ano_carro = ano['code']
                break
    else:
        print(f'Erro: {resposta_ano.status_code}')

    resposta_carros = requests.get(f'https://fipe.parallelum.com.br/api/v2/cars/{codigo_fipe}/years/{ano_carro}')
    if resposta_carros.status_code == 200:
        info_carros = resposta_carros.json()
        valor_carro_str = info_carros['price'].replace('R$', '').replace('.', '').replace(',', '.').strip()
        valor_carro = float(valor_carro_str) * 0.002

        print(f'Marca: {info_carros['brand']}\nModelo: {info_carros['model']}\nAno: {info_carros['modelYear']}\nCombustivel: {info_carros['fuel']}\nValor do Aluguel: {valor_carro} / Dia')
    else:
        print(f'Erro: {resposta_carros.status_code}')

def mostrar_veiculos():
    carros = carregar_dados(carros_lista)
    menu_buscar_carro()
    selecionar = int(input("Selecione: "))
    if selecionar == 1:
        print(f'=========== {cor.CIANO}Marcas{cor.RESET} ============')
        print(f'| {cor.CIANO}Jeep{cor.RESET}                        |')
        print(f'| {cor.CIANO}Volkswagen{cor.RESET}                  |')
        print(f'| {cor.CIANO}Chevrolet{cor.RESET}                   |')
        print(f'| {cor.CIANO}Fiat{cor.RESET}                        |')
        print(f'| {cor.CIANO}Ford{cor.RESET}                        |')
        print(f'| {cor.CIANO}Renault{cor.RESET}                     |')
        print(f'| {cor.CIANO}Hyundai{cor.RESET}                     |')
        print(f'| {cor.CIANO}Toyota{cor.RESET}                      |')
        print(f'| {cor.CIANO}Nissan{cor.RESET}                      |')
        print(f'| {cor.CIANO}Honda{cor.RESET}                       |')
        print('===============================\n')
        marca = input("Digite a marca que deseja buscar: ").capitalize()
        for carro in carros:
            if marca == carro['marca']:
                for modelo in carro['modelos']:
                    if modelo['disponivel']:
                        print(f"Modelo: {modelo['modelo']} | Tipo: {modelo['tipo']}")
    elif selecionar == 2:
        print(f'========== {cor.CIANO}LocaSmart{cor.RESET} ==========')
        print(f'| [{cor.CIANO}1{cor.RESET}] SUV                     |')
        print(f'| [{cor.CIANO}2{cor.RESET}] Sedã                    |')
        print(f'| [{cor.CIANO}3{cor.RESET}] Hatch                   |')
        print('===============================\n')

        tipo = int(input(f"{cor.CIANO}Selecione o tipo de carro que deseja buscar: {cor.RESET}"))
        if tipo == 1:
            for carro in carros:
                for modelo in carro['modelos']:
                    if (modelo['disponivel'] and modelo['tipo'] == 'SUV'):
                        print(f"Modelo: {modelo['modelo']} | Tipo: {modelo['tipo']}")
        elif tipo == 2:
            for carro in carros:
                for modelo in carro['modelos']:
                    if (modelo['disponivel'] and modelo['tipo'] == 'Sedan'):
                        print(f"Modelo: {modelo['modelo']} | Tipo: {modelo['tipo']}")
        elif tipo == 3:
            for carro in carros:
                for modelo in carro['modelos']:
                    if (modelo['disponivel'] and modelo['tipo'] == 'Hatch'):
                        print(f"Modelo: {modelo['modelo']} | Tipo: {modelo['tipo']}")

        else:
            print(f"{cor.VERMELHO}Selecione uma opção válida!{cor.RESET}")

    elif selecionar == 3:
        for carro in carros:
            print(f"Marca: {carro['marca']}")
            for modelo in carro['modelos']:
                if modelo['disponivel']:
                    print(f"    Modelo: {modelo['modelos']} | Tipo: {modelo['tipo']}")

def selecionar_veiculo(modelo, marca,cpf):
    usuario_carro = carregar_dados(carros_locados)
    dados_usuario = carregar_dados(usuarios)
    info_carro(marca,modelo)
    for usuario in dados_usuario:
        if usuario['cpf'] == cpf:
            novo_aluguel = {'nome': usuario['nome'], 'cpf': usuario['cpf'], 'modelo': modelo.capitalize(),'marca': marca.capitalize() ,'data': '', 'seguro': False}
    usuario_carro.append(novo_aluguel)
    salvar_dados(usuario_carro, carros_locados)

def alterar_veiculo(novo_modelo,nova_marca,cpf):
    usuario_carro = carregar_dados(carros_locados)
    info_carro(nova_marca,novo_modelo)
    for usuario in usuario_carro:
        if usuario['cpf'] == cpf:
            usuario['modelo'] = novo_modelo
            usuario['marca'] = nova_marca
    salvar_dados(usuario_carro, carros_locados)

def cancelar_locacao(cpf):
    usuario_carro = carregar_dados(carros_locados)
    for usuario in usuario_carro:
        if usuario['cpf'] == cpf:
            usuario_carro.remove(usuario)
    salvar_dados(usuario_carro, carros_locados)

def verificar_disponibilidade(modeloU,marcaU,data_inicio,data_fim,):
    carros = carregar_dados(carros_lista)

    data_inicio = datetime.strptime(data_inicio, '%d-%m-%Y').date()
    data_fim = datetime.strptime(data_fim, '%d-%m-%Y').date()

    for carro in carros:
        if carro['marca'] == marcaU.capitalize():
            for modelo in carro['modelos']:
                if modelo['modelo'] == modeloU.capitalize():
                    for data in modelo['datas']:
                        inicio = datetime.strptime(data['inicio'], '%d-%m-%Y').date()
                        fim = datetime.strptime(data['fim'], '%d-%m-%Y').date()

                        if (data_inicio <= fim and data_fim >= inicio):
                            return False
                        elif not modelo['datas']:
                            return True
                    return True
    return False

def selecionar_data(data_inicio,data_fim,modeloU,marcaU):
    carros = carregar_dados(carros_lista)
    if verificar_disponibilidade(modeloU,marcaU,data_inicio,data_fim):
        for carro in carros:
            if carro['marca'] == marcaU.capitalize():
                for modelo in carro['modelos']:
                    if modelo['modelo'] == modeloU.capitalize():
                        modelo['datas'].append({'inicio': data_inicio, 'fim': data_fim})
                        return True
    else:
        print("A data selecionada já está reservada!")
        return False


def locar_carro():
    dados_locacao = carregar_dados(carros_locados)
    cpf = input("Confirme seu cpf: ")
    checar_cpf(cpf)
    while True:
        menu_locacao()
        res_menu = int(input('Selecione: '))
        if res_menu == 0:
            break
        elif res_menu == 1:
            while True:
                mostrar_veiculos()
                print(f'========== {cor.CIANO}LocaSmart{cor.RESET} ==========')
                print(f'| [{cor.CIANO}1{cor.RESET}] Selecionar Veiculo      |')
                print(f'| [{cor.CIANO}2{cor.RESET}] Informações do Veiculo  |')
                print(f'| [{cor.CIANO}3{cor.RESET}] Buscar Novamente        |')
                print('===============================\n')

                selecionar = int(input(f"{cor.CIANO}Selecione a opção: {cor.RESET}"))
                if selecionar == 3:
                    continue
                elif selecionar == 2:
                    marca = input("Digite a marca do veiculo que deseja: ").capitalize()
                    modelo = input("Digite o modelo do veiculo que deseja: ").capitalize()
                    info_carro(marca, modelo)
                    print(f'========== {cor.CIANO}LocaSmart{cor.RESET} ==========')
                    print(f'| [{cor.CIANO}1{cor.RESET}] Selecionar Veiculo      |')
                    print(f'| [{cor.CIANO}2{cor.RESET}] Buscar Novamente        |')
                    print('===============================\n')
                    selecionar2 = int(input(f"{cor.CIANO}Selecione a opção: {cor.RESET}"))
                    if selecionar2 == 1:
                        selecionar_veiculo(modelo, marca, cpf)
                    elif selecionar2 == 2:
                        continue
                elif selecionar == 1:
                    marca = input(f"{cor.CIANO}Digite a marca do veiculo que deseja: {cor.RESET}").capitalize()
                    modelo = input(f"{cor.CIANO}Digite o modelo do veiculo que deseja: {cor.RESET}").capitalize()
                    selecionar_veiculo(modelo, marca, cpf)

                print(f'========== {cor.CIANO}LocaSmart{cor.RESET} ==========')
                print(f'| [{cor.CIANO}1{cor.RESET}] Confirmar               |')
                print(f'| [{cor.CIANO}2{cor.RESET}] Trocar Veiculo          |')
                print(f'| [{cor.CIANO}3{cor.RESET}] Cancelar                |')
                print('===============================\n')

                selecionar3 = int(input(f"{cor.CIANO}Selecione a opção: {cor.RESET}"))
                if selecionar3 == 3:
                    cancelar_locacao(cpf)
                    break
                elif selecionar3 == 2:
                    nova_marca = input(f"{cor.CIANO}Digite a marca do veiculo para qual deseja alterar: {cor.RESET}").capitalize()
                    novo_modelo = input(f"{cor.CIANO}Digite o modelo do veiculo para qual deseja alterar: {cor.RESET}").capitalize()
                    alterar_veiculo(novo_modelo, nova_marca, cpf)
                elif selecionar3 == 1:
                    while True:
                        print("Por favor, insira as datas do aluguel.")
                        data_inicio = input("Data do Inicio: (dd-mm-aaaa)")
                        data_fim = input("Data do Fim: (dd-mm-aaaa)")
                        for usuario in dados_locacao:
                            if usuario['cpf'] == cpf:
                                if selecionar_data(data_inicio, data_fim, usuario['modelo'],usuario['marca']):
                                    usuario['data'] = data_inicio
                                    print('Data disponível!')
                                    break
                                else:
                                    print('Data indisponível.')
                    print(f'========== {cor.CIANO}LocaSmart{cor.RESET} ==========')
                    print(f'| [{cor.CIANO}1{cor.RESET}] Concluir Locação        |')
                    print(f'| [{cor.CIANO}2{cor.RESET}] Adicionar Seguro        |')
                    print('===============================\n')
                    selecionar_final = int(input("Selecione: "))
                    if selecionar_final == 1:
                        print("Locacao Concluida!")
                        for dados in dados_locacao:
                            if dados['cpf'] == cpf:
                                print(f"Nome: {dados['nome']}\nModelo: {dados['modelo']}\nMarca: {dados['marca']}")
                        exit()
                    elif selecionar_final == 2:
                        main_seguro()
                        exit()
                    else:
                        print("Erro")