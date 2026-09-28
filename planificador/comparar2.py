# -*- coding: utf-8 -*-
"""Los dos meses de CrossFit.com contra los tres de Luis.

Con un solo mes no se sabe qué era patrón y qué era la casualidad de ese mes.
Con dos, cada número se puede repetir o no repetir — y lo que no se repite no
es una conclusión, es ruido.
"""
from collections import Counter
import crossfitcom, crossfitcom2, mes2, mes3, septiembre
from leer_wod import leer

M1 = crossfitcom.DIAS
M2 = crossfitcom2.DIAS
AMBOS = M1 + M2


def movs_luis(MES):
    """[(etiqueta_dia, cat, [movs]), ...] — solo el WOD, sin el bloque."""
    out = []
    for sem in MES:
        dias = sem[3]
        for d in dias:
            out.append((d[0], d[1], leer(d[4])['movimientos']))
        if len(sem) > 4 and sem[4]:
            out.append(('Sábado', 'PARTNER', leer(sem[4])['movimientos']))
    return out


def perfil(nombre, dias, movs_de):
    ms = [movs_de(d) for d in dias]
    c = Counter(m for lista in ms for m in lista)
    total = sum(c.values())
    distintos = len(c)
    una_vez = sum(1 for v in c.values() if v == 1)
    top10 = sum(v for _, v in c.most_common(10))
    return {
        'nombre': nombre, 'dias': len(dias), 'distintos': distintos,
        'por_dia': total / len(dias),
        'una_vez': una_vez / distintos,
        'top10': top10 / total,
        'contador': c,
    }


def fila(p):
    return (f"{p['nombre']:<20}{p['dias']:>5}{p['distintos']:>10}"
            f"{p['por_dia']:>10.1f}{p['una_vez']:>11.0%}{p['top10']:>12.0%}")


CFM = lambda d: d[5]
LUIS = lambda d: d[2]

luis = {n: movs_luis(m.MES) for n, m in
        (('Luis Mes 2', mes2), ('Luis Mes 3', mes3), ('Luis Sept', septiembre))}
luis_todo = sum(luis.values(), [])

perfiles = [
    perfil('CF.com Mes 1', M1, CFM),
    perfil('CF.com Mes 2', M2, CFM),
    perfil('CF.com ambos', AMBOS, CFM),
    perfil('Luis Mes 2', luis['Luis Mes 2'], LUIS),
    perfil('Luis Mes 3', luis['Luis Mes 3'], LUIS),
    perfil('Luis Sept', luis['Luis Sept'], LUIS),
    perfil('Luis los tres', luis_todo, LUIS),
]

print(f"{'':<20}{'días':>5}{'distintos':>10}{'x día':>10}{'sale 1 vez':>11}{'top10 vol':>12}")
for p in perfiles:
    print(fila(p))

print()
print('— ¿Se repite el vocabulario entre los dos meses de CrossFit.com? —')
c1 = perfiles[0]['contador']
c2 = perfiles[1]['contador']
comun = set(c1) & set(c2)
print(f'mes 1: {len(c1)} movimientos · mes 2: {len(c2)} · en los dos: {len(comun)}')
print(f'el mes 2 estrenó {len(set(c2) - set(c1))} que el mes 1 no tenía')
cA = perfiles[2]['contador']
print(f'unión de los dos meses: {len(cA)} movimientos distintos en 63 días')

print()
print('— Formatos —')
for nombre, dias in (('CF.com Mes 1', M1), ('CF.com Mes 2', M2), ('CF.com ambos', AMBOS)):
    f = Counter(d[3] for d in dias)
    print(f'{nombre:<16}{len(f):>3} formatos en {len(dias)} días · '
          + ', '.join(f'{k} {v}' for k, v in f.most_common(4)))

print()
print('— Dominios —')
for nombre, dias in (('CF.com Mes 1', M1), ('CF.com Mes 2', M2), ('CF.com ambos', AMBOS)):
    d = Counter(x[4] for x in dias)
    n = len(dias)
    print(f'{nombre:<16}' + '  '.join(f'{k} {v/n:.0%}' for k, v in d.most_common()))

print()
print('— Etiquetas —')
for nombre, dias in (('CF.com Mes 1', M1), ('CF.com Mes 2', M2)):
    e = Counter(x[2] or '—' for x in dias)
    print(f'{nombre:<16}' + '  '.join(f'{k} {v}' for k, v in e.most_common()))

print()
print('— Día de la semana: ¿hay patrón fijo? —')
for dia in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']:
    m1 = [d for d in M1 if d[1] == dia]
    m2 = [d for d in M2 if d[1] == dia]
    dom1 = Counter(d[4] for d in m1).most_common(1)
    dom2 = Counter(d[4] for d in m2).most_common(1)
    et = sum(1 for d in M1 + M2 if d[1] == dia and d[2])
    print(f'{dia}  mes1 {dom1[0][0]} {dom1[0][1]}/{len(m1)} · '
          f'mes2 {dom2[0][0]} {dom2[0][1]}/{len(m2)} · con etiqueta {et}/{len(m1)+len(m2)}')

print()
print('— Los más repetidos —')
print('CF.com (63 días):', ', '.join(f'{m} {v}' for m, v in cA.most_common(8)))
cl = perfiles[6]['contador']
print('Luis (72 días):  ', ', '.join(f'{m} {v}' for m, v in cl.most_common(8)))
