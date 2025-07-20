import os
import textwrap
import time
from colorama import init, Fore, Style

init(autoreset=True)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def efeito_digitando(texto, delay=0.03, cor=Fore.WHITE):
    """Imprime texto com efeito de digitação."""
    for char in texto:
        print(cor + char, end="", flush=True)
        time.sleep(delay)
    print()

def carregamento():
    """Mostra uma tela de carregamento animada."""
    limpar_tela()
    efeito_digitando(Fore.CYAN + "Iniciando o sistema do Banco Digital Banzatto...\n", 0.04)
    for i in range(1, 6):
        print(Fore.YELLOW + f"Carregando{'.' * i}")
        time.sleep(0.4)
        limpar_tela()
    efeito_digitando(Fore.GREEN + "Sistema carregado com sucesso!\n", 0.04)
    time.sleep(1)

def tela_boas_vindas():
    """Exibe o banner inicial do banco."""
    limpar_tela()
    banner = f"""
{Fore.CYAN}==============================================
{Fore.YELLOW}      BEM-VINDO AO BANCO DIGITAL BANZATTO
{Fore.CYAN}==============================================
{Fore.WHITE}Seu banco moderno, rápido e seguro.
{Fore.GREEN}Gerencie sua conta de forma simples e prática!
{Fore.CYAN}==============================================
"""
    print(banner)
    input(Fore.MAGENTA + "\nPressione Enter para acessar o menu...")

def menu():
    limpar_tela()
    print(Fore.CYAN + "=" * 40)
    print(Fore.YELLOW + "           MENU PRINCIPAL           ")
    print(Fore.CYAN + "=" * 40)
    print(Fore.GREEN + "[d] " + Fore.WHITE + "Depositar")
    print(Fore.GREEN + "[s] " + Fore.WHITE + "Sacar")
    print(Fore.GREEN + "[e] " + Fore.WHITE + "Extrato")
    print(Fore.GREEN + "[nc]" + Fore.WHITE + " Nova conta")
    print(Fore.GREEN + "[lc]" + Fore.WHITE + " Listar contas")
    print(Fore.GREEN + "[nu]" + Fore.WHITE + " Novo usuário")
    print(Fore.RED + "[q] " + Fore.WHITE + "Sair")
    print(Fore.CYAN + "=" * 40)
    return input(Fore.YELLOW + "Escolha uma opção: " + Fore.WHITE)

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(Fore.GREEN + "\n=== Depósito realizado com sucesso! ===")
    else:
        print(Fore.RED + "\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print(Fore.RED + "\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print(Fore.RED + "\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print(Fore.RED + "\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(Fore.GREEN + "\n=== Saque realizado com sucesso! ===")

    else:
        print(Fore.RED + "\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print(Fore.CYAN + "\n" + "=" * 40)
    print(Fore.YELLOW + "               EXTRATO               ")
    print(Fore.CYAN + "=" * 40)
    print(Fore.WHITE + ("Não foram realizadas movimentações." if not extrato else extrato))
    print(Fore.GREEN + f"\nSaldo:\t\tR$ {saldo:.2f}")
    print(Fore.CYAN + "=" * 40)
    input(Fore.MAGENTA + "\nPressione Enter para voltar ao menu...")

def criar_usuario(usuarios):
    cpf = input(Fore.CYAN + "Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.RED + "\n@@@ Já existe usuário com esse CPF! @@@")
        input(Fore.MAGENTA + "\nPressione Enter para continuar...")
        return

    nome = input(Fore.CYAN + "Informe o nome completo: ")
    data_nascimento = input(Fore.CYAN + "Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(Fore.CYAN + "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(Fore.GREEN + "\n=== Usuário criado com sucesso! ===")
    input(Fore.MAGENTA + "\nPressione Enter para continuar...")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input(Fore.CYAN + "Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.GREEN + "\n=== Conta criada com sucesso! ===")
        input(Fore.MAGENTA + "\nPressione Enter para continuar...")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print(Fore.RED + "\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    input(Fore.MAGENTA + "\nPressione Enter para continuar...")

def listar_contas(contas):
    print(Fore.CYAN + "\n" + "=" * 60)
    print(Fore.YELLOW + "              LISTA DE CONTAS              ")
    print(Fore.CYAN + "=" * 60)
    for conta in contas:
        linha = f"""\
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
        """
        print(Fore.WHITE + "-" * 60)
        print(Fore.WHITE + textwrap.dedent(linha))
    print(Fore.CYAN + "=" * 60)
    input(Fore.MAGENTA + "\nPressione Enter para voltar ao menu...")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    carregamento()
    tela_boas_vindas()

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input(Fore.CYAN + "Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
            input(Fore.MAGENTA + "\nPressione Enter para continuar...")

        elif opcao == "s":
            valor = float(input(Fore.CYAN + "Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            input(Fore.MAGENTA + "\nPressione Enter para continuar...")

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            limpar_tela()
            efeito_digitando(Fore.YELLOW + "Obrigado por usar o Banco Digital Banzatto! Até logo!\n", 0.04)
            break

        else:
            print(Fore.RED + "Operação inválida, por favor selecione novamente a operação desejada.")
            input(Fore.MAGENTA + "\nPressione Enter para continuar...")

main()
