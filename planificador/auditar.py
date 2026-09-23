# -*- coding: utf-8 -*-
"""Genera meses y los pasa por el mismo validador que corrió sobre septiembre.

El punto: que el generador se someta al control que encontró los problemas de
su mes escrito a mano. Si el generador no pasa sus propias reglas, no sirve.
"""
import sys
from collections import Counter
from semana import generar_mes
from validar import validar


def a_formato_mes(semanas, mes):
    """Del formato del generador al formato de septiembre.MES."""
    out = []
    for n, sem in enumerate(semanas, 1):
        jornadas = [(d['dia'], d['cat'], d['cap'], d['skill'], d['wod'])
                    for d in sem['dias']]
        out.append((n, f'semana {n}', f'mes {mes}', jornadas, sem['sabado']))
    return out


def auditar(mes, semillas, detalle=True):
    todos = Counter()
    fallos = 0
    for s in semillas:
        semanas = generar_mes(mes, semilla=s)
        if not semanas:
            fallos += 1
            continue
        h = validar(a_formato_mes(semanas, mes), imprimir=False)
        for nivel, regla, _ in h:
            if nivel == 'revisar':
                todos[regla] += 1
    return todos, fallos, len(semillas)


if __name__ == '__main__':
    mes = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12

    print('=' * 70)
    print(f'UN MES GENERADO (mes {mes}, semilla 11) POR EL VALIDADOR')
    print('=' * 70)
    semanas = generar_mes(mes, semilla=11)
    validar(a_formato_mes(semanas, mes), f'Mes {mes} generado · semilla 11')

    print()
    print('=' * 70)
    print(f'{n} MESES GENERADOS — qué regla se rompe y cuántas veces')
    print('=' * 70)
    todos, fallos, total = auditar(mes, range(1, n + 1))
    print(f'Meses sin combinación: {fallos}/{total}')
    if not todos:
        print('Ninguna regla rota en ningún mes.')
    for regla, veces in todos.most_common():
        print(f'  {veces:>3} × {regla}   ({veces/max(1,total-fallos):.1f} por mes)')
