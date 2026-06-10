import re
veiculos = {
    "registros": []
}

vagas = {
    1: "livre",
    2: "livre",
    3: "livre",
    4: "livre",
    5: "livre",
    6: "livre",
    7: "livre",
    8: "livre",
    9: "livre",
    10: "livre",
}


while True:
    print("-"*30)
    print("Escolha uma das opçoes abaixo")
    print()
    print("1 - Entrada de veiculos")
    print("2 - Saida de veiculos")
    print("3 - Listar veiculos selecionados")
    print("4 - Consultar vagas disponiveis")
    print("5 - Sair")
    print()
    print("-"*30)
    escolha = input("Opçao deseja: ")

    if escolha == "1":

        while True:
            placa = input("Digite a placa do carro (ABC-1234): ")
            
            if re.fullmatch(r"[A-Z]{3}-\d{4}", placa.upper()):
                print("Placa registrada com sucesso!")
             
            else:
                print("Placa digitada no formato incorreto")
                print("Exemplo de modelo correto ABC-1234")
                continue
            
            horario = input("Digite o horario em qual ele foi registrado (HH:MM): ")

            if re.fullmatch(r"\d{2}:\d{2}", horario):
                print("Horario registrado com sucesso")
            
            else:
                print("Horario no formato errado formato correto HH:MM")
                continue

            tipo_veiculo = input("Digite o tipo do veiculo que esta sendo registrado: ")
            vaga_escolhida = int(input("Digite a vaga na qual o carro foi estacionado: "))

            if vaga_escolhida not in vagas:
                print("Essa vaga nao existe, tente novamente")
                continue
                
            if vagas[vaga_escolhida] == "ocupada":
                print(f"A vaga {vaga_escolhida} ja esta ocupada")
                continue

            vagas[vaga_escolhida] = "ocupada"

            novo_veiculo = {
                "placa": placa.upper(),
                "horario": horario,
                "tipo_veiculo": tipo_veiculo,
                "vaga_escolhida": vaga_escolhida
            }

            veiculos["registros"].append(novo_veiculo)

            print(f"Veiculo da placa {placa.upper()}, foi registrado com sucesso na vaga {vaga_escolhida}")

    elif escolha == "2":
        print("-"*20)
        print("Saida de veiculos")

    elif escolha == "3":

        if len(veiculos["registros"]) == 0:
            print("Nenhum veiculo cadastrado")

        else:
            for veiculo in veiculos["registros"]:
                print("-" * 30)
                print(f"Placa: {veiculo['placa']}")
                print(f"Horario: {veiculo['horario']}")
                print(f"Tipo do veiculo: {veiculo['tipo_veiculo']}")
                print(f"Vaga: {veiculo['vaga_escolhida']}")
                print()
        