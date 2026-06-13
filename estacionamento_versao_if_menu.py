import re

CAPACIDADE_MAXIMA = 10

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
    print("-" * 30)
    print("Escolha uma das opcoes abaixo")
    print()
    print("1 - Entrada de veiculos")
    print("2 - Saida de veiculos")
    print("3 - Listar veiculos estacionados")
    print("4 - Consultar vagas disponiveis")
    print("5 - Sair")
    print()
    print("-" * 30)

    escolha = input("Opcao desejada: ").strip()

    if escolha == "1":
        # ENTRADA DE VEICULO

        if len(veiculos["registros"]) >= CAPACIDADE_MAXIMA:
            print("Estacionamento lotado. Nao foi possivel cadastrar.")
            continue

        placa = input("Digite a placa do carro (ABC-1234): ").upper().strip()

        if re.fullmatch(r"[A-Z]{3}-\d{4}", placa) is None:
            print("Placa invalida. Use o formato ABC-1234.")
            continue

        placa_repetida = False

        for veiculo in veiculos["registros"]:
            if veiculo["placa"] == placa:
                placa_repetida = True
                break

        if placa_repetida:
            print("Essa placa ja esta cadastrada no estacionamento.")
            continue

        horario = input("Digite o horario em qual ele foi registrado (HH:MM): ").strip()

        if re.fullmatch(r"\d{2}:\d{2}", horario) is None:
            print("Horario invalido. Use o formato HH:MM (exemplo 08:30).")
            continue

        partes_horario = horario.split(":")
        hora = int(partes_horario[0])
        minuto = int(partes_horario[1])

        if hora > 23 or minuto > 59:
            print("Horario invalido. Hora entre 00 e 23, minuto entre 00 e 59.")
            continue

        tipo_veiculo = input("Digite o tipo do veiculo que esta sendo registrado (carro / moto): ").lower().strip()

        if tipo_veiculo != "carro" and tipo_veiculo != "moto":
            tipo_veiculo = "carro"

        try:
            vaga_escolhida = int(input("Digite a vaga na qual o carro foi estacionado: "))
        except ValueError:
            print("Digite um numero valido para a vaga.")
            continue

        if vaga_escolhida not in vagas:
            print("Essa vaga nao existe, tente novamente.")
            continue

        if vagas[vaga_escolhida] == "ocupada":
            print(f"A vaga {vaga_escolhida} ja esta ocupada.")
            continue

        vagas[vaga_escolhida] = "ocupada"

        novo_veiculo = {
            "placa": placa,
            "horario": horario,
            "tipo_veiculo": tipo_veiculo,
            "vaga_escolhida": vaga_escolhida
        }

        veiculos["registros"].append(novo_veiculo)

        print(f"Veiculo da placa {placa}, foi registrado com sucesso na vaga {vaga_escolhida}.")

    elif escolha == "2":
        # SAIDA DE VEICULO

        print("-" * 20)
        print("Saida de veiculos")

        placa_saida = input("Digite a placa do veiculo que esta saindo: ").upper().strip()

        if re.fullmatch(r"[A-Z]{3}-\d{4}", placa_saida) is None:
            print("Placa invalida. Use o formato ABC-1234.")
            continue

        veiculo_encontrado = None

        for veiculo in veiculos["registros"]:
            if veiculo["placa"] == placa_saida:
                veiculo_encontrado = veiculo
                break

        if veiculo_encontrado is None:
            print("Placa nao encontrada no estacionamento.")
            continue

        horario_saida = input("Digite o horario de saida (HH:MM): ").strip()

        if re.fullmatch(r"\d{2}:\d{2}", horario_saida) is None:
            print("Horario invalido. Use o formato HH:MM (exemplo 08:30).")
            continue

        partes_saida = horario_saida.split(":")
        hora_saida = int(partes_saida[0])
        minuto_saida = int(partes_saida[1])

        if hora_saida > 23 or minuto_saida > 59:
            print("Horario invalido. Hora entre 00 e 23, minuto entre 00 e 59.")
            continue

        horario_entrada = veiculo_encontrado["horario"]

        partes_entrada = horario_entrada.split(":")
        hora_entrada = int(partes_entrada[0])
        minuto_entrada = int(partes_entrada[1])

        entrada_minutos = hora_entrada * 60 + minuto_entrada
        saida_minutos = hora_saida * 60 + minuto_saida

        permanencia = saida_minutos - entrada_minutos

        if permanencia < 0:
            print("O horario de saida nao pode ser anterior ao de entrada.")
            continue

        if permanencia <= 60:
            valor = 5
        else:
            minutos_extras = permanencia - 60
            blocos = minutos_extras // 15

            if minutos_extras % 15 != 0:
                blocos += 1

            valor = 5 + blocos * 2

        vaga_liberada = veiculo_encontrado["vaga_escolhida"]
        vagas[vaga_liberada] = "livre"
        veiculos["registros"].remove(veiculo_encontrado)

        print()
        print(f"Placa: {placa_saida}")
        print(f"Entrada: {horario_entrada}")
        print(f"Saida: {horario_saida}")
        print(f"Permanencia: {permanencia} min")
        print(f"Total a pagar: R$ {valor:.2f}".replace(".", ","))
        print(f"Vaga {vaga_liberada} liberada.")

    elif escolha == "3":
        # LISTAGEM DE VEICULOS

        if len(veiculos["registros"]) == 0:
            print("Nao ha veiculos estacionados.")
            continue

        print("-" * 60)
        print("VEICULOS ESTACIONADOS")
        print("-" * 60)

        for veiculo in veiculos["registros"]:
            print(f"Placa: {veiculo['placa']}")
            print(f"Entrada: {veiculo['horario']}")
            print(f"Tipo: {veiculo['tipo_veiculo']}")
            print(f"Vaga: {veiculo['vaga_escolhida']}")
            print("-" * 60)

    elif escolha == "4":
        # CONSULTA DE VAGAS

        livres = 0

        for situacao in vagas.values():
            if situacao == "livre":
                livres += 1

        print(f"Vagas disponiveis: {livres}")

        for numero_vaga, situacao in vagas.items():
            print(f"Vaga {numero_vaga}: {situacao}")

    elif escolha == "5":
        print("Programa encerrado.")
        break

    else:
        print("Opcao invalida. Escolha um numero do menu.")
