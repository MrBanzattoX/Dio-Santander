import os
import platform
import re
import time

clientes = []
contas = []
numero_conta_corrente = 1


def limpar_tela():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def pausar(mensagem="➡️ Pressione Enter para continuar..."):
    input(f"\n{mensagem}")
    limpar_tela()


def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf, peso):
        soma = sum(int(d) * p for d, p in zip(cpf, range(peso, 1, -1)))
        digito = (soma * 10) % 11
        return 0 if digito == 10 else digito

    digito1 = calcular_digito(cpf[:9], 10)
    digito2 = calcular_digito(cpf[:10], 11)

    return cpf[-2:] == f"{digito1}{digito2}"


def cliente_existe(cpf):
    return any(cliente['cpf'] == cpf for cliente in clientes)


def cadastrar_cliente():
    print("👤 Cadastro de Cliente")
    nome = input("Nome: ")
    cpf = input("CPF (somente números): ")

    if not validar_cpf(cpf):
        print("❌ CPF inválido.")
        time.sleep(2)
        return
    if cliente_existe(cpf):
        print("⚠️ CPF já cadastrado.")
        time.sleep(2)
        return

    endereco = input("Endereço (Rua, Número): ")
    cidade = input("Cidade: ")
    estado = input("Estado (sigla): ")

    clientes.append({
        "nome": nome,
        "cpf": cpf,
        "endereco": endereco,
        "cidade": cidade,
        "estado": estado
    })

    print("✅ Cliente cadastrado com sucesso!")
    time.sleep(2)


def cadastrar_conta():
    global numero_conta_corrente
    print("🏦 Abertura de Conta Corrente")
    cpf = input("Digite o CPF do cliente: ")

    if not cliente_existe(cpf):
        print("❌ Cliente não encontrado.")
        time.sleep(2)
        return

    numero = f"{numero_conta_corrente:06d}"
    contas.append({
        "agencia": "0001",
        "numero": numero,
        "cpf": cpf,
        "saldo": 0.0,
        "movimentacoes": []
    })
    numero_conta_corrente += 1
    print(f"✅ Conta criada com sucesso! Número: {numero}")
    time.sleep(2)


def encontrar_contas_por_cpf(cpf):
    return [c for c in contas if c['cpf'] == cpf]


def escolher_conta(cpf):
    contas_cliente = encontrar_contas_por_cpf(cpf)
    if not contas_cliente:
        print("❌ Nenhuma conta encontrada para este CPF.")
        time.sleep(2)
        return None

    print("Contas disponíveis:")
    for i, conta in enumerate(contas_cliente):
        print(f"{i + 1}. Conta {conta['numero']} - Saldo: R$ {conta['saldo']:.2f}")
    try:
        escolha = int(input("Escolha a conta (número): ")) - 1
        return contas_cliente[escolha]
    except (IndexError, ValueError):
        print("⚠️ Escolha inválida.")
        time.sleep(2)
        return None


def sacar():
    print("💸 Saque")
    cpf = input("CPF: ")
    conta = escolher_conta(cpf)
    if not conta:
        return

    valor = float(input("Valor do saque: "))
    if valor <= 0:
        print("⚠️ Valor deve ser positivo.")
    elif valor > conta['saldo']:
        print("❌ Saldo insuficiente.")
    else:
        conta['saldo'] -= valor
        conta['movimentacoes'].append(f"Saque: -R$ {valor:.2f}")
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
    time.sleep(2)


def depositar():
    print("💰 Depósito")
    cpf = input("CPF: ")
    conta = escolher_conta(cpf)
    if not conta:
        return

    valor = float(input("Valor do depósito: "))
    if valor <= 0:
        print("⚠️ Valor deve ser positivo.")
    else:
        conta['saldo'] += valor
        conta['movimentacoes'].append(f"Depósito: +R$ {valor:.2f}")
        print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    time.sleep(2)


def visualizar_saldo():
    print("📄 Extrato e Saldo")
    cpf = input("CPF: ")
    contas_cliente = encontrar_contas_por_cpf(cpf)
    if not contas_cliente:
        print("❌ Nenhuma conta encontrada.")
        time.sleep(2)
        return

    for conta in contas_cliente:
        print(f"\n📌 Conta {conta['numero']} - Agência {conta['agencia']}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("Movimentações:")
        if conta['movimentacoes']:
            for m in conta['movimentacoes']:
                print(" •", m)
        else:
            print(" (Sem movimentações)")
    pausar()


def exibir_clientes():
    print("👥 Lista de Clientes")
    if not clientes:
        print("📭 Nenhum cliente cadastrado.")
    else:
        for cliente in clientes:
            print(f"{cliente['nome']} - CPF: {cliente['cpf']} - {cliente['endereco']} - {cliente['cidade']}/{cliente['estado']}")
    pausar()


def exibir_contas():
    print("🏦 Lista de Contas Correntes")
    if not contas:
        print("📭 Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            print(f"Conta {conta['numero']} - Agência {conta['agencia']} - CPF: {conta['cpf']} - Saldo: R$ {conta['saldo']:.2f}")
    pausar()


def menu():
    while True:
        limpar_tela()
        print("╔══════════════════════════════════════╗")
        print("║     BANCO DIGITAL BANZODROID 🏦      ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1 - Cadastrar cliente                ║")
        print("║ 2 - Cadastrar conta corrente         ║")
        print("║ 3 - Sacar                            ║")
        print("║ 4 - Depositar                        ║")
        print("║ 5 - Visualizar saldo e extrato       ║")
        print("║ 6 - Exibir clientes                  ║")
        print("║ 7 - Exibir contas                    ║")
        print("║ 0 - Sair                             ║")
        print("╚══════════════════════════════════════╝")

        opcao = input("👉 Escolha uma opção: ").strip()
        limpar_tela()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_conta()
        elif opcao == "3":
            sacar()
        elif opcao == "4":
            depositar()
        elif opcao == "5":
            visualizar_saldo()
        elif opcao == "6":
            exibir_clientes()
        elif opcao == "7":
            exibir_contas()
        elif opcao == "0":
            print("🏁 Encerrando o sistema... Obrigado por usar o BanzoDroid!")
            time.sleep(2)
            break
        else:
            print("❌ Opção inválida.")
            time.sleep(2)


# Inicia o sistema
menu()
