# -*- coding: utf-8 -*-
"""Las reglas de CrossTrain EIM, corriendo sobre un mes.

Antes esto era un script pegado a septiembre.py. Ahora es una función: el
mismo juego de reglas que encontró lo tuyo a mano tiene que poder correr
sobre lo que produce el generador, o no sirve de nada como control.

    from validar import validar
    validar(MES_DE_SEPTIEMBRE, 'Septiembre 2026')      # el suyo, a mano
    validar(mes_generado, 'Mes 2 generado')            # el de la máquina

El mes entra con la forma de septiembre.MES:
    [(semana, fechas, fase, [(dia, cat, cap, skill, texto)...], texto_sabado)]
"""
import openpyxl, re
from collections import defaultdict, Counter
from leer_wod import leer

# --- Catálogo: base y cadenas -------------------------------------------
wb = openpyxl.load_workbook('CSL-Fit_Catalogo_Base.xlsx', data_only=True)
BASE, CAD1, CAD2, TECNICO = {}, {}, {}, set()
for r in wb['Movimientos'].iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    nombre, base, _pat, c1, c2 = r[0], r[1], r[2], r[3], r[4]
    BASE[nombre] = base or nombre
    CAD1[base or nombre] = c1 or ''
    CAD2[base or nombre] = c2 or ''
    if str(r[7] or '').strip().lower() in ('sí', 'si'): TECNICO.add(base or nombre)

def base_de(m): return BASE.get(m, m)
def cadenas(m):
    b = base_de(m)
    return [c for c in (CAD1.get(b, ''), CAD2.get(b, '')) if c]

DOMINIO = lambda cap: 'fosfágeno' if cap < 14 else ('glucolítico' if cap <= 19 else 'aeróbico')
# 30/50/20, escrito con todas sus letras en la leyenda del mes 2
# ("Distribución objetivo: 30% / 50% / 20%"). Yo usaba 25/50/25.
OBJETIVO = {'fosfágeno': .30, 'glucolítico': .50, 'aeróbico': .20}
SKILL_ESPERADO = lambda cap: (20, 22) if cap < 14 else ((17, 17) if cap <= 19 else (12, 12))


FASES_BANDA = {1: (65, 75), 2: (75, 82), 3: (78, 85), 4: (82, 95)}
_LEV_SIMPLE = re.compile(r'^([A-Za-zÁÉÍÓÚáéíóúñ ]+?)\s+(\d+x\d+)\s+@(\d+)(?:-(\d+))?%')


