import requests
import json
import os
from CRUD_Registro import adicionar_usuario

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
            return 'Usuario Existe!'

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
    return 'Usuario Registrado!'

def menu_locacao():
    print('==== << LocaSmart >> ====')
    print('| [1] Locar Carro       |')
    print('| [0] Sair              |')
    print('-------------------------\n')

def menu_buscar_carro():
    print('======= << LocaSmart >> =======')
    print('| [1] Buscar Carros por Marca |')
    print('| [2] Buscar Carros por Tipo  |')
    print('| [0] Sair                    |')
    print('-------------------------------\n')

def info_carro(marca_carro, modelo_carro):
    carros = carregar_dados(carros_lista)
    for carro in carros:
        if carro['marca'] == marca_carro.capitalize():
            id_marca = carro['idMarca']
            for modelo in carro['modelos']:
                if modelo['modelo'] == modelo_carro.capitalize():
                    print(modelo['modelo'])
                    print(modelo['codigo_fipe'])
                    codigo_fipe = modelo['codigo_fipe']

    resposta = requests.get(f'https://fipe.parallelum.com.br/api/v2/cars/{codigo_fipe}/years/2021-1')
    if resposta.status_code == 200:
        info_fipe = resposta.json()
        print(info_fipe)
    else:
        print(f'Erro: {resposta.status_code}')


info_carro('volkswagen','gol')