def movimentar_saldo(saldo, operacao, valor):
    if operacao == "deposito":
        saldo += valor
        print(f"💰 Depósito realizado com sucesso. Novo saldo: R$ {saldo:.2f}\n")
    elif operacao == "saque":
        if valor > saldo:
            print("❌ Saldo insuficiente para saque.\n")
        else:
            saldo -= valor
            print(f"💸 Saque realizado com sucesso. Novo saldo: R$ {saldo:.2f}\n")
    else:
        print("⚠️ Operação inválida. Digite 'deposito' ou 'saque'.\n")
    
    return saldo

# Saldo inicial
saldo_atual = 2500.00
print("Bem-vindo ao Banco Digital BanzoDroid!")
print(f"Seu saldo inicial é: R$ {saldo_atual:.2f}\n")

# Loop principal
while True:
    operacao = input("Digite a operação (deposito, saque ou sair): ").strip().lower()

    if operacao == "sair":
        print(f"\n🏁 Operações encerradas. Saldo final: R$ {saldo_atual:.2f}")
        break

    valor_str = input("Digite o valor: ")

    try:
        valor = float(valor_str)
        if valor <= 0:
            print("⚠️ O valor deve ser maior que zero.\n")
            continue
        saldo_atual = movimentar_saldo(saldo_atual, operacao, valor)
    except ValueError:
        print("⚠️ Valor inválido. Digite um número válido.\n")