def validar(MES, titulo='Mes', imprimir=True, bloques=None, mes_del_ciclo=None):
    """Devuelve la lista de hallazgos [(nivel, regla, texto)]."""
    dias, sabados = [], []
    for semana, fechas, fase, jornadas, sabado in MES:
        for dia, cat, cap, skill, texto in jornadas:
            r = leer(texto)
            dias.append({'semana': semana, 'dia': dia, 'i': len(dias), 'cat': cat,
                         'cap': cap, 'skill': skill,
                         'movs': [base_de(m) for m in r['movimientos']],
                         'escalas': [base_de(m) for m in r['escalas']],
                         'formato': r['formato'], 'cap_texto': r['cap'], 'fase': fase})
        # La línea "Score / Evita" nombra movimientos que NO están en el WOD:
        # son justamente los que hay que evitar. Leerla hacía que el validador
        # denunciara como repetido entre sábados algo que solo estaba en el
        # aviso. Se corta antes de leer.
        cuerpo = sabado.split('Score:')[0]
        rs = leer(cuerpo)
        sabados.append({'semana': semana, 'movs': [base_de(m) for m in rs['movimientos']]})

    hallazgos = []
    def marcar(nivel, regla, texto):
        hallazgos.append((nivel, regla, texto))

    # --- R1  Balance Skill / WOD ----------------------------------------
    for d in dias:
        # El mes 2 no escribe los minutos de skill en la planilla: ahí no hay
        # nada que validar, no es que esté mal.
        if d['skill'] is None:
            continue
        lo, hi = SKILL_ESPERADO(d['cap'])
        if not (lo <= d['skill'] <= hi):
            marcar('revisar', 'Balance Skill/WOD',
                   f"S{d['semana']} {d['dia']}: WOD de {d['cap']}' lleva skill de {d['skill']}', "
                   f"y para ese cap corresponde {lo}'" + (f"-{hi}'" if hi != lo else ""))

    # --- R2  Las 4 categorías cada semana -------------------------------
    for semana, *_ in MES:
        cats = {d['cat'] for d in dias if d['semana'] == semana}
        faltan = {'STRENGTH', 'GYMNASTICS', 'METCON', 'ACCESSORY'} - cats
        if faltan:
            marcar('revisar', 'Categorías de la semana',
                   f"S{semana}: falta {', '.join(sorted(faltan))}")

    # --- R3  Rotación de categoría por día (STRENGTH exento) ------------
    porDia = defaultdict(list)
    for d in dias: porDia[d['dia']].append((d['semana'], d['cat']))
    # El criterio no es "nunca dos veces": su septiembre pone ACCESSORY el
    # viernes de S13 y otra vez el de S16, y está bien. Lo que no puede pasar
    # es que se vuelva predecible — tres veces al mes, o dos semanas seguidas.
    for cat in ('GYMNASTICS', 'METCON', 'ACCESSORY'):
        for dia, pares in porDia.items():
            semanas = sorted(s for s, c in pares if c == cat)
            etiqueta = ' y '.join('S' + str(s) for s in semanas)
            if len(semanas) > 2:
                marcar('revisar', 'Rotación de categoría',
                       f"{cat} cayó {dia} {len(semanas)} veces ({etiqueta}) — "
                       f"cualquiera diría que \"los {dia.lower()} son de {cat.lower()}\"")
            elif any(b - a == 1 for a, b in zip(semanas, semanas[1:])):
                marcar('revisar', 'Rotación de categoría',
                       f"{cat} cayó {dia} dos semanas seguidas ({etiqueta})")

    # --- R4  Dominios consecutivos --------------------------------------
    for i in range(len(dias) - 1):
        a, b = dias[i], dias[i+1]
        if a['semana'] != b['semana']: continue
        if DOMINIO(a['cap']) == DOMINIO(b['cap']):
            marcar('revisar', 'Dominios consecutivos',
                   f"S{a['semana']}: {a['dia']} y {b['dia']} son los dos {DOMINIO(a['cap'])} "
                   f"({a['cap']}' y {b['cap']}')")

    # --- R5  Distribución del mes ---------------------------------------
    c = Counter(DOMINIO(d['cap']) for d in dias)
    total = len(dias)
    detalle = []
    for dom, obj in OBJETIVO.items():
        real, esperado = c[dom], round(obj * total)
        detalle.append(f"{dom} {real} ({real/total:.0%}, objetivo {obj:.0%})")
        if abs(real - esperado) >= 3:
            marcar('informativo', 'Distribución del mes',
                   f"{dom}: {real} de {total} ({real/total:.0%}) contra un objetivo de {obj:.0%} "
                   f"— {'+' if real > esperado else '−'}{abs(real-esperado)}")

    # --- R6  Separación de burpees --------------------------------------
    apariciones = [d for d in dias if any('Burpee' in m for m in d['movs'])]
    for x, y in zip(apariciones, apariciones[1:]):
        sep = y['i'] - x['i']
        if sep < 3:
            marcar('revisar', 'Separación de burpees',
                   f"S{x['semana']} {x['dia']} y S{y['semana']} {y['dia']}: "
                   f"{sep} día(s) de separación, mínimo 3")

    # --- R7  Box Jump Over, máx 2 por semana ----------------------------
    for semana, *_ in MES:
        veces = [d for d in dias if d['semana'] == semana
                 and any('Box Jump' in m for m in d['movs'])]
        if len(veces) > 2:
            marcar('revisar', 'Box Jump Over', f"S{semana}: {len(veces)} veces, el máximo son 2")

    # --- R8  Movimientos repetidos en días consecutivos -----------------
    for i in range(len(dias) - 1):
        a, b = dias[i], dias[i+1]
        if a['semana'] != b['semana']: continue
        repes = set(a['movs']) & set(b['movs'])
        if repes:
            marcar('revisar', 'Movimiento en días seguidos',
                   f"S{a['semana']}: {', '.join(sorted(repes))} está el "
                   f"{a['dia'].lower()} y el {b['dia'].lower()}")

    # --- R9  Máximo 2 movimientos de la misma cadena por WOD ------------
    for d in dias:
        cuenta = Counter()
        for m in d['movs']:
            for cad in cadenas(m): cuenta[cad] += 1
        for cad, n in cuenta.items():
            if n > 2:
                cuales = [m for m in d['movs'] if cad in cadenas(m)]
                nivel = 'revisar' if 'empuje' in cad else 'informativo'
                marcar(nivel, 'Cadena muscular',
                       f"S{d['semana']} {d['dia']}: {n} movimientos de {cad} — {', '.join(cuales)}")

    # --- R10  (retirada) -------------------------------------------------
    # Tenía una regla que marcaba como error cualquier movimiento con "Técnico /
    # reps bajas = Sí" dentro de un WOD. Estaba mal: esa columna significa que va
    # a POCAS repeticiones, no que esté prohibido. Marcaba 7 falsos positivos —
    # Push Jerk, Squat Snatch, Power Clean— que él programa así a propósito.

    # --- R11  Sábados ----------------------------------------------------
    vistas = defaultdict(list)
    for s in sabados:
        mono = next((m for m in s['movs'] if 'monostructural' in cadenas(m)), None)
        if mono: vistas[mono].append(s['semana'])
    for mono, semanas in vistas.items():
        if len(semanas) > 2:
            marcar('revisar', 'Apertura de sábado',
                   f"{mono} abrió {len(semanas)} sábados ({', '.join('S'+str(s) for s in semanas)}) "
                   f"— en su septiembre la más repetida sale 2 veces")
        elif len(semanas) == 2 and abs(semanas[0] - semanas[1]) == 1:
            marcar('revisar', 'Apertura de sábado',
                   f"{mono} abrió dos sábados seguidos (S{semanas[0]} y S{semanas[1]})")

    for i, s in enumerate(sabados):
        for otro in sabados[i+1:]:
            repes = {m for m in set(s['movs']) & set(otro['movs'])
                     if m and 'monostructural' not in cadenas(m)}
            if repes:
                marcar('revisar', 'Repetición entre sábados',
                       f"S{s['semana']} y S{otro['semana']} comparten {', '.join(sorted(repes))} "
                       f"— en su septiembre los 8 puestos son distintos")

    # --- R12  La escala no puede ser otro movimiento del mismo WOD ------
    # "· 10 Pistol / 20 Air Squat (Esc)" junto a "· 12 Air Squat" deja al que
    # escala haciendo 32 sentadillas y al que va Rx, 12.
    for d in dias:
        choque = set(d['escalas']) & set(d['movs'])
        if choque:
            marcar('revisar', 'Escala que ya está en el WOD',
                   f"S{d['semana']} {d['dia']}: {', '.join(sorted(choque))} es la escala de un "
                   f"movimiento y además está como movimiento aparte")

    # --- R13  El mismo movimiento dos veces en un WOD -------------------
    for d in dias:
        rep = [m for m, n in Counter(d['movs']).items() if n > 1]
        if rep:
            marcar('revisar', 'Movimiento repetido en el WOD',
                   f"S{d['semana']} {d['dia']}: {', '.join(sorted(rep))} aparece dos veces")

    # --- R14  El % del bloque contra la banda de la fase -----------------
    # Va como DATO, no como falla. En sus tres meses, 6 de 12 bloques de
    # levantamiento simple caen fuera de la banda que declara su propio
    # encabezado — y el patrón del mes 4 sugiere que la banda describe dónde
    # TERMINA el mes, no dónde empieza: la S1 va a 75-80% (bajo la banda
    # @82-95%) y la S3 llega a 88-92% (dentro). Si es así la banda está bien
    # y lo que falta es decir que es el objetivo, no el rango.
    if bloques and mes_del_ciclo in FASES_BANDA:
        blo, bhi = FASES_BANDA[mes_del_ciclo]
        for clave, texto in sorted(bloques.items()):
            m = _LEV_SIMPLE.match(texto.split('\n')[0])
            if not m:
                continue
            lo, hi = int(m.group(3)), int(m.group(4) or m.group(3))
            if lo < blo or hi > bhi:
                marcar('informativo', 'Porcentaje fuera de la banda de fase',
                       f"{clave[0]} {clave[1]}: {m.group(1).strip()} a {lo}-{hi}%, "
                       f"y la fase del mes declara {blo}-{bhi}%")

    if imprimir:
        _informe(titulo, total, detalle, hallazgos)
    return hallazgos


def _informe(titulo, total, detalle, hallazgos):
    print(f"{titulo} · {total} WODs + {total // 5} sábados")
    print(f"Dominios: {' · '.join(detalle)}")
    print()
    orden = {'revisar': 0, 'informativo': 1}
    porRegla = defaultdict(list)
    for nivel, regla, texto in sorted(hallazgos, key=lambda h: (orden[h[0]], h[1])):
        porRegla[(nivel, regla)].append(texto)
    for (nivel, regla), textos in porRegla.items():
        marca = '▲ REVISAR ' if nivel == 'revisar' else '· dato    '
        print(f"{marca} {regla}")
        for t in textos: print(f"             {t}")
        print()
    revisar = sum(1 for h in hallazgos if h[0] == 'revisar')
    print(f"{revisar} para revisar · {len(hallazgos)-revisar} informativos")


if __name__ == '__main__':
    from septiembre import MES
    validar(MES, 'SEPTIEMBRE 2026 · Mes 4 · escrito a mano')
