# -*- coding: utf-8 -*-
"""¿Dónde se cae un mes que no genera? Semana, y si fue el plan o el sábado."""
import random
import generar2 as g
import semana as S
from sabado import armar_sabado

for semilla in (1, 2, 15, 27, 29):
    sabados, previos = [], []
    for n in range(1, 5):
        sem, falla_plan, falla_sabado = None, 0, 0
        for intento in range(30):
            base = semilla * 10 + n + intento * 977
            # Se repite acá lo que hace generar_semana, pero mirando cuál de
            # los dos pasos devolvió None. Sin separarlos, "sin combinación"
            # no dice nada: el plan de días y el sábado fallan por motivos
            # distintos y se arreglan distinto.
            if g.proponer(semilla=base, previas=previos) is None:
                falla_plan += 1
                continue
            sem = S.generar_semana(2, n, semilla=base,
                                   sabados_del_mes=sabados, dias_previos=previos)
            if sem:
                break
            falla_sabado += 1
        if not sem:
            print(f'semilla {semilla:>2} · se cae en la semana {n} · '
                  f'{falla_plan} veces sin plan de días, '
                  f'{falla_sabado} veces sin sábado')
            break
        sabados.append(sem['usados_sabado'])
        previos += [{'dia': d['dia'], 'cat': d['cat'], 'movs': d['movs']}
                    for d in sem['dias']]
        previos.append({'dia': 'Sábado', 'cat': 'PARTNER',
                        'movs': list(sem['usados_sabado'])})
