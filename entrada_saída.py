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


def validar_placa(placa):
    """Valida se a placa esta no formato AAA-1234."""
    placa = placa.upper().strip()
    return re.fullmatch(r"[A-Z]{3}-\d{4}", placa) is not None


def validar_horario(horario):
    """Valida se o horario esta no formato HH:MM e dentro dos limites permitidos."""
    if re.fullmatch(r"\d{2}:\d{2}", horario) is None:
        return False

    partes = horario.split(":")
    hora = int(partes[0])
    minuto = int(partes[1])

    if hora > 23 or minuto > 59:
        return False

    return True


def converter_horario_para_minutos(horario):
    """Converte um horario no formato HH:MM para minutos totais."""
    partes = horario.split(":")
    hora = int(partes[0])
    minuto = int(partes[1])

    return hora * 60 + minuto


def calcular_valor(minutos):
    """Calcula o valor a pagar com base na permanencia em minutos."""
    if minutos <= 60:
        return 5

    minutos_extras = minutos - 60
    blocos = minutos_extras // 15

    if minutos_extras % 15 != 0:
        blocos += 1

    return 5 + blocos * 2


def buscar_veiculo_por_placa(placa):
    """Procura um veiculo pela placa e devolve o dicionario encontrado."""
    for veiculo in veiculos["registros"]:
        if veiculo["placa"] == placa:
            return veiculo

    return None


def contar_vagas_livres():
    """Conta quantas vagas estao livres no estacionamento."""
    livres = 0

    for situacao in vagas.values():
        if situacao == "livre":
            livres += 1

    return livres


def cadastrar_veiculo():
    """Registra a entrada de um veiculo no estacionamento."""
    if len(veiculos["registros"]) >= CAPACIDADE_MAXIMA:
        print("Estacionamento lotado. Nao foi possivel cadastrar.")
        return

    placa = input("Digite a placa do carro (ABC-1234): ").upper().strip()

    if not validar_placa(placa):
        print("Placa invalida. Use o formato ABC-1234.")
        return

    if buscar_veiculo_por_placa(placa) is not None:
        print("Essa placa ja esta cadastrada no estacionamento.")
        return

    horario = input("Digite o horario em qual ele foi registrado (HH:MM): ").strip()

    if re.fullmatch(r"\d{2}:\d{2}", horario) is None:
        print("Horario invalido. Use o formato HH:MM (exemplo 08:30).")
        return

    if not validar_horario(horario):
        print("Horario invalido. Hora entre 00 e 23, minuto entre 00 e 59.")
        return

    tipo_veiculo = input("Digite o tipo do veiculo que esta sendo registrado (carro / moto): ").lower().strip()

    if tipo_veiculo != "carro" and tipo_veiculo != "moto":
        tipo_veiculo = "carro"

    try:
        vaga_escolhida = int(input("Digite a vaga na qual o carro foi estacionado: "))
    except ValueError:
        print("Digite um numero valido para a vaga.")
        return

    if vaga_escolhida not in vagas:
        print("Essa vaga nao existe, tente novamente.")
        return

    if vagas[vaga_escolhida] == "ocupada":
        print(f"A vaga {vaga_escolhida} ja esta ocupada.")
        return

    vagas[vaga_escolhida] = "ocupada"

    novo_veiculo = {
        "placa": placa,
        "horario": horario,
        "tipo_veiculo": tipo_veiculo,
        "vaga_escolhida": vaga_escolhida
    }

    veiculos["registros"].append(novo_veiculo)

    print(f"Veiculo da placa {placa}, foi registrado com sucesso na vaga {vaga_escolhida}.")


def remover_veiculo():
    """Registra a saida de um veiculo, calcula permanencia, valor e libera a vaga."""
    print("-" * 20)
    print("Saida de veiculos")

    placa_saida = input("Digite a placa do veiculo que esta saindo: ").upper().strip()

    if not validar_placa(placa_saida):
        print("Placa invalida. Use o formato ABC-1234.")
        return

    veiculo_encontrado = buscar_veiculo_por_placa(placa_saida)

    if veiculo_encontrado is None:
        print("Placa nao encontrada no estacionamento.")
        return

    horario_saida = input("Digite o horario de saida (HH:MM): ").strip()

    if re.fullmatch(r"\d{2}:\d{2}", horario_saida) is None:
        print("Horario invalido. Use o formato HH:MM (exemplo 08:30).")
        return

    if not validar_horario(horario_saida):
        print("Horario invalido. Hora entre 00 e 23, minuto entre 00 e 59.")
        return

    horario_entrada = veiculo_encontrado["horario"]

    entrada_minutos = converter_horario_para_minutos(horario_entrada)
    saida_minutos = converter_horario_para_minutos(horario_saida)

    permanencia = saida_minutos - entrada_minutos

    if permanencia < 0:
        print("O horario de saida nao pode ser anterior ao de entrada.")
        return

    valor = calcular_valor(permanencia)

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


def listar_veiculos():
    """Lista todos os veiculos atualmente estacionados."""
    if len(veiculos["registros"]) == 0:
        print("Nao ha veiculos estacionados.")
        return

    print("-" * 60)
    print("VEICULOS ESTACIONADOS")
    print("-" * 60)

    for veiculo in veiculos["registros"]:
        print(f"Placa: {veiculo['placa']}")
        print(f"Entrada: {veiculo['horario']}")
        print(f"Tipo: {veiculo['tipo_veiculo']}")
        print(f"Vaga: {veiculo['vaga_escolhida']}")
        print("-" * 60)


def consultar_vagas():
    """Mostra a quantidade de vagas livres e a situacao de cada vaga."""
    livres = contar_vagas_livres()

    print(f"Vagas disponiveis: {livres}")

    for numero_vaga, situacao in vagas.items():
        print(f"Vaga {numero_vaga}: {situacao}")


def main():
    """Controla o menu principal do sistema."""
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
            cadastrar_veiculo()

        elif escolha == "2":
            remover_veiculo()

        elif escolha == "3":
            listar_veiculos()

        elif escolha == "4":
            consultar_vagas()

        elif escolha == "5":
            print("Programa encerrado.")
            break

        else:
            print("Opcao invalida. Escolha um numero do menu.")


if __name__ == "__main__":
    main()
