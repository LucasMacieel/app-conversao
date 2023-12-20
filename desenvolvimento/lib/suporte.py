import math

from lib.definicoes import AWG, PotenciaCorrente, Lamina


def encontrar_produto_mais_proximo(secao_geometrica, lamina):
    a_aproximado = arredondar_para_meio(secao_geometrica**0.5)
    aproximacoes_quadrado = []
    dimensoes = {(-1, -1): "Inválido"}

    if a_aproximado > 5:
        a_aproximado = 5

    for i in range(0, 7):
        a = a_aproximado - 1.5 + (i * 0.5)
        b = arredondar_para_meio(secao_geometrica / a)

        diferenca_produto = secao_geometrica - (a * b)
        diferenca_quadrado = abs(a - b)

        diferencas = (diferenca_produto, diferenca_quadrado)
        medidas = definir_dimensoes(a, b, lamina)

        aproximacoes_quadrado.append(diferencas)
        dimensoes[diferencas] = medidas

    aproximacoes_quadrado = dimensoes_elegiveis(aproximacoes_quadrado)
    melhor_dimensao = selecionar_dimensao(aproximacoes_quadrado, dimensoes)

    return dimensoes[melhor_dimensao]


def definir_dimensoes(dimensao_a, dimensao_b, lamina):
    if lamina == Lamina.PADRONIZADA:
        if dimensao_a < 1.5 or dimensao_a > 5 or dimensao_a == 4.5:
            if dimensao_b < 1.5 or dimensao_b > 5 or dimensao_b == 4.5:
                return "Inválido"
            else:
                return dimensao_b, dimensao_a
        else:
            return dimensao_a, dimensao_b
    elif lamina == Lamina.COMPRIDA:
        if dimensao_a < 4 or dimensao_a > 5 or dimensao_a == 4.5:
            if dimensao_b < 4 or dimensao_b > 5 or dimensao_b == 4.5:
                return "Inválido"
            else:
                return dimensao_b, dimensao_a
        else:
            return dimensao_a, dimensao_b
    elif lamina == Lamina.INVALIDO:
        return "Inválido"


def dimensoes_elegiveis(lista_diferencas):
    dimensoes_ordenadas = sorted(lista_diferencas)
    dimensoes_filtradas = filter(lambda x: (x[1] <= 1.5), dimensoes_ordenadas)

    return list(dimensoes_filtradas)


def selecionar_dimensao(lista_diferencas, dimensoes):
    for diff_prod, diff_a_b in lista_diferencas:
        if diff_a_b <= 1.5 and dimensoes[(diff_prod, diff_a_b)] != "Inválido":
            return diff_prod, diff_a_b

    return -1, -1


def calcular_espiras(tensao, inducao_magnetica_max, secao_magnetica, frequencia):
    return math.ceil((tensao * 1E8) / (4.44 * inducao_magnetica_max * secao_magnetica * frequencia))


def calcular_secao_cobre(espiras_primario, espiras_secundario, secao_condutor_primario, secao_condutor_secundario):
    secao_cobre_primario = espiras_primario*secao_condutor_primario
    secao_cobre_secundario = espiras_secundario*secao_condutor_secundario

    return secao_cobre_primario + secao_cobre_secundario


def encontrar_valor_awg(bitola_cabo_primario):
    for awg in AWG:
        if awg.value >= bitola_cabo_primario:
            return awg.name, awg.value

    return "Inválido", "Inválido"


def encontrar_densidade_corrente(potencia_secundaria):
    for potencia, corrente in PotenciaCorrente.items():
        if potencia >= potencia_secundaria:
            return corrente

    return "Inválido"


def calcular_densidade_corrente_media(corrente_primaria, corrente_secundaria, secao_condutor_primario,
                                      secao_condutor_secundario):
    densidade_corrente_primaria = corrente_primaria/secao_condutor_primario
    densidade_corrente_secundaria = corrente_secundaria/secao_condutor_secundario

    return (densidade_corrente_primaria + densidade_corrente_secundaria)/2


def verificar_valores(*valores):
    for valor in valores:
        if valor == "Inválido":
            return False
    return True


def arredondar_para_meio(sm):
    return round(sm * 2) / 2
