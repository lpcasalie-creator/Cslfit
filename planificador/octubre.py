# -*- coding: utf-8 -*-
"""Octubre 2026 — Mes 1 del ciclo nuevo, semanas 17-20.

Su septiembre (Mes 4, semanas 13-16) cierra el domingo 27. El ciclo vuelve a
empezar el lunes 29 con el mes Base, que es EL ÚNICO del que no hay planilla.
Todo lo de porcentajes y series acá es extrapolado, y va marcado.
"""
import sys
from datetime import date, timedelta
from semana import generar_mes, PUNTO, LEYENDA
from bloque import (FASES, PCT_POR_MES, TEST_DEL_MES, ROTULO_S4,
                    MESES_SIN_DATO, AVISO_SIN_DATO)

MES = 1
PRIMER_LUNES = date(2026, 9, 29)
ANCHO = 68

MESES_ES = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
            'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


def rango(n):
    """El rango de fechas de la semana n (1-4), como lo escribe él."""
    lunes = PRIMER_LUNES + timedelta(weeks=n - 1)
    sabado = lunes + timedelta(days=5)
    if lunes.month == sabado.month:
        return f'{lunes.day}–{sabado.day} {MESES_ES[lunes.month]}'
    return f'{lunes.day} {MESES_ES[lunes.month]} – {sabado.day} {MESES_ES[sabado.month]}'


def imprimir(semanas):
    fase, banda = FASES[MES]
    test = TEST_DEL_MES.get(MES, 'ninguno')
    print('=' * ANCHO)
    print(f'CROSSTRAIN EIM — Mes {MES} · {fase} {banda}')
    print(f'Semanas 17–20 · {rango(1).split("–")[0].strip()} a '
          f'{(PRIMER_LUNES + timedelta(weeks=3, days=5)).day} de octubre')
    print('2 STRENGTH · 1 GYMNASTICS · 1 METCON · 1 ACCESSORY por semana')
    if MES in MESES_SIN_DATO:
        print()
        print('  ⚠ MES SIN PLANILLA DE REFERENCIA')
        for linea in AVISO_SIN_DATO.split('\n'):
            print('    ' + linea.strip())
    print('=' * ANCHO)

    for n, sem in enumerate(semanas, 1):
        escalera = PCT_POR_MES.get(MES, PCT_POR_MES[3])
        pct = (ROTULO_S4[test] if n == 4 and test != 'ninguno' else escalera[n])
        print()
        print(f'SEMANA {16 + n}  |  {rango(n)}  |  {pct}')
        print('─' * ANCHO)
        for d in sem['dias']:
            aviso = ('   ▲ se pidió ' + d['dom_pedido']
                     if d.get('dom_pedido') and d['dom_pedido'] != d['dom'] else '')
            print()
            print(f"  {d['dia'].upper():<11} {d['cat']:<11} {PUNTO[d['dom']]} "
                  f"{d['cap']}'   Skill {d['skill']}'{aviso}")
            for l in d['bloque'].split('\n'):
                print(f'      {l}')
            print()
            for l in d['wod'].split('\n'):
                print(f'      {l}')
        print()
        print(f"  {'SÁBADO':<11} PARTNER     35'")
        for l in sem['sabado'].split('\n'):
            print(f'      {l}')
        print()

    print('─' * ANCHO)
    for l in LEYENDA:
        print(l)


if __name__ == '__main__':
    semilla = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    semanas = generar_mes(MES, semilla=semilla)
    if not semanas:
        print('sin combinación — probar otra semilla')
        sys.exit(1)
    imprimir(semanas)
