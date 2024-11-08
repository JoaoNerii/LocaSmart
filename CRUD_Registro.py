import json
import os

arquivo = "usuarios.json"

class cor:
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    RESET = '\033[0m'

def carregar_dados():
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r") as infile:
                return json.load(infile)
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo JSON.")
            return []
    return []

def salvar_dados(dados):
    with open(arquivo, "w") as outfile:
        json.dump(dados, outfile, indent=4)

def adicionar_usuario(nome, cpf, telefone, endereco, cep, email, senha, idade):
    dados_usuario = carregar_dados()

    novo_usuario = {"nome": nome,
                    "cpf": cpf,
                    "telefone": telefone,
                    "endereco": endereco,
                    "cep": cep,
                    "email": email,
                    "senha": senha,
                    "idade": idade}

    dados_usuario.append(novo_usuario)
    salvar_dados(dados_usuario)

def listar_usuario():
    dados_usuario = carregar_dados()

    if dados_usuario:
        for users in dados_usuario:
            print(f"Nome: {users['nome']}")
            print(f"CPF: {users['cpf']}")
            print(f"Telefone: {users['telefone']}")
            print(f"Endereço: {users['endereco']}")
            print(f"CEP: {users['cep']}")
            print(f"E-Mail: {users['email']}")
            print(f"Senha: {users['senha']}")
            print(f"Idade: {users['idade']}")

def atualizar_usuario():
    dados_usuario = carregar_dados()

    cpf_att = input("Digite seu CPF: ")
    usuario_encontrado = False

    for users in dados_usuario:
        if users["cpf"] == cpf_att:
            usuario_encontrado = True
            print("Atualizando Dados... \n")
            users['nome'] = input(f"Novo Nome [{users['nome']}]: ") or users['nome']
            users['cpf'] = input(f"Novo CPF [{users['cpf']}]: ") or users['cpf']
            users['telefone'] = input(f"Novo Telefone [{users['telefone']}]: ") or users['telefone']
            users['endereco'] = input(f"Novo Endereço [{users['endereco']}]: ") or users['endereco']
            users['cep'] = input(f"Novo CEP [{users['cep']}]: ") or users['cep']
            users['email'] = input(f"Novo Email [{users['email']}]: ") or users['email']
            users['senha'] = input(f"Nova Senha [{users['senha']}]: ") or users['senha']
            users['idade'] = input(f"Nova Idade [{users['idade']}]: ") or users['idade']

    if usuario_encontrado:
        print("=" * 22)
        print("Atualizando Usuário...")
        print("=" * 22)
        salvar_dados(dados_usuario)
    else:
        print("Usuário Não Encontrado...")

def excluir_usuario():
    dados_usuarios = carregar_dados()

    cpf_excluir = input("Digite seu CPF: ")
    lista_atualizada = [users for users in dados_usuarios if users["cpf"] != cpf_excluir]

    if len(lista_atualizada) < len(dados_usuarios):
        salvar_dados(lista_atualizada)
        print("=" * 22)
        print("Excluindo Usuário...")
        print("=" * 22)
        print(f"Pessoa com CPF {cpf_excluir} Excluido com sucesso")
    else:
        print(f"Pessoa com CPF {cpf_excluir} Não Encontrada")

def login_usuario(cpf, senha):
    dados_usuario = carregar_dados()

    cpf = cpf.strip()
    senha = senha.strip()

    for users in dados_usuario:
        if str(users["cpf"]) == cpf and str(users["senha"]) == senha:
            print(f"Fazendo Login em conta de CPF: {cpf}")
            return True

    print("CPF Ou Senha Incorretos!")
    return False

while True:
    print("=" * 11, cor.CIANO + "LocaSmart" + cor.RESET, "=" * 12)
    print(f"|  [{cor.CIANO}1{cor.RESET}] - Menu ADM                |\n|  [{cor.CIANO}2{cor.RESET}] - Login/Cadastro          |\n|  [{cor.CIANO}0{cor.RESET}] - Sair                    |")
    print("=" * 34)

    opcao_login = int(input(cor.CIANO + "Escolha uma opção: " + cor.RESET))

    if opcao_login == 1:
        login_adm = input("Digite seu Login: ")
        senha_adm = input("Digite sua Senha: ")
        if login_adm == "adm" and senha_adm == "adm123":
            while True:
                print("=" * 7, cor.CIANO + "Menu ADM | LocaSmart" + cor.RESET, "=" * 5)
                print(f"|  [{cor.CIANO}1{cor.RESET}] - Listar Usuários         |\n|  [{cor.CIANO}2{cor.RESET}] - Atualizar Usuário       |\n|  [{cor.CIANO}3{cor.RESET}] - Excluir Usuário         |\n|  [{cor.CIANO}0{cor.RESET}] - Voltar                  |")
                print("=" * 34)
                opcao = int(input(cor.CIANO + "Escolha uma opção: " + cor.RESET))
                match (opcao):
                    case 1:
                        print("=" * 20)
                        print("Listando Usuários...")
                        print("=" * 20)
                        listar_usuario()
                    case 2:
                        atualizar_usuario()
                    case 3:
                        excluir_usuario()
                    case 0:
                        print("=" * 9)
                        print("Saindo...")
                        print("=" * 9)
                        break
        else:
            print("Login ou Senha Inválidos...")

    elif opcao_login == 2:
        print("Sessão Login")
        while True:
            print("=" * 11, cor.CIANO + "LocaSmart" + cor.RESET, "=" * 12)
            print(f"|  [{cor.CIANO}1{cor.RESET}] - Cadastrar Novo Usuário  |\n|  [{cor.CIANO}2{cor.RESET}] - Login                   |\n|  [{cor.CIANO}0{cor.RESET}] - Voltar                  |")
            print("=" * 34)
            opcao = int(input(cor.CIANO + "Escolha uma opção: " + cor.RESET))
            match (opcao):
                case 1:
                    print("-" * 27)
                    print(f"{cor.CIANO}Cadastrando Novo Usuário...{cor.RESET}")
                    print("-" * 27)
                    nome = input("Digite seu nome: ")
                    cpf = input("Digite seu CPF: ")
                    telefone = input("Digite seu telefone: ")
                    endereco = input("Digite seu endereço: ")
                    cep = input("Digite seu CEP: ")
                    email = input("Digite seu email: ")
                    senha = input("Digite sua senha: ")
                    idade = input("Digite sua idade: ")
                    adicionar_usuario(nome, cpf, telefone, endereco, cep, email, senha, idade)
                case 2:
                    cpf = input("Digite seu CPF: ")
                    senha = input("Digite sua Senha: ")
                    login_usuario(cpf, senha)
                case 0:
                    print("=" * 13)
                    print(f"| {cor.CIANO}Saindo...{cor.RESET} |")
                    print("=" * 13)
                    break
        

    elif opcao_login == 0:
        print("=" * 13)
        print(f"| {cor.CIANO}Saindo...{cor.RESET} |")
        print("=" * 13)
        break

    else:
        print(f"{cor.VERMELHO}Opção Inválida!{cor.RESET}")
        