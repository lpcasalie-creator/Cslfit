# -*- coding: utf-8 -*-
"""Escalas: la línea (Esc) que acompaña a los movimientos de alta destreza.

DE DÓNDE SALEN

Dos fuentes, y las dos coinciden en la lógica:

  · Las que Luis ya escribe en su planilla, medidas de septiembre. Su razón es
    2x cuando el sustituto es claramente más fácil y 1,5x cuando es cercano.
  · El documento de escalado de Mayhem Athlete, que usa la misma convención.
    De sus dieciséis tablas se descartaron seis —Rope Climb, Legless, Pegboard,
    Sled y Sandbag— porque ese equipamiento no existe en el box (regla 11).

Los principios del documento, que son los que mandan cuando hay que elegir:
preservar el estímulo, mantener el dominio de tiempo y mantener el patrón de
movimiento. Bajar reps o bajar carga, no cambiar el ejercicio por otro que
entrene otra cosa.
"""

# movimiento Rx -> [(sustituto, razón, origen)]  en orden de preferencia
ESCALAS = {
 # --- Las que él ya usa (septiembre) ---------------------------------
 'HSPU':                 [('Pike Push-Up', 2.0, 'suya')],
 'Ring Dip':             [('Box Dip', 1.5, 'suya')],
 'Bar Muscle-up':        [('C2B', 2.0, 'suya'), ('Pull-Up', 3.0, 'Mayhem')],
 'Pistol':               [('Air Squat', 2.0, 'suya')],
 'Pull-up':              [('Ring Row', 2.0, 'suya'), ('Jumping Pull-Up', 1.5, 'Mayhem'),
                          ('Banded Pull-Up', 1.5, 'Mayhem')],
 'Chest-to-Bar Pull-up': [('Pull-Up', 1.0, 'suya')],

 # --- De Mayhem, con el equipamiento que sí tiene --------------------
 'Toes-to-Bar':          [('V-Up', 1.4, 'Mayhem'), ('Sit-Up', 2.0, 'Mayhem')],
 'Ring Muscle-up':       [('Bar Muscle-Up', 1.0, 'Mayhem'), ('Pull-Up', 2.0, 'Mayhem')],
 'Wall Walk':            [('Bear Crawl', 1.0, 'Mayhem')],
 'Handstand Walk':       [('Wall Walk', 0.06, 'Mayhem')],
 'Double under':         [('Single Under', 2.0, 'Mayhem')],
 'Squat Snatch':         [('Power Snatch', 1.0, 'Mayhem')],
}

# Tabla de conversión cardio de Mayhem. Permite rotar la modalidad sin perder
# el estímulo: 400m de carrera son 500m de remo o 1000m de bici.
CARDIO = [
 # (Run, Row, Bike, Ski)   en metros, versión hombres
 (100,   125,   250,   125),
 (200,   250,   500,   250),
 (400,   500,  1000,   500),
 (600,   750,  1500,   750),
 (800,  1000,  2000,  1000),
 (1000, 1250,  2500,  1250),
 (1600, 2000,  4000,  2000),
 (2000, 2500,  5000,  2500),
]
_COL = {'Run': 0, 'Row': 1, 'Bike': 2, 'Ski': 3}

def convertir(desde, hacia, metros):
    """400m de Run -> 500m de Row. Devuelve None si no hay equivalencia."""
    if desde not in _COL or hacia not in _COL: return None
    i, j = _COL[desde], _COL[hacia]
    mejor = min(CARDIO, key=lambda f: abs(f[i] - metros))
    if abs(mejor[i] - metros) > metros * 0.3: return None
    return mejor[j]

def escala_de(mov, reps):
    """La línea de escala para un movimiento, o None si no lleva."""
    opciones = ESCALAS.get(mov)
    if not opciones: return None
    sust, razon, _ = opciones[0]
    # Sin redondear: él escribe "12 HSPU / 24 Pike Push-Up", no 25.
    return f'{int(round(reps * razon))} {sust}'
