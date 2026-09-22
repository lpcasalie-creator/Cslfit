# -*- coding: utf-8 -*-
"""Convertir una lista de movimientos en un WOD escrito.

Los rangos NO son de un manual: se midieron sobre los 24 WODs de septiembre.
Cuando un movimiento tiene un solo valor histórico, se usa ese; no se inventa
una variación que Luis nunca programó.
"""
import random, re
from ritmos import estimar, MARGEN_CAP
from escalas import escala_de
from collections import defaultdict
from reps import leer_reps
from septiembre import MES as _SEPT
import mes2 as _m2, mes3 as _m3

# Aprende de sus TRES meses, no solo de septiembre.
#
# Esto leía un mes y el efecto se sentía arriba: DIST solo conocía Run y Row,
# así que el generador tenía 14 de cupo de distancia para 14 días que la
# necesitan — cero holgura— y se quedaba sin combinación. Bike, Ski, Shuttle
# Run y Farmer Carry estaban transcritos desde hace días y nadie los miraba.
# De paso, los rangos de repeticiones, los pesos y los techos por movimiento
# pasan a tener el triple de observaciones.
MESES = list(_m2.MES) + list(_m3.MES) + list(_SEPT)
MES = MESES          # el resto del archivo ya recorre MES

# --- Aprender de su historia --------------------------------------------
REPS  = defaultdict(list)      # reps por ronda en formatos multironda
DIST  = defaultdict(list)
PESOS = {}

PESO_RE = re.compile(r'\((\d+)\s*/\s*(\d+)\s*(lb|kg)\)', re.I)
from leer_wod import leer

for s, f, fa, jornadas, sab in MES:
    for dia, cat, cap, sk, texto in jornadas:
        r = leer_reps(texto)
        # El chipper y el partner son de una ronda: sus reps no son comparables
        multironda = (r['rondas'] or 0) > 1 or r['formato'] in ('AMRAP','EMOM')
        for m, d in r['movimientos'].items():
            if d['tipo'] == 'distancia': DIST[m].append(d['valor'])
            elif d['por_ronda'] and multironda: REPS[m].append(d['por_ronda'])
    for texto in [t for *_, t in [(0, sab)]]:
        pass
    for linea in (sab + '\n' + '\n'.join(t for *_, t in jornadas)).split('\n'):
        pm = PESO_RE.search(linea)
        if not pm: continue
        mv = leer(linea)['movimientos']
        if mv: PESOS.setdefault(mv[0], []).append((int(pm.group(1)), int(pm.group(2)), pm.group(3).lower()))

# Cinco movimientos que él programa pero nunca escribió con carga en los tres
# meses transcritos, así que salían sin peso. Deducidos de sus propias anclas y
# aprobados por él el 22 de septiembre:
#
#   Back Squat      155/105   un escalón sobre su Front Squat (135/95)
#   Clean and Jerk  135/95    lo limita el jerk: Push Jerk 115/75, Squat Clean 135/95
#   Overhead Squat   95/65    lo limita la posición de snatch: sus dos snatch van 95/65
#   Split Jerk      135/95    su Push Jerk sale 115/75 dos veces y 135/95 una
#   Thruster         95/65    lo limita la sentadilla: bajo su Push Press (115/75)
#
# Van con `setdefault`: si mañana transcribe un mes donde sí escribió la carga,
# el dato medido gana y esto no lo pisa.
for _m, _p in (('Back Squat', (155, 105, 'lb')), ('Clean and Jerk', (135, 95, 'lb')),
               ('Overhead Squat', (95, 65, 'lb')), ('Split Jerk', (135, 95, 'lb')),
               ('Thruster', (95, 65, 'lb'))):
    PESOS.setdefault(_m, [_p])

# Respaldo: movimientos cuyo único dato histórico viene de un esquema
# (21-15-9). Se guarda la serie más chica del esquema, que es lo que él
# usaría como reps por ronda.
REPS_ESQUEMA = defaultdict(list)
for s_, f_, fa_, jornadas_, sab_ in MES:
    for dia_, cat_, cap_, sk_, texto_ in jornadas_:
        r_ = leer_reps(texto_)
        if r_['esquema']:
            for m_ in r_['movimientos']:
                REPS_ESQUEMA[m_].append(min(r_['esquema']))

# Techo por movimiento: el máximo que Luis ha programado de verdad. Escalar
# sin techo llevaba un chipper a 1400m de carrera y 100 box jump over, números
# que no están en ninguna de sus planillas.
TECHO = {}
for _s, _f, _fa, _jor, _sab in MES:
    for _d, _c, _cap, _sk, _t in list(_jor) + [(None, None, None, None, _sab)]:
        _r = leer_reps(_t)
        _rondas = _r['rondas'] or 1
        for _m, _dd in _r['movimientos'].items():
            _v = (_dd['valor'] if _dd['tipo'] == 'distancia'
                  else (_dd['total'] or (_dd['por_ronda'] or 0) * _rondas))
            if _v: TECHO[_m] = max(TECHO.get(_m, 0), _v)

