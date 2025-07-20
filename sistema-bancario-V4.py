import os
import textwrap
import time
import sys
from colorama import init, Fore, Style

# Inicializa o colorama com conversão para Windows e fallback
init(autoreset=True, convert=True, strip=False)

# Detecta se o terminal suporta cores
SUPORTA_CORES = sys.stdout.isatty()

# Se o terminal não suportar, as cores viram strings vazias
if not SUPORTA_CORES:
    Fore.CYAN = Fore.YELLOW = Fore.GREEN = Fore.RED = Fore.MAGENTA = Fore.WHITE = ""
    Style.RESET_ALL = ""

# Beep no Windows (não funciona em Linux)
def beep(frequencia=1000, duracao=200):
    if os.name == 'nt':
        import winsound
        winsound.Beep(frequencia, duracao)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def efeito_digitando(texto, delay=0.03, cor=Fore.WHITE):
    """Imprime texto com efeito de digitação (desativa cor se não suportar)."""
    for char in texto:
        print((cor if SUPORTA_CORES else "") + char, end="", flush=True)
        time.sleep(delay)
    print()

def carregamento():
    """Tela de carregamento com beep."""
    limpar_tela()
    efeito_digitando(Fore.CYAN + "Iniciando o sistema do Banco Digital Banzatto...\n", 0.04)
    beep(800, 150)
    for i in range(1, 6):
        print(Fore.YELLOW + f"Carregando{'.' * i}")
        time.sleep(0.4)
        limpar_tela()
    beep(1000, 200)
    efeito_digitando(Fore.GREEN + "Sistema carregado com sucesso!\n", 0.04)
    time.sleep(1)

def tela_boas_vindas():
    """Tela inicial com banner."""
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
    beep(1200, 200)
    input(Fore.MAGENTA + "\nPressione Enter para acessar o menu...")

def tela_despedida(saldo, extrato):
    """Mostra recibo final antes de sair."""
    limpar_tela()
    efeito_digitando(Fore.YELLOW + "Gerando seu recibo final...\n", 0.04)
    time.sleep(1)
    beep(1000, 150)
    limpar_tela()

    print(Fore.CYAN + "=" * 40)
    print(Fore.YELLOW + "       BANCO DIGITAL BANZATTO")
    print(Fore.CYAN + "=" * 40)
    print(Fore.WHITE + ("Sem movimentações registradas." if not extrato else extrato))
    print(Fore.GREEN + f"\nSaldo final:\tR$ {saldo:.2f}")
    print(Fore.CYAN + "=" * 40)
    efeito_digitando(Fore.GREEN + "\nObrigado por utilizar nossos serviços!\n", 0.04)
    beep(800, 200)
    time.sleep(1)

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
        beep(1200, 100)
    else:
        print(Fore.RED + "\n@@@ Operação falhou! O valor informado é inválido. @@@")
        beep(400, 200)
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print(Fore.RED + "\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        beep(400, 200)

    elif excedeu_limite:
        print(Fore.RED + "\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        beep(400, 200)

    elif excedeu_saques:
        print(Fore.RED + "\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        beep(400, 200)

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(Fore.GREEN + "\n=== Saque realizado com sucesso! ===")
        beep(1200, 100)

    else:
        print(Fore.RED + "\n@@@ Operação falhou! O valor informado é inválido. @@@")
        beep(400, 200)

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print(Fore.CYAN + "\n" + "=" * 40)
    print(Fore.YELLOW + "               EXTRATO               ")
    print(Fore.CYAN + "=" * 40)
    print(Fore.WHITE + ("Não foram realizadas movimentações." if not extrato else extrato))
    print(Fore.GREEN + f"\nSaldo atual:\tR$ {saldo:.2f}")
    print(Fore.CYAN + "=" * 40)
    beep(800, 100)
    input(Fore.MAGENTA + "\nPressione Enter para voltar ao menu...")

def criar_usuario(usuarios):
    cpf = input(Fore.CYAN + "Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.RED + "\n@@@ Já existe usuário com esse CPF! @@@")
        beep(400, 200)
        input(Fore.MAGENTA + "\nPressione Enter para continuar...")
        return

    nome = input(Fore.CYAN + "Informe o nome completo: ")
    data_nascimento = input(Fore.CYAN + "Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(Fore.CYAN + "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(Fore.GREEN + "\n=== Usuário criado com sucesso! ===")
    beep(1200, 100)
    input(Fore.MAGENTA + "\nPressione Enter para continuar...")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input(Fore.CYAN + "Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.GREEN + "\n=== Conta criada com sucesso! ===")
        beep(1200, 100)
        input(Fore.MAGENTA + "\nPressione Enter para continuar...")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print(Fore.RED + "\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    beep(400, 200)
    input(Fore.MAGENTA + "\nPressione Enter para continuar...")

def listar_contas(contas):
    print(Fore.CYAN + "\n" + "=" * 60)
    print(Fore.YELLOW + "              LISTA DE CONTAS              ")
    print(Fore.CYAN + "=" * 60)
    if not contas:
        print(Fore.WHITE + "Nenhuma conta cadastrada.")
    for conta in contas:
        linha = f"""\
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
        """
        print(Fore.WHITE + "-" * 60)
        print(Fore.WHITE + textwrap.dedent(linha))
    print(Fore.CYAN + "=" * 60)
    beep(800, 100)
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
            tela_despedida(saldo, extrato)
            break

        else:
            print(Fore.RED + "Operação inválida, por favor selecione novamente a operação desejada.")
            beep(400, 200)
            input(Fore.MAGENTA + "\nPressione Enter para continuar...")

main()
