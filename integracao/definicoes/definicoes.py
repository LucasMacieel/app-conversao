import math
from enum import Enum


class Transformador(Enum):
    INVALIDO = 0
    P1_S1 = 1
    P2_S1_OU_P1_S2 = 2
    P2_S2 = 3


class Lamina(Enum):
    INVALIDO = 0
    PADRONIZADA = 1
    COMPRIDA = 2


PotenciaCorrente = {
    500: 3,
    1000: 2.5,
    3000: 2,
}

LaminaInformacoes = {
    Lamina.INVALIDO: "Inválido",
    Lamina.PADRONIZADA: {
        1.5: (0, 168, 0.095),
        2: (1, 300, 0.170),
        2.5: (2, 468, 0.273),
        3: (3, 675, 0.380),
        3.5: (4, 900, 0.516),
        4: (5, 1200, 0.674),
        5: (6, 1880, 1.053),
    },
    Lamina.COMPRIDA: {
        4: (5, 2400, 1),
        5: (6, 3750, 1.580)
    }
}


class AWG(Enum):
    AWG_44 = 0.002
    AWG_43 = 0.0025
    AWG_42 = 0.0032
    AWG_41 = 0.0040
    AWG_40 = 0.0050
    AWG_39 = 0.0063
    AWG_38 = 0.0079
    AWG_37 = 0.0100
    AWG_36 = 0.0127
    AWG_35 = 0.0159
    AWG_34 = 0.0201
    AWG_33 = 0.0254
    AWG_32 = 0.032
    AWG_31 = 0.04
    AWG_30 = 0.051
    AWG_29 = 0.064
    AWG_28 = 0.08
    AWG_27 = 0.1
    AWG_26 = 0.13
    AWG_25 = 0.16
    AWG_24 = 0.2
    AWG_23 = 0.26
    AWG_22 = 0.33
    AWG_21 = 0.41
    AWG_20 = 0.52
    AWG_19 = 0.65
    AWG_18 = 0.82
    AWG_17 = 1.04
    AWG_16 = 1.31
    AWG_15 = 1.65
    AWG_14 = 2.08
    AWG_13 = 2.63
    AWG_12 = 3.31
    AWG_11 = 4.17
    AWG_10 = 5.26
    AWG_9 = 6.63
    AWG_8 = 8.36
    AWG_7 = 10.55
    AWG_6 = 13.3
    AWG_5 = 16.77
    AWG_4 = 21.15
    AWG_3 = 26.67
    AWG_2 = 33.63
    AWG_1 = 42.41
    AWG_0 = 53.48
    AWG_00 = 67.43
    AWG_000 = 85.3
    AWG_0000 = 107.2
    INVALIDO = math.inf


TRANSFORMADOR = {
    "1p1s": 0,
    "2p1s-1p2s": 1,
    "2p2s": 2
}

lamina = {
    "padronizada": 0,
    "comprida": 1
}