# El trabajo monostructural no tiene el techo de septiembre: ahí no hubo nada
# largo, pero en los meses 2 y 3 sí —1000m Row en el "JACKIE" MOD, 800m Run en
# la escalera de empuje— y Luis lo confirmó: "aeróbico puede ser correr, remar,
# ski o bike, y puede ser largo".
TECHO.update({'Run': 2000, 'Row': 3000, 'Bike': 3000, 'Ski': 3000,
              'Shuttle Run': 800, 'Farmer Carry': 600})

# Dos techos distintos: cuánto se acumula en todo el WOD, y cuánto se hace DE
# UNA VEZ. Su pieza individual más larga es el 1000m Row del "JACKIE" MOD;
# 2000m corridos de un tirón no están en ninguna planilla suya.
TECHO_POR_VEZ = {'Run': 1000, 'Row': 1000, 'Bike': 1000, 'Ski': 1000,
                 'Farmer Carry': 200, 'Shuttle Run': 400}

FORMATO_POR_DOMINIO = {
 'fosfágeno':   [('FOR TIME', .55), ('ROUNDS', .30), ('AMRAP', .15)],
 'glucolítico': [('AMRAP', .40), ('EMOM', .30), ('ROUNDS', .30)],
 'aeróbico':    [('ROUNDS', .50), ('CHIPPER', .50)],
}

def _elegir(rnd, pares):
    x, acum = rnd.random(), 0
    for v, p in pares:
        acum += p
        if x <= acum: return v
    return pares[-1][0]

def reps_de(rnd, mov, factor=1.0):
    vals = REPS.get(mov) or REPS_ESQUEMA.get(mov)
    if not vals: return None
    base = rnd.choice(vals)
    # En un chipper, el multiplicador se aplica al revés de la dificultad: un
    # movimiento que normalmente va a 5 reps no se sube a 15. Su chipper de
    # septiembre fue 50 Air Squat / 40 Sit-up / 30 Box Jump / 20 Pull-up.
    if factor > 1.0:
        factor = factor if base >= 12 else (2.0 if base >= 9 else 1.5)
    n = int(round(base * factor))
    # Redondear a múltiplos de 5 cuando el número es grande, como lo escribe él
    if n >= 30: return int(round(n/10)*10)
    if n >= 20: return int(round(n/5)*5)
    return max(1, n)

def peso_de(mov):
    ps = PESOS.get(mov)
    if not ps: return None
    h, m, u = max(set(ps), key=ps.count)     # el más usado
    return f'{h}/{m} {u}'

def linea_de(rnd, mov, factor=1.0, emom=False):
    if mov in DIST:
        opciones = sorted(set(DIST[mov]))
        # En un EMOM el trabajo tiene que caber en el minuto: 500m de remo son
        # casi dos. Sus EMOM reales solo usan 200m Run.
        if emom: opciones = [d for d in opciones if d <= 200] or [min(opciones)]
        return f'· {rnd.choice(opciones)}m {mov}'
    n = reps_de(rnd, mov, factor)
    peso = peso_de(mov)
    txt = f'· {n} {mov}' if n else f'· {mov}'
    return txt + (f' ({peso})' if peso else '')

def cabe_en_un_minuto(mov):
    """En un EMOM el trabajo tiene que terminarse dentro del minuto."""
    if mov not in DIST: return True
    return min(DIST[mov]) <= 200

# El hueco de 12-13' NO es casualidad: en 60 días de los tres meses no hay un
# solo cap ahí. Su leyenda del mes 2 lo dice escrito — "Corto <12' · Medio
# 14-19' · Largo 20'+". Yo tenía el medio arrancando en 12.
RANGO = {'fosfágeno': (6, 11), 'glucolítico': (14, 19), 'aeróbico': (20, 26)}

def trabajo_del_wod(movs, reps_por_mov, rondas):
    return {m: reps_por_mov[m] * rondas for m in movs if reps_por_mov.get(m)}

# Sus rondas: 3, 3, 3, 4, 4, 4, 4, 5, 5 en septiembre. Nunca 2, nunca 6+.
RONDAS_POSIBLES = [3, 4, 5]
# El piso del cap es 6'. Ayer lo puse en 8 mirando SOLO septiembre, y los meses
# 2 y 3 lo desmienten: la semana 11 abre con un FOR TIME (Cap 6') de 7-5-3 de
# Clean & Jerk + T2B, y hay tres caps de 7'. Cuatro días en tres meses. Un mes
# no alcanza para fijar un piso.
PISO_CAP = 6
# Distancias que usa, para estirar un WOD sin tocar las reps de lo difícil
DISTANCIAS = {'Row': [250, 500, 750, 1000, 1500, 2000],
              'Run': [200, 400, 600, 800, 1000],
              'Bike': [500, 1000, 1500, 2000],
              'Farmer Carry': [100, 200, 400]}

def _distancia_redonda(mov, metros):
    """La distancia más cercana de las que él usa, sin pasarse del objetivo."""
    opciones = sorted(set(DISTANCIAS.get(mov, []) + list(DIST.get(mov, []))))
    candidatas = [d for d in opciones if d <= metros] or opciones[:1]
    return candidatas[-1] if candidatas else int(round(metros / 50) * 50)


def ajustar_a_dominio(dominio, movs, reps, rnd):
    """Busca rondas (3-5) y distancia que dejen el WOD dentro de su dominio.

    La distancia es la perilla, no las rondas: subir rondas multiplica también
    el movimiento difícil, y así salían cuarenta Bar Muscle-up.
    """
    lo, hi = RANGO[dominio]
    de_distancia = [m for m in movs if m in DIST]
    opciones = []
    for n in RONDAS_POSIBLES:
        combos = [[]] if not de_distancia else [
            [(m, d) for m, d in zip(de_distancia, combo)]
            for combo in __import__('itertools').product(
                *[DISTANCIAS.get(m, sorted(set(DIST[m]))) for m in de_distancia])]
        for combo in combos:
            r = dict(reps)
            for m, d in combo: r[m] = d
            # El techo también vale acá: 15 Box Jump por 5 rondas son 75, y su
            # máximo histórico son 60. Pero en vez de descartar la combinación
            # entera, se BAJAN las reps hasta que quepan — descartarla dejaba
            # sin solución a los días aeróbicos.
            r = dict(r)
            for m in movs:
                por_vez = TECHO_POR_VEZ.get(m)
                if por_vez and r[m] > por_vez: r[m] = por_vez
                techo = TECHO.get(m)
                if techo and r[m] * n > techo:
                    # Nunca por debajo de las reps más bajas que él ha usado:
                    # el techo de Pistol es 10 porque lo programó una sola vez,
                    # y dividido en cinco rondas daba 2. Un techo sacado de una
                    # observación no puede mandar sobre el rango real.
                    piso = min(REPS.get(m) or [r[m]])
                    if m not in DIST:
                        r[m] = max(piso, techo // n)
                    else:
                        # Una distancia se redondea a lo que él escribiría. El
                        # techo partido por las rondas daba "666m Run": 2000÷3.
                        # Nadie programa 666 metros.
                        r[m] = _distancia_redonda(m, max(1, techo // n))
            total = {m: r[m] * n for m in movs}
            cap = (estimar(total) + MARGEN_CAP) / 60
            opciones.append((abs(cap - (lo + hi) / 2), n, r, max(PISO_CAP, round(cap)), lo <= cap <= hi))
    if not opciones:   # con el techo no hay combinación: se usa lo mínimo
        n = RONDAS_POSIBLES[0]
        cap = (estimar({m: reps[m] * n for m in movs}) + MARGEN_CAP) / 60
        return n, reps, max(PISO_CAP, round(cap))
    dentro = [o for o in opciones if o[4]]
    elegidas = dentro or opciones
    elegidas.sort(key=lambda x: x[0])
    _, n, r, cap, _ = elegidas[0]
    # EL HUECO DE 12-13' NO EXISTE EN SUS PLANILLAS. Sesenta días de los tres
    # meses y ni uno solo ahí: su leyenda del mes 2 lo dice escrito, "Corto
    # <12' · Medio 14-19'". Un día pedido glucolítico que calcula 12 o 13
    # minutos no es un día corto — es el estimador quedándose a un minuto del
    # casillero. Se sube al piso del rango en vez de reclasificarlo.
    #
    # Sin esto, 76 de los 108 días que terminaban en el dominio equivocado eran
    # exactamente este caso, y de ahí salían los "dominios consecutivos".
    if dominio == 'glucolítico' and lo - 3 <= cap < lo:
        cap = lo
    return n, r, cap

def rondas_para(dominio, movs, reps_por_mov):
    """Cuántas rondas hacen que el WOD dure lo que su dominio pide.

    Al revés de como lo tenía antes: el cap no se elige, se calcula. Es la
    regla 4 de Luis —"cap = mejor atleta + 2-3'"— aplicada de verdad.
    """
    lo, hi = RANGO[dominio]
    mejor, mejor_dist = 1, 1e9
    for n in range(1, 13):
        cap = (estimar(trabajo_del_wod(movs, reps_por_mov, n)) + MARGEN_CAP) / 60
        if lo <= cap <= hi: return n, round(cap)
        d = min(abs(cap - lo), abs(cap - hi))
        if d < mejor_dist: mejor, mejor_dist = n, d
    cap = (estimar(trabajo_del_wod(movs, reps_por_mov, mejor)) + MARGEN_CAP) / 60
    return mejor, max(PISO_CAP, round(cap))

def escribir(rnd, dia):
    """Devuelve el texto del WOD. El cap NO se elige: se calcula del trabajo."""
    movs, dom = dia['movs'], dia['dom']

    # 1. Reps de cada movimiento, de sus rangos históricos
    reps = {}
    for m in movs:
        reps[m] = (rnd.choice(sorted(set(DIST[m]))) if m in DIST
                   else (reps_de(rnd, m) or 10))

    # 2. Cuántas rondas hacen que el WOD dure lo que el dominio pide
    rondas, reps, cap = ajustar_a_dominio(dom, movs, reps, rnd)

    # 3. El formato, ahora que el cap ya está
    fmt = _elegir(rnd, FORMATO_POR_DOMINIO[dom])
    if fmt == 'EMOM' and not all(cabe_en_un_minuto(m) for m in movs):
        fmt = 'AMRAP'
    if fmt == 'CHIPPER':
        # Un chipper es de una sola ronda: el volumen va en las reps. Hay que
        # buscar el factor que deja el WOD DENTRO de su dominio — antes
        # multiplicaba por las rondas y el resultado se salía: un día marcado
        # aeróbico terminaba con cap de 9 minutos.
        lo, hi = RANGO[dom]
        objetivo = (lo + hi) / 2 * 60 - MARGEN_CAP
        mejor, mejor_d = None, 1e9
        f = 1.0
        while f <= 8.0:
            r = {m: (reps[m] * (f if m in DIST else 1)) if m in DIST
                    else (reps_de(rnd, m, factor=f) or reps[m])
                 for m in movs}
            r = {m: min(int(round(v)), TECHO_POR_VEZ.get(m, TECHO.get(m, int(round(v)))))
                 for m, v in r.items()}
            d = abs(estimar(r) - objetivo)
            if d < mejor_d: mejor, mejor_d = r, d
            f += 0.25
        reps_chipper = mejor
        cap_chipper = max(6, round((estimar(reps_chipper) + MARGEN_CAP) / 60))
        if lo <= cap_chipper <= hi:
            reps, rondas, cap = reps_chipper, 1, cap_chipper
        else:
            # Con el techo puesto, el chipper no alcanza la duración del día.
            # Entonces el formato correcto es por rondas, no chipper.
            fmt = 'ROUNDS'

    def linea(m, emom=False):
        if m in DIST:
            d = reps[m]
            if emom and d > 200: d = 200
            return f'· {d}m {m}'
        peso = peso_de(m)
        base = f'· {reps[m]} {m}' + (f' ({peso})' if peso else '')
        # La línea (Esc) va solo en los movimientos de alta destreza, que es
        # donde él la pone: regla 6, pocas reps Rx más la escala con más reps.
        esc = escala_de(m, reps[m])
        # Y no se escribe si la escala es otro movimiento del mismo WOD. Salía
        # "· 10 Pistol / 20 Air Squat (Esc)" seguido de "· 12 Air Squat": el
        # que escala termina haciendo 32 sentadillas y el que va Rx, 12. La
        # escala tiene que ser más fácil que el Rx, no más trabajo que el WOD.
        if esc and any(otro != m and otro in esc for otro in movs):
            esc = None
        return base + (f' / {esc} (Esc)' if esc else '')

    # Las rondas van SIEMPRE en una línea aparte antes de los movimientos.
    # Metidas en el encabezado se leen como si el WOD fuera una sola vuelta:
    # "5 Rounds (Cap 24')" seguido de la lista se entiende como 4 minutos de
    # trabajo en vez de 21.
    encabeza_rondas = [f'{rondas} Rounds:'] if rondas > 1 else []

    if fmt == 'CHIPPER':
        cab, cuerpo = f"CHIPPER (Cap {cap}')", [linea(m) for m in movs]
    elif fmt == 'EMOM':
        cab = f"EMOM {cap}'"
        cuerpo = [f'{i+1}: {linea(m, emom=True)[2:]}' for i, m in enumerate(movs)]
        cuerpo.append(f'{len(movs)+1}: Rest')
    elif fmt == 'AMRAP':
        cab, cuerpo = f"AMRAP {cap}'", [linea(m) for m in movs]
    elif fmt == 'FOR TIME':
        cab = f"FOR TIME (Cap {cap}')"
        cuerpo = encabeza_rondas + [linea(m) for m in movs]
    else:
        cab = f"FOR TIME (Cap {cap}')"
        cuerpo = encabeza_rondas + [linea(m) for m in movs]
    return 'WOD — ' + cab + '\n' + '\n'.join(cuerpo), fmt, cap
