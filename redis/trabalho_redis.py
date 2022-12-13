import random
from datetime import date, timedelta

from pyredis import Client

client = Client(host="localhost")


def numerosmegasena():
    resultado = []
    i = 1
    while i < 7:
        resultado.append(random.randint(1, 61))
        i += 1

    return resultado


def numerosganhadores():
    return random.randint(0, 21)


def criaregistro():
    data = date(1999, 10, 13)
    atual = date(2022, 10, 10)
    i = 1

    client.bulk_start()

    while data < atual:
        if data.weekday() != 2 and data.weekday() != 5:
            data += timedelta(days=1)
            continue

        megasena = str(numerosmegasena())
        ganhadores = numerosganhadores()
        chave = f'sorteio:{i}:{data}'

        client.hmset(chave, "numero_sorteio", i)
        client.hmset(chave, "data", str(data))
        client.hmset(chave, "numeros", megasena)
        client.hmset(chave, "ganhadores", ganhadores)

        i += 1
        data += timedelta(days=1)

    client.bulk_stop()


def consulta(param):
    criaregistro()

    if param.count("-") > 0:
        resultado_pesquisa = client.keys(f"sorteio:*:{param}")
    else:
        resultado_pesquisa = client.keys(f"sorteio:{param}:*")

    if not resultado_pesquisa:
        print("Data ou número não encontrado, tente novamente.")
        exit()

    numero_sorteio = (client.hget(resultado_pesquisa[0], "numero_sorteio"))
    data = (client.hget(resultado_pesquisa[0], "data"))
    numeros = (client.hget(resultado_pesquisa[0], "numeros"))
    ganhadores = (client.hget(resultado_pesquisa[0], "ganhadores"))
    print(f"numero_sorteio: {numero_sorteio}\n"
          f"data: {data}\n"
          f"numeros: {numeros}\n"
          f"ganhadores: {ganhadores}")


def main():
    param = input("Digite a data (no formato aaaa-mm-dd) ou o número do sorteio a ser procurado: ")
    consulta(param)


print("MEGA-SENA")
main()