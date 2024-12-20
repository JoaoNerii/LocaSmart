import json
import os
from time import sleep

class Cor:
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    RESET = '\033[0m'



arquivo = os.path.join(os.path.dirname(__file__), 'multas.json')


def carregar_usuarios():
    
    if not os.path.exists(arquivo):
        with open(arquivo, 'w') as f:
            json.dump([], f, indent=4)
    
    
    with open(arquivo, 'r') as f:
        return json.load(f)


def adicionar_multa(cpf, multa):
    usuarios = carregar_usuarios()
    usuarios.append({'cpf': cpf, 'multa': multa})

    with open(arquivo, 'w') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
    print("Multa cadastrada com sucesso")


def listar_multas():
    usuarios = carregar_usuarios()

    if usuarios:
        for usuario in usuarios:
            cpf = usuario.get('cpf', 'CPF não encontrado')
            multa = usuario.get('multa', 'Multa não encontrada')
            print(f"CPF: {cpf}")
            print(f"MULTA: {multa}")
            print("=" * 20)
    else:
        print("Nenhuma multa registrada.")


def atualizar_usuario(cpf, nova_multa):
    usuarios = carregar_usuarios()
    atualizado = False

    for usuario in usuarios:
        if 'cpf' in usuario and usuario['cpf'] == cpf:
            usuario['multa'] = nova_multa
            atualizado = True
            break

    with open(arquivo, 'w') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

    if atualizado:
        print("Usuário atualizado com sucesso!")
    else:
        print("Usuário não encontrado.")


def excluir_usuario(cpf):
    usuarios = carregar_usuarios()
    encontrado = False

    for usuario in usuarios:
        if 'cpf' in usuario and usuario['cpf'] == cpf:
            usuarios.remove(usuario)
            encontrado = True
            break

    with open(arquivo, 'w') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

    if encontrado:
        print("Usuário excluído com sucesso!")
    else:
        print("Usuário não encontrado.")




def menu_inicial():
    print("=" * 13, Cor.CIANO + "LocaSmart" + Cor.RESET, "=" * 14)
    print(f"|  [{Cor.CIANO}1{Cor.RESET}] - Cadastrar nova infração     |\n"
          f"|  [{Cor.CIANO}2{Cor.RESET}] - Listar usuários/multas      |\n"
          f"|  [{Cor.CIANO}3{Cor.RESET}] - Atualizar usuário/multa     |\n"
          f"|  [{Cor.CIANO}4{Cor.RESET}] - Excluir usuário/multa       |\n"
          f"|  [{Cor.CIANO}0{Cor.RESET}] - Sair                        |")
    print("=" * 38)


def main_multas():
    while True:
        menu_inicial()
        opcao = int(input(Cor.CIANO + "Escolha uma opção: " + Cor.RESET))
        
        if opcao == 1:
            cpf = input("Digite o CPF do cliente: ")
            multa = input("Digite a multa a ser cadastrada: ")
            adicionar_multa(cpf, multa)
        
        elif opcao == 2:
            print("=" * 20)
            print("Listando multas...")
            print("=" * 20)
            listar_multas()
        
        elif opcao == 3:
            cpf = input("Digite o CPF do usuário para atualizar a multa: ")
            nova_multa = input("Digite a nova multa: ")
            atualizar_usuario(cpf, nova_multa)
        
        elif opcao == 4:
            cpf = input("Digite o CPF para que a multa seja excluída: ")
            excluir_usuario(cpf)
        
        elif opcao == 0:
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main_multas()

  