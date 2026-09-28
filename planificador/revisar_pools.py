# -*- coding: utf-8 -*-
"""Cruza los pools de la app contra el catálogo y lista lo que no cuadra.

ESTO REEMPLAZA LA IDEA DE GENERAR LOS POOLS, que no se puede hacer. El catálogo
ofrece entre 7 y 20 candidatos por pool y la app elige seis: esa elección es
curaduría de Luis y no está en ninguna columna. Un generador tendría que
inventarla.

Lo que sí se puede es al revés, y sirve igual: cada movimiento que está en un
pool tiene que cumplir con lo que el catálogo dice de él. Si `fuerza/
push_vertical/completo` trae un movimiento cuyo `Patrón` no es 'push', o cuya
cadena no es 'empuje vertical', o cuyo equipo dice 'Limitado', es un error de
dedo en index.html — y este script lo encuentra sin tocar la app.

Tres reglas, y por qué cada una es así:

  · PATRÓN. La clave del pool manda: push_vertical y push_horizontal tienen que
    ser los dos 'push'; olympic_main y olympic_acc, los dos 'olympic'. Es la
    única distinción que el catálogo NO puede hacer, así que acá no se exige.

  · CADENA. Vale la principal O la secundaria. Los tres High Pull son el motivo:
    Luis los definió como "las dos cosas" —bisagra de principal, tracción
    vertical de secundaria— así que exigir solo la principal los marcaría mal.

  · EQUIPO. Un pool 'limitado' no puede traer un movimiento que el catálogo
    marque 'Completo', y al revés. 'Cualquiera' sirve para los dos.

Los movimientos que no están en el catálogo se listan aparte: seis de ellos son
prescripciones disfrazadas de movimiento ('Row 250m', 'Ski Erg 300m') y cinco
son la misma cosa escrita distinta ('Wall Balls' contra 'Wall Ball'). Eso es
para arreglar, pero es otro trabajo y no un error de clasificación.

    python3 revisar_pools.py          ->  el informe
    python3 revisar_pools.py --duro   ->  además sale con código 1 si hay algo
"""
import sys
from collections import defaultdict

import openpyxl

from pools import leer_pools, por_movimiento

CATALOGO = 'CSL-Fit_Catalogo_Completo.xlsx'

# Patrón que el catálogo tiene que decir, por clave de pool. None = la clave no
# se puede verificar contra el catálogo (no hay columna que lo distinga).
PATRON_DE = {
    'squat': 'squat', 'hinge': 'hinge', 'lunge': 'lunge',
    'push_vertical': 'push', 'push_horizontal': 'push',
    'pull_vertical': 'pull', 'pull_horizontal': 'pull',
    'olympic_main': 'olympic', 'olympic_acc': 'olympic',
    # gimnasia, cardio y musculacion usan claves que no son patrones del
    # catálogo ('core', 'dip', 'skill', 'interval', 'accessory', 'legs'):
    # ahí el patrón no se verifica y la cadena tampoco.
}

CADENA_DE = {
    'squat': 'rodilla', 'hinge': 'bisagra', 'lunge': 'rodilla',
    'push_vertical': 'empuje vertical', 'push_horizontal': 'empuje horizontal',
    'pull_vertical': 'traccion vertical',
    'pull_horizontal': 'traccion horizontal',
}

EQUIPO_DE = {'limitado': 'Limitado', 'completo': 'Completo'}

# Movimientos que pertenecen de verdad a DOS familias. El catálogo guarda un
# solo `Patrón`, así que sin esta tabla el checker los denunciaría para siempre
# y el informe se llenaría de ruido que nadie va a arreglar — que es como muere
# un checker. Cada uno va con su razón, para que sea una decisión anotada y no
# una excepción escondida:
#
#   · Los tres jerks: el catálogo dice 'olympic' y es cierto, son levantamientos
#     olímpicos. La app los usa en push_vertical y también es cierto: la barra
#     termina sobre la cabeza. Sus dos cadenas ya dicen 'empuje vertical', así
#     que la regla de cadena los aprueba sola; el desacuerdo era solo de patrón.
#   · Overhead Squat: el catálogo dice 'squat' porque es una sentadilla. La app
#     lo usa como accesorio de arranque, que es para lo que sirve.
#
# Es el mismo caso de los tres High Pull, que Luis resolvió con "las dos cosas".
DOS_FAMILIAS = {
    ('Push Jerk', 'push_vertical'):      'olympic',
    ('Power Jerk', 'push_vertical'):     'olympic',
    ('Split Jerk', 'push_vertical'):     'olympic',
    ('Overhead Squat', 'olympic_acc'):   'squat',
    # DB Bulgarian Split Squat está en los DOS pools de la app, lunge y squat.
    # Es una sentadilla a una pierna con el patrón de zancada, así que las dos
    # son ciertas. El catálogo lo dice 'lunge' y en squat el checker lo acepta.
    ('DB Bulgarian Split Squat', 'squat'): 'lunge',
}


def leer_catalogo(ruta=CATALOGO):
    wb = openpyxl.load_workbook(ruta, data_only=True)
    filas = {}
    for r in wb['Movimientos'].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        filas[str(r[0]).strip()] = {
            'patron': r[2], 'cad1': r[3], 'cad2': r[4],
            'categoria': r[5], 'equipo': r[6]}
    return filas


def revisar(pools=None, catalogo=None):
    pools = pools or leer_pools()
    cat = catalogo or leer_catalogo()
    hallazgos, ausentes = [], defaultdict(list)

    for foco, claves in pools.items():
        for clave, niveles in claves.items():
            for equipo, movs in niveles.items():
                for m in movs:
                    if m not in cat:
                        ausentes[m].append(f'{foco}/{clave}/{equipo}')
                        continue
                    r = cat[m]
                    donde = f'{foco}/{clave}/{equipo}'
                    esperado = PATRON_DE.get(clave)
                    permitido = DOS_FAMILIAS.get((m, clave))
                    if esperado and r['patron'] not in (esperado, permitido):
                        hallazgos.append(
                            ('Patrón', m, donde,
                             f"el catálogo dice {r['patron']!r}, "
                             f'la clave pide {esperado!r}'))
                    cadena = CADENA_DE.get(clave)
                    if cadena and cadena not in (r['cad1'], r['cad2']):
                        hallazgos.append(
                            ('Cadena', m, donde,
                             f"el catálogo dice {r['cad1']!r} / {r['cad2']!r}, "
                             f'la clave pide {cadena!r}'))
                    exige = EQUIPO_DE[equipo]
                    if str(r['equipo']) not in (exige, 'Cualquiera'):
                        hallazgos.append(
                            ('Equipo', m, donde,
                             f"el catálogo dice {r['equipo']!r}, "
                             f'el pool es {equipo!r}'))
    return hallazgos, dict(ausentes)


if __name__ == '__main__':
    hallazgos, ausentes = revisar()

    print(f'{len(hallazgos)} desacuerdos entre los pools y el catálogo')
    por_regla = defaultdict(list)
    for regla, m, donde, detalle in hallazgos:
        por_regla[regla].append((m, donde, detalle))
    for regla in ('Patrón', 'Cadena', 'Equipo'):
        if regla not in por_regla:
            continue
        print(f'\n{regla} — {len(por_regla[regla])}')
        for m, donde, detalle in sorted(por_regla[regla]):
            print(f'  {m:38} {donde:34} {detalle}')

    print(f'\n{len(ausentes)} movimientos del pool que no están en el catálogo')
    for m, donde in sorted(ausentes.items()):
        print(f'  {m:38} {", ".join(donde)}')

    if '--duro' in sys.argv and (hallazgos or ausentes):
        sys.exit(1)
