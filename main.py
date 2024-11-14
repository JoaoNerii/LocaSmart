from CRUD_Devolucao import *
from CRUD_Locacao import *
from CRUD_Multas import *
from CRUD_Registro import *
from CRUD_Seguro import *



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
                    usuarioLogado = login_usuario(cpf, senha)
                    if usuarioLogado:
                        locar_carro()
                    else:
                        ("CPF Ou Senha Incorretos...")
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
        