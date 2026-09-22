# -*- coding: utf-8 -*-
"""¿Qué separación mínima usa Luis, de verdad, en sus tres meses?

Antes de ponerle una regla al generador hay que saber si la regla sale de él o
me la estoy inventando mirando CrossFit.com. Son gimnasios distintos: él tiene
clases con horario y 5 días, ellos open gym y 7. Copiarles el número sería
programar para otra gente.

Se mide el hueco MÍNIMO observado por movimiento, dentro de cada mes.
"""
from collections import defaultdict
import mes2, mes3, septiembre
from leer_wod import leer
from familias import familia_de

try:
    from generar2 import CATEG, peso_tipico
except Exception:                         # si el catálogo no carga
    CATEG, peso_tipico = {}, lambda m: 0


def dias_de(MES):
    out = []
    for sem in MES:
        for d in sem[3]:
            out.append(leer(d[4])['movimientos'])
        out.append(leer(sem[4].split('Score:')[0])['movimientos'])
    return out


MESES = [('Mes 2', dias_de(mes2.MES)), ('Mes 3', dias_de(mes3.MES)),
         ('Sept', dias_de(septiembre.MES))]

huecos = defaultdict(list)
veces = defaultdict(int)
for _, dias in MESES:
    pos = defaultdict(list)
    for i, dia in enumerate(dias):
        for m in set(dia):
            pos[m].append(i)
            veces[m] += 1
    for m, v in pos.items():
        huecos[m] += [b - a for a, b in zip(v, v[1:])]

# Un movimiento que salió una sola vez en un mes no tiene hueco que medir, y
# con la lista vacía el mínimo no existe. No es un caso raro: son la mayoría.
huecos = {m: g for m, g in huecos.items() if g}

# Los tres grupos que importan. El relleno puede volver al día siguiente sin que
# nadie lo note; un Bar Muscle-up no.
RELLENO = {'Run', 'Row', 'Bike', 'Ski', 'Machine', 'Shuttle Run',
           'Double under', 'Single Under', 'Air Squat', 'Sit-up', 'Burpee'}


def grupo(m):
    if m in RELLENO:
        return 'relleno'
    if peso_tipico(m) >= 115:
        return 'barra pesada'
    if CATEG.get(m) == 'Gimnasia' and veces[m] <= 4:
        return 'gimnasia dura'
    return 'resto'


def main():
    print(f"{'movimiento':<26}{'grupo':<15}{'veces':>6}{'huecos'}")
    filas = sorted(huecos.items(), key=lambda kv: (grupo(kv[0]), min(kv[1])))
    por_grupo = defaultdict(list)
    for m, g in filas:
        por_grupo[grupo(m)] += g
        print(f'{m:<26}{grupo(m):<15}{veces[m]:>6}  {sorted(g)}')

    print()
    print(f"{'grupo':<16}{'hueco mínimo':>14}{'mediana':>10}{'≤2 días':>10}{'n':>5}")
    for g in ('barra pesada', 'gimnasia dura', 'resto', 'relleno'):
        v = sorted(por_grupo[g])
        if not v:
            continue
        print(f'{g:<16}{v[0]:>14}{v[len(v)//2]:>10}'
              f'{sum(1 for x in v if x <= 2)/len(v):>9.0%}{len(v):>5}')

    print()
    print('— Los que NUNCA vuelven en menos de N días en sus tres meses —')
    for m, g in sorted(huecos.items(), key=lambda kv: -min(kv[1]))[:12]:
        print(f'  {m:<26} mínimo {min(g)} · sale {veces[m]} veces')


if __name__ == '__main__':
    main()
