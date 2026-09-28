# -*- coding: utf-8 -*-
"""Cuántas repeticiones de cada movimiento tiene un WOD."""
import re
from leer_wod import leer, norm, INDICE, sin_distancia, RUIDO

RONDAS   = re.compile(r'\b(\d+)\s*rounds?\b', re.I)
ESQUEMA  = re.compile(r'\b(\d+(?:\s*[-–]\s*\d+){1,})\b')
MINUTO   = re.compile(r'^\s*\d+\s*[:.]\s*')
REPS_LIN = re.compile(r'^\s*[·\-*•]?\s*(\d+)\s+(?!\s*(?:rounds?|min|m\b))')
DIST_LIN = re.compile(r'^\s*[·\-*•]?\s*(\d+)\s*(m|km|cal)\b', re.I)

def _movimiento(parte):
    p = sin_distancia(norm(parte))
    p = ' '.join(w for w in p.split() if w not in RUIDO)
    if not p: return None
    for patron, nombre in INDICE:
        if patron.search(p): return nombre
    return None

# "15/10 Cal Machine" es hombre/mujer, no un Rx con su escala. El corte por "/"
# que separa la escala lo partía en "15" y el movimiento se perdía entero: el
# Machine quedó sin un solo dato en las tres planillas y el generador le ponía
# un 10 pelado de respaldo. Se normaliza al número del hombre, que es la misma
# convención que ya usa el lector de pesos.
RX_DOBLE = re.compile(r'(\d+)\s*/\s*\d+(\s*(?:m|km|cal)\b)', re.I)


def leer_reps(texto):
    """Devuelve {'rondas': n|None, 'esquema': [..]|None, 'movimientos': {nombre: {...}}}"""
    lineas = [RX_DOBLE.sub(r'\1\2', ln) for ln in texto.split('\n')]
    base = leer(texto)

    rondas = None
    esquema = None
    for ln in lineas:
        m = RONDAS.search(ln)
        if m and rondas is None: rondas = int(m.group(1))
        e = ESQUEMA.search(ln)
        # Un esquema es 21-15-9: varios números y ningún movimiento en la línea
        if e and esquema is None and _movimiento(ln) is None:
            nums = [int(x) for x in re.split(r'[-–]', e.group(1))]
            if len(nums) >= 2: esquema = nums

    if rondas is None and (base['formato'] or '') == 'CHIPPER':
        rondas = 1   # el chipper se hace una vez de corrido

    out = {}
    for ln in lineas:
        principal = MINUTO.sub('', re.split(r'\s*/\s*|\s+o\s+', ln)[0])
        mov = _movimiento(principal)
        if not mov or mov in out: continue

        d = DIST_LIN.match(principal)
        if d:
            out[mov] = {'tipo': 'distancia', 'valor': int(d.group(1)), 'unidad': d.group(2).lower(),
                        'por_ronda': int(d.group(1)), 'total': None}
            continue

        r = REPS_LIN.match(principal)
        if r:
            por = int(r.group(1))
            total = por * rondas if rondas else None
        elif esquema:
            por, total = None, sum(esquema)
        else:
            por, total = None, None
        out[mov] = {'tipo': 'reps', 'por_ronda': por, 'total': total}

    # Con esquema, el total va a todos los movimientos sin reps propias
    if esquema:
        for mov, d in out.items():
            if d['tipo'] == 'reps' and d['total'] is None:
                d['total'] = sum(esquema); d['esquema'] = esquema

    return {'rondas': rondas, 'esquema': esquema, 'formato': base['formato'],
            'cap': base['cap'], 'movimientos': out, 'escalas': base.get('escalas', [])}
