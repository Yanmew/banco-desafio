import sys
import textwrap

def menu():
    menu ="""
$-----$ BANCO IMAGINÁRIO $-----$
#                              #
#       [1] - Depósito         #
#       [2] - Saque            #
#       [3] - Extrato          #
#       [4] - Novo Usuário     #
#       [5] - Criar Conta      #
#       [6] - Listar Contas    #
#       [0] - Cancelar         #
#                              #
$------------------------------$

=> """
    return input(textwrap.dedent(menu))

def deposito(saldo, valor, extrato, /):
    if valor >= 0:
        saldo += valor
        extrato += f"Depósito:\t+R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
        print(f"\n=== Saldo atual: {saldo}! ===")
    
    else:
        print("Valor inválido. Digite um valor acima de 0 (zero)")
    
    return saldo, extrato  

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("\nERRO: Você não tem saldo suficiente! Por favor, realize um depósito primeiro.")
    elif excedeu_limite:
        print(f"\nERRO: Você não tem limite de saque o suficiente para realizar esta operação.\n O seu limite atual é {limite}\n Consulte seu gerente para aumentar o seu limite.\n")
    elif excedeu_saques:
        exit_input = input(f"\n Você atingiu o limite máximo de {limite_saques} saques por dia. Pressione qualquer botão para continuar...")
    elif valor >= 0:
        saldo -= valor
        extrato += f"Saque:\t\t-R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n$===$ Saque realizado com sucesso! $===$")
        print(f"\n$===$ Saldo atual: {saldo}! $===$")
        
        if numero_saques >= 3:
            exit_input = input(f"\n Você atingiu o limite máximo de {limite_saques} saques por dia. Pressione qualquer botão para continuar...")
    else:
        print("Valor inválido. Digite um valor entre 1 (um) e 500 (quinhentos).")
    
    return saldo, extrato, numero_saques
        

def exibir_extrato(saldo, /, *, extrato):
    print("\n$================$ EXTRATO $================$")
    print("\nNão foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}\n")
    print("$=============================================$")
    
def criar_usuario(usuarios):
    cpf = input("Digite o seu número de CPF sem pontos ou traços: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\nERRO: Já existe um usuário com esse CPF. Talvez você quis criar uma conta e não um usuário?")
        return
    
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd--mm-aaaa): ")
    endereco = input("Endereço completo (logradouro, número, bairro, cidade/estado): ")
    
    usuarios.append({"nome": nome, "data_nascimento" : data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("$===$ Usuário criado com sucesso! $===$")
    exit_input = input(f"\nPressione qualquer botão para continuar...")
    

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None    

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n $=====$ Conta criada com sucesso! $=====$")
        exit_input = input(f"\nPressione qualquer botão para continuar...")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nERRO: Usuário não encontrado no nosso registro. Tente novamente.")
    
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            Conta Corrente:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))



def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    contador = 0
    usuarios = []
    contas = []
    exit_input = False

    while True:
        opcao = menu()

        if opcao == "1":
                
            continuar = 1
            print("$=====$ DEPÓSITO $=====$")
            
            while continuar  == 1:
                try:
                    valor = float(input("Digite o valor a ser depositado: "))

                    saldo, extrato = deposito(saldo, valor, extrato)
                    continuar = -1
                    while continuar not in [0, 1]:
                        continuar = int(input("""Você deseja realizar mais um depósito?
[1] Sim
[0] Não
=> """))
                except ValueError:
                    print("Digite um número válido.")


        elif opcao == "2":
            continuar = 1
            
            print("$=====$ SAQUE $=====$")
            while continuar == 1:
                try:
                    valor = float(input("Digite o valor a sacar: "))
                    saldo, extrato, numero_saques = saque(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
       
                    continuar = -1
                    if continuar != 1 and numero_saques < 3:
                        while continuar not in [0, 1]:
                            continuar = int(input("""Você deseja realizar mais um saque?
[1] Sim
[0] Não
=> """))
                except ValueError:
                    print("Digite um número válido.")

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
            exit_input = input(f"\nPressione qualquer botão para continuar...")

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            exit_input = input(f"\nPressione qualquer botão para continuar...")

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)
            exit_input = input(f"\nPressione qualquer botão para continuar...")

        elif opcao == "0":
            print("""
$------CANCELAR------$
#                    #
# O Banco Imaginário #
#      Agradece      #
#                    #
$--------------------$

""")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()