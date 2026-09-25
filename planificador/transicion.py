# -*- coding: utf-8 -*-
"""Octubre con la semana de cierre de septiembre adelante, en una sola planilla.

POR QUÉ JUNTAS

Su mes 4 cierra el sábado 27 con la semana de TEST 1RM, y el mes 1 abre el
lunes 29 al @75%. Son dos días de distancia y el salto es el más grande del
ciclo: de buscar un máximo a la semana más liviana de los cuatro meses. Esa es
la regla que él decidió el 22 de septiembre —"la S1 de cada mes como descarga
del mes anterior"— y en dos planillas separadas no se ve.

LA SEMANA 16 ES SUYA, NO GENERADA

Va marcada como tal. Y va SIN bloque: septiembre está transcrito solo con los
WOD, sus bloques de fuerza no están en el archivo. Se escribe "no transcrito"
en vez de rellenarlo con algo parecido, porque una planilla que mezcla lo que
él escribió con lo que supuso la máquina, sin decir cuál es cuál, deja de
servir para revisar.

    python3 transicion.py [semilla]   ->  octubre-transicion.html
"""
import html
import sys
from datetime import date, timedelta

from semana import generar_mes, PUNTO
from bloque import FASES, PCT_POR_MES, TEST_DEL_MES, ROTULO_S4
from planilla_html import CSS, COLOR_CAT, MESES_ES, rango
from septiembre import MES as SEPTIEMBRE

PRIMER_LUNES_OCT = date(2026, 9, 29)

EXTRA = """
.origen{font-size:12px; letter-spacing:1px; text-transform:uppercase;
        padding:2px 8px; border-radius:3px; margin-left:8px; font-weight:700}
.suyo{background:#CCFF00; color:#000}
.maquina{background:#2a2a2a; color:#bbb}
.puente{border:1px solid var(--lima); background:#1a1f00; padding:14px 16px;
        margin:18px 0; font-size:15px; color:#e8ffb0; border-radius:4px}
.puente b{color:var(--lima); display:block; margin-bottom:5px; letter-spacing:.5px}
.sinbloque{color:#666; font-style:italic; font-size:13px; margin-bottom:10px}
"""


def _dia(cab_dia, cat, cap, skill, bloque, wod, punto):
    col = COLOR_CAT.get(cat, '#666')
    e = html.escape
    out = [f'<div class="dia" style="border-top-color:{col}">',
           f'<div class="cab"><span class="cat" style="color:{col}">{e(cab_dia)} · {e(cat)}</span><br>'
           f'<span class="min">{punto} {cap}\' · Skill {skill}\'</span></div>']
    if bloque is None:
        out.append('<div class="sinbloque">Bloque no transcrito de tu planilla</div>')
    else:
        out.append(f'<div class="bloque">{e(bloque)}</div>')
    out.append(f'<div class="wod">{e(wod)}</div></div>')
    return ''.join(out)


def render(semanas, semilla):
    e = html.escape
    s16 = SEPTIEMBRE[-1]          # (16, '22–27 sept', 'TEST 1RM', jornadas, sabado)
    fase1, banda1 = FASES[1]
    escalera = PCT_POR_MES[1]
    test1 = TEST_DEL_MES.get(1, 'ninguno')

    o = ['<!doctype html><html lang="es"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>CrossTrain EIM — Transición septiembre · octubre 2026</title>',
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">',
         f'<style>{CSS}{EXTRA}</style></head><body>',
         '<header>',
         '<h1>CrossTrain EIM — Cierre de septiembre y Mes 1</h1>',
         f'<div class="sub">Semana 16 a semana 20 · 22 septiembre al 25 de octubre · '
         f'Mes 4 {e(FASES[4][0])} cierra, Mes 1 {e(fase1)} {e(banda1)} abre · '
         '2 STRENGTH · 1 GYMNASTICS · 1 METCON · 1 ACCESSORY por semana</div>',
         '</header>']

    # --- Semana 16, la suya -------------------------------------------
    o.append(f'<div class="semana">Semana {s16[0]} · {e(s16[1])} · {e(s16[2])}'
             '<span class="origen suyo">tu planilla</span></div>')
    o.append('<div class="dias">')
    for dia, cat, cap, skill, texto in s16[3]:
        dom = 'fosfágeno' if cap < 14 else ('glucolítico' if cap <= 19 else 'aeróbico')
        o.append(_dia(dia, cat, cap, skill, None, texto, PUNTO[dom]))
    o.append('</div>')
    o.append('<div class="sabado"><div class="tit">Sábado 27 · Partner · 35\'</div>'
             f'<pre>{e(s16[4])}</pre></div>')

    # --- El puente ----------------------------------------------------
    o.append(
        '<div class="puente"><b>El salto, en dos días</b>'
        'El sábado 27 cierra el mes de Fuerza Máxima con la semana de test. '
        'El lunes 29 abre el Base al <b style="display:inline">@75%</b>, que es la '
        'semana más liviana de los cuatro meses. Es a propósito: la primera semana '
        'de cada mes descarga del mes anterior. Domingo 28 sin clases.</div>')

    # --- Las cuatro generadas ------------------------------------------
    for n, sem in enumerate(semanas, 1):
        pct = ROTULO_S4[test1] if n == 4 and test1 != 'ninguno' else escalera[n]
        o.append(f'<div class="semana">Semana {16 + n} · '
                 f'{e(rango(PRIMER_LUNES_OCT, n))} · {e(pct)}'
                 '<span class="origen maquina">generada</span></div>')
        o.append('<div class="dias">')
        for d in sem['dias']:
            o.append(_dia(d['dia'], d['cat'], d['cap'], d['skill'],
                          d['bloque'], d['wod'], PUNTO[d['dom']]))
        o.append('</div>')
        o.append('<div class="sabado"><div class="tit">Sábado · Partner · 35\'</div>'
                 f'<pre>{e(sem["sabado"])}</pre></div>')

    o.append('<div class="leyenda">')
    for linea in ['🟢 Corto &lt;14\'   🟡 Medio 14-19\'   🔴 Largo 20\'+   ·   objetivo 30 / 50 / 20',
                  '(Esc) versión escalada — se elige por movimiento, no por alumno',
                  '@% porcentaje del 1RM de la fase del mes',
                  'relay uno trabaja, el otro descansa   ·   JUNTOS los dos a la vez',
                  '* nota de coaching, no es trabajo extra',
                  'La semana 16 es tu planilla transcrita y va sin bloque: septiembre '
                  'está cargado solo con los WOD.']:
        o.append(f'<div>{linea}</div>')
    o.append('</div>')

    o.append('<footer>CrossTrain EIM · Head Coach <span class="cred">Luis Casali</span> · '
             '<span class="cred">@luis_casali</span><br>'
             'CF-L3 · CCFT · USAW L1 · HYROX Official Coach · Lead Coach Burgener Strength Latinoamérica'
             f'<br>Semanas 17-20 generadas con semilla {semilla}.'
             '</footer></body></html>')
    return '\n'.join(o)


if __name__ == '__main__':
    semilla = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    semanas = generar_mes(1, semilla=semilla)
    if not semanas:
        print('sin combinación')
        sys.exit(1)
    with open('octubre-transicion.html', 'w', encoding='utf-8') as f:
        f.write(render(semanas, semilla))
    print(f'octubre-transicion.html escrito · semilla {semilla}')
