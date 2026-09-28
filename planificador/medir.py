# -*- coding: utf-8 -*-
"""Medición limpia del generador, con y sin la regla de separación.

DOS TRAMPAS que me comí y que dejan el número mal:

 1. Leer el texto del sábado entero mete la línea "Evita:", que nombra
    justamente lo que el sábado NO usa. `generar2._cuenta_mes` corta en
    'Score:' por eso; mis primeras mediciones no cortaban y contaban esos
    movimientos como si estuvieran en el WOD. Todas las violaciones de barra
    que creí encontrar eran de esa línea.

 2. Releer el texto en vez de mirar el plan. El plan (`d['movs']`,
    `usados_sabado`) es lo que el generador decidió; el texto es una
    reescritura que puede nombrar cosas de más. Para auditar una regla del
    generador hay que mirar lo que el generador decidió.

Acá se mide el plan.
"""
import sys
from collections import Counter, defaultdict
import generar2 as g
import semana as S

MESES = int(sys.argv[1]) if len(sys.argv) > 1 else 20


def dias_del_mes(m):
    """Los 24 días en orden cronológico, como listas de movimientos."""
    out = []
    for sem in m:
        for d in sem['dias']:
            out.append(list(d['movs']))
        out.append(list(sem['usados_sabado']))
    return out


def correr(con_regla):
    # La regla se apaga poniendo las separaciones en cero, que es el mismo
    # camino que usa el código: `separacion_de` devuelve 0 y `muy_pronto`
    # corta al toque.
    guardado = (g.SEPARACION_BARRA, g.SEPARACION_DESTREZA, dict(g.SEPARACION_EXTRA))
    if not con_regla:
        g.SEPARACION_BARRA = g.SEPARACION_DESTREZA = 0
        g.SEPARACION_EXTRA = {}
    try:
        meses, fallan = [], []
        for s in range(1, MESES + 1):
            m = S.generar_mes(2, semilla=s)
            if m:
                meses.append(dias_del_mes(m))
            else:
                fallan.append(s)
        return meses, fallan
    finally:
        g.SEPARACION_BARRA, g.SEPARACION_DESTREZA, g.SEPARACION_EXTRA = guardado


def grupo(mv):
    if g.CATEG.get(mv) == 'Fuerza':
        return 'barra'
    if mv in g.ALTA_DESTREZA:
        return 'alta destreza'
    if mv in g.MONOSTRUCTURAL or mv in ('Air Squat', 'Sit-up', 'Burpee'):
        return 'relleno'
    return 'resto'


def informe(nombre, meses, fallan):
    huecos = defaultdict(list)
    dias_tot = 0
    for dias in meses:
        dias_tot += len(dias)
        pos = defaultdict(list)
        for i, dia in enumerate(dias):
            for mv in set(dia):
                pos[mv].append(i)
        for mv, v in pos.items():
            huecos[grupo(mv)] += [b - a for a, b in zip(v, v[1:])]
    todos = [x for v in huecos.values() for x in v]
    print(f'\n### {nombre} · {len(meses)} meses · {dias_tot} días · '
          f'sin combinación {len(fallan)}/{MESES} {fallan}')
    print(f"{'grupo':<16}{'mínimo':>8}{'mediana':>9}{'≤3 días':>9}{'n':>6}")
    for gr in ('barra', 'alta destreza', 'resto', 'relleno'):
        v = sorted(huecos[gr])
        if not v:
            print(f'{gr:<16}{"—":>8}')
            continue
        print(f'{gr:<16}{v[0]:>8}{v[len(v)//2]:>9}'
              f'{sum(1 for x in v if x <= 3)/len(v):>8.0%}{len(v):>6}')
    t = sorted(todos)
    print(f"{'TODO':<16}{t[0]:>8}{t[len(t)//2]:>9}"
          f'{sum(1 for x in t if x <= 3)/len(t):>8.0%}{len(t):>6}')
    return huecos


sin_r, f_sin = correr(False)
con_r, f_con = correr(True)
informe('SIN la regla', sin_r, f_sin)
informe('CON la regla', con_r, f_con)

print('\n### Luis, sus tres meses, mismos grupos')
print(f"{'grupo':<16}{'mínimo':>8}{'mediana':>9}{'≤3 días':>9}{'n':>6}")
import separacion as sp
luis = defaultdict(list)
for mv, v in sp.huecos.items():
    luis[grupo(mv)] += v
for gr in ('barra', 'alta destreza', 'resto', 'relleno'):
    v = sorted(luis[gr])
    if not v:
        print(f'{gr:<16}{"—":>8}')
        continue
    print(f'{gr:<16}{v[0]:>8}{v[len(v)//2]:>9}'
          f'{sum(1 for x in v if x <= 3)/len(v):>8.0%}{len(v):>6}')
