import re


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


def buscar_veiculo_por_placa(placa, veiculos):
    """Procura um veiculo pela placa e devolve o dicionario encontrado."""
    for veiculo in veiculos["registros"]:
        if veiculo["placa"] == placa:
            return veiculo

    return None


def saida_de_veiculo(veiculos, vagas):
    """
    Registra a saida de um veiculo.

    Esta funcao:
    1. Pede a placa do veiculo.
    2. Procura a placa na lista de registros.
    3. Pede o horario de saida.
    4. Calcula a permanencia.
    5. Calcula o valor a pagar.
    6. Libera a vaga.
    7. Remove o veiculo da lista.
    """
    print("-" * 20)
    print("Saida de veiculos")

    placa_saida = input("Digite a placa do veiculo que esta saindo: ").upper().strip()

    veiculo_encontrado = buscar_veiculo_por_placa(placa_saida, veiculos)

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


# Exemplo de como chamar no arquivo principal:
#
# elif escolha == "2":
#     saida_de_veiculo(veiculos, vagas)
