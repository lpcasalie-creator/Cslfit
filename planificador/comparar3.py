# -*- coding: utf-8 -*-
"""Segunda tanda: cada cuánto vuelve un movimiento, y qué tan cargado está el
día más repetido. Lo primero es lo que el alumno siente como "otra vez esto".
"""
from collections import Counter, defaultdict
import crossfitcom, crossfitcom2, mes2, mes3, septiembre
from comparar2 import movs_luis, luis_todo

CF = crossfitcom.DIAS + crossfitcom2.DIAS
cf = [d[5] for d in CF]
lu = [d[2] for d in luis_todo]


def techos(secuencia, ventana):
    """Máximo de veces que un movimiento aparece dentro de `ventana` días."""
    peor = Counter()
    for i in range(len(secuencia)):
        c = Counter(m for dia in secuencia[i:i + ventana] for m in dia)
        for m, v in c.items():
            peor[m] = max(peor[m], v)
    return peor


def huecos(secuencia):
    """Días entre dos apariciones del mismo movimiento."""
    pos = defaultdict(list)
    for i, dia in enumerate(secuencia):
        for m in set(dia):
            pos[m].append(i)
    g = [b - a for v in pos.values() for a, b in zip(v, v[1:])]
    return g


for nombre, s in (('CrossFit.com (63 días)', cf), ('Luis (72 días)', lu)):
    g = sorted(huecos(s))
    t24 = techos(s, 24)
    print(f'{nombre}')
    print(f'  vuelve a salir, en promedio, a los {sum(g)/len(g):.1f} días '
          f'(mediana {g[len(g)//2]})')
    print(f'  vuelve en 3 días o menos: {sum(1 for x in g if x <= 3)/len(g):.0%} de las veces')
    print(f'  techo dentro de 24 días: el peor es {t24.most_common(1)[0][0]} '
          f'con {t24.most_common(1)[0][1]} · '
          f'{sum(1 for v in t24.values() if v >= 4)} movimientos llegan a 4+')
    dias_con = Counter()
    for dia in s:
        for m in set(dia):
            dias_con[m] += 1
    print('  sale en más días: ' + ', '.join(
        f'{m} {v/len(s):.0%}' for m, v in dias_con.most_common(5)))
    print()

print('— Cuántos movimientos cubren la mitad del volumen —')
for nombre, s in (('CrossFit.com', cf), ('Luis', lu)):
    c = Counter(m for dia in s for m in dia)
    total = sum(c.values())
    acc, n = 0, 0
    for _, v in c.most_common():
        acc += v; n += 1
        if acc >= total / 2:
            break
    print(f'  {nombre}: {n} de {len(c)} ({n/len(c):.0%} del vocabulario)')
