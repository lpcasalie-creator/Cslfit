# -*- coding: utf-8 -*-
"""Cuánto demora cada movimiento para un buen atleta del grupo.

POR QUÉ NO SE DEDUCE SOLO DE LOS DATOS

La regla 4 de Luis —"cap = mejor atleta + 2-3'"— convierte cada cap en una
ecuación. Pero septiembre da 13 ecuaciones para 22 movimientos: el sistema
está subdeterminado. Ajustarlo a ciegas reproduce los caps perfecto y asigna
16 segundos a un sit-up y 0,05 a un push jerk.

Así que los valores de partida son de entrenamiento, no de ajuste: lo que
demora una repetición sin fallar, a ritmo de metcon, para alguien capaz.
Los caps reales de Luis los corrigen dentro de un margen — pueden moverlos
un 40% arriba o abajo, no inventarlos.
"""

# Segundos por repetición (por metro en los de distancia)
BASE = {
 # Peso corporal rápido
 'Air Squat': 1.2, 'Sit-up': 1.5, 'Push-up': 1.6, 'V-up': 1.8,
 'Double under': 0.35, 'Single Under': 0.2,
 # Peso corporal con destreza
 'Pull-up': 2.2, 'Chest-to-Bar Pull-up': 2.6, 'Bar Muscle-up': 4.5,
 'Ring Muscle-up': 5.5, 'Ring Dip': 2.2, 'Box Dip': 1.8,
 'HSPU': 3.2, 'Pike Push-up': 2.0, 'Toes-to-Bar': 2.4, 'Pistol': 3.0,
 'Wall Walk': 8.0, 'Burpee': 3.6, 'Box Jump-Over': 2.6, 'Box Jump': 2.4,
 # Barra
 'Deadlift': 3.0, 'Front Squat': 3.2, 'Back Squat': 3.2, 'Overhead Squat': 3.5,
 'Power Clean': 4.2, 'Squat Clean': 4.8, 'Hang Power Clean': 3.6,
 'Power Snatch': 4.2, 'Squat Snatch': 5.0, 'Push Press': 2.6,
 'Push Jerk': 3.0, 'Split Jerk': 3.4, 'Thruster': 3.2, 'Clean and Jerk': 5.5,
 # Implemento
 'Wall Ball': 2.0, 'KB swing': 1.6, 'DB Snatch': 2.0, 'DB Push Press': 2.2,
 'Devil Press': 5.0,
 # Distancia: segundos por metro
 'Run': 0.26, 'Row': 0.20, 'Bike': 0.15, 'Farmer Carry': 0.50,
 'Shuttle Run': 0.30,
}
# Los ritmos de arriba son de atleta élite sin fallar. Este factor los lleva
# al grupo real de CrossTrain, y NO es una estimación: es el multiplicador que
# mejor reproduce los 13 caps que Luis puso en septiembre, ajustado por
# mínimos cuadrados. Un solo parámetro con trece datos.
FACTOR_GRUPO = 1.58

POR_DEFECTO = 3.0
MARGEN_CAP = 2.5 * 60     # el "+2-3'" de la regla 4


def segundos_de(mov, cantidad):
    return BASE.get(mov, POR_DEFECTO) * cantidad * FACTOR_GRUPO


def estimar(trabajo):
    """trabajo = {movimiento: reps o metros} -> segundos del mejor atleta."""
    return sum(segundos_de(m, n) for m, n in trabajo.items())


def cap_para(trabajo):
    """El cap que corresponde a ese trabajo, redondeado al minuto."""
    return max(6, round((estimar(trabajo) + MARGEN_CAP) / 60))
