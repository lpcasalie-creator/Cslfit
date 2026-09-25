# -*- coding: utf-8 -*-
"""Semanas 16 a 20 en una planilla, para repartir a los coaches.

ESTE DOCUMENTO SE ENTREGA, NO SE REVISA

La primera versión llevaba etiquetas "tu planilla" / "generada", una banda
explicando el salto de porcentajes, una línea diciendo que los bloques de
septiembre no están transcritos, y la semilla en el pie. Todo eso servía
cuando el documento era para que Luis lo revisara. Un coach abre la planilla
para saber qué dicta el martes, y cada una de esas marcas le dice "esto lo
armó una máquina" — que fue exactamente su comentario.

Así que acá no hay nada que hable del documento. Solo la programación, con la
leyenda de su planilla: las cuatro categorías, los tres dominios y la
distribución objetivo 30/50/20 que dice el mes 2.

Las notas que quedan son notas de COACH —cortas, imperativas, sin explicar el
porqué— que es como él las escribe en los bloques: "*Descanso 2:00 entre
sets", "Evita: ...".

    python3 transicion.py [semilla]   ->  octubre-transicion.html
"""
import html
import sys
from datetime import date, timedelta

from semana import generar_mes, PUNTO
from bloque import PCT_POR_MES, TEST_DEL_MES, ROTULO_S4
from planilla_html import COLOR_CAT, MESES_ES
from septiembre import MES as SEPTIEMBRE

PRIMER_LUNES_OCT = date(2026, 9, 29)

# La nota de cada semana, en su voz: qué hacer, no por qué. La 17 es la que
# más se puede malinterpretar —viene de la semana de test y baja fuerte— así
# que es la única que lleva algo escrito.
NOTA_SEMANA = {
    17: 'Semana de descarga. Viene del test: no la subas.',
    20: 'Un solo 1RM en la semana. El resto de los días, bloque normal.',
}

CSS = """
:root{
  --negro:#0d0d0d; --panel:#141414; --panel2:#1b1b1b;
  --lima:#CCFF00; --blanco:#fff; --gris:#bbb; --borde:#2a2a2a;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--negro); color:var(--blanco);
  font-family:'Barlow Condensed','Arial Narrow',Arial,sans-serif;
  font-size:16px; line-height:1.45; padding:16px;
}
header{border-bottom:2px solid var(--lima); padding-bottom:12px; margin-bottom:8px}
h1{font-size:28px; margin:0 0 4px; color:var(--lima); letter-spacing:1px; text-transform:uppercase}
.sub{color:var(--gris); font-size:15px}
.semana{
  background:var(--lima); color:#000; font-weight:700; letter-spacing:1px;
  padding:7px 12px; margin:26px 0 0; font-size:17px; text-transform:uppercase;
  display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;
}
.semana .pct{font-weight:700}
.nota{background:var(--panel2); border-left:3px solid var(--lima); color:var(--blanco);
      padding:8px 12px; font-size:15px; margin-top:0}
.dias{display:grid; grid-template-columns:1fr; gap:10px; margin-top:10px}
@media(min-width:1000px){ .dias{grid-template-columns:repeat(5,1fr)} }
.dia{background:var(--panel); border:1px solid var(--borde); border-top-width:3px; padding:10px}
.cab{font-size:13px; letter-spacing:.5px; margin-bottom:8px}
.cat{font-weight:700; text-transform:uppercase}
.min{color:var(--gris)}
.bloque{white-space:pre-wrap; font-size:14px; color:var(--gris); margin-bottom:10px}
.wod{white-space:pre-wrap; font-size:15px; background:var(--panel2); padding:8px; border-left:2px solid var(--lima)}
.sabado{background:var(--panel); border:1px solid var(--borde); border-left:3px solid var(--lima); padding:10px; margin-top:10px}
.sabado .tit{color:var(--lima); font-weight:700; letter-spacing:1px; font-size:14px; margin-bottom:6px; text-transform:uppercase}
.sabado pre{white-space:pre-wrap; margin:0; font-family:inherit; font-size:15px}
.leyenda{margin-top:30px; padding:14px; background:var(--panel); border:1px solid var(--borde); font-size:14px; color:var(--gris)}
.leyenda .cats{display:flex; gap:18px; flex-wrap:wrap; margin-bottom:10px}
.leyenda .cats span{color:var(--blanco); font-weight:600; letter-spacing:.5px}
.leyenda .sq{display:inline-block; width:11px; height:11px; margin-right:6px}
.leyenda div{margin-bottom:3px}
footer{margin-top:30px; padding-top:14px; border-top:1px solid var(--borde); color:var(--gris); font-size:13px}
footer .cred{color:var(--lima)}
"""


def rango(primer_lunes, n):
    lu = primer_lunes + timedelta(weeks=n - 1)
    sa = lu + timedelta(days=5)
    if lu.month == sa.month:
        return f'{lu.day}–{sa.day} {MESES_ES[lu.month]}'
    return f'{lu.day} {MESES_ES[lu.month]} – {sa.day} {MESES_ES[sa.month]}'


def _dia(cab_dia, cat, cap, skill, bloque, wod, punto):
    col = COLOR_CAT.get(cat, '#666')
    e = html.escape
    out = [f'<div class="dia" style="border-top-color:{col}">',
           f'<div class="cab"><span class="cat" style="color:{col}">{e(cab_dia)} · {e(cat)}</span><br>'
           f'<span class="min">{punto} {cap}\' · Skill {skill}\'</span></div>']
    # Sin bloque no se escribe nada. Septiembre está transcrito solo con los
    # WOD, y un cartel diciéndolo es información sobre el archivo, no sobre el
    # entrenamiento: al coach no le sirve y delata la herramienta.
    if bloque:
        out.append(f'<div class="bloque">{e(bloque)}</div>')
    out.append(f'<div class="wod">{e(wod)}</div></div>')
    return ''.join(out)


def _banda(numero, fechas, pct, nota):
    e = html.escape
    o = [f'<div class="semana"><span>Semana {numero} · {e(fechas)}</span>'
         f'<span class="pct">{e(pct)}</span></div>']
    if nota:
        o.append(f'<div class="nota">{e(nota)}</div>')
    return ''.join(o)


def render(semanas):
    e = html.escape
    s16 = SEPTIEMBRE[-1]
    escalera = PCT_POR_MES[1]
    test1 = TEST_DEL_MES.get(1, 'ninguno')

    o = ['<!doctype html><html lang="es"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>CrossTrain EIM — Semanas 16 a 20</title>',
         '<link rel="preconnect" href="https://fonts.googleapis.com">',
         '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">',
         f'<style>{CSS}</style></head><body>',
         '<header><h1>CrossTrain EIM — Semanas 16 a 20</h1>',
         '<div class="sub">22 de septiembre al 25 de octubre · 2 STRENGTH · '
         '1 GYMNASTICS · 1 METCON · 1 ACCESSORY por semana</div></header>']

    o.append(_banda(s16[0], s16[1], s16[2], None))
    o.append('<div class="dias">')
    for dia, cat, cap, skill, texto in s16[3]:
        dom = 'fosfágeno' if cap < 14 else ('glucolítico' if cap <= 19 else 'aeróbico')
        o.append(_dia(dia, cat, cap, skill, None, texto, PUNTO[dom]))
    o.append('</div>')
    o.append('<div class="sabado"><div class="tit">Sábado · Partner · 35\'</div>'
             f'<pre>{e(s16[4])}</pre></div>')

    for n, sem in enumerate(semanas, 1):
        numero = 16 + n
        pct = ROTULO_S4[test1] if n == 4 and test1 != 'ninguno' else escalera[n]
        o.append(_banda(numero, rango(PRIMER_LUNES_OCT, n), pct,
                        NOTA_SEMANA.get(numero)))
        o.append('<div class="dias">')
        for d in sem['dias']:
            o.append(_dia(d['dia'], d['cat'], d['cap'], d['skill'],
                          d['bloque'], d['wod'], PUNTO[d['dom']]))
        o.append('</div>')
        o.append('<div class="sabado"><div class="tit">Sábado · Partner · 35\'</div>'
                 f'<pre>{e(sem["sabado"])}</pre></div>')

    # La leyenda de SU planilla: las cuatro categorías con su cuadrado, los
    # tres dominios y el 30/50/20 del mes 2. Nada más.
    o.append('<div class="leyenda"><div class="cats">')
    for cat in ('STRENGTH', 'GYMNASTICS', 'METCON', 'ACCESSORY'):
        o.append(f'<span><i class="sq" style="background:{COLOR_CAT[cat]}"></i>{cat}</span>')
    o.append('</div>')
    for linea in ['🟢 Corto &lt;14\'   ·   🟡 Medio 14-19\'   ·   🔴 Largo 20\'+   ·   '
                  'Distribución objetivo 30% / 50% / 20%',
                  '(Esc) versión escalada — se elige por movimiento, no por alumno',
                  '@% porcentaje del 1RM de la fase del mes',
                  'relay uno trabaja, el otro descansa   ·   JUNTOS los dos a la vez',
                  '* nota de coaching, no es trabajo extra']:
        o.append(f'<div>{linea}</div>')
    o.append('</div>')

    o.append('<footer>CrossTrain EIM · Head Coach <span class="cred">Luis Casali</span> · '
             '<span class="cred">@luis_casali</span><br>'
             'CF-L3 · CCFT · USAW L1 · HYROX Official Coach · '
             'Lead Coach Burgener Strength Latinoamérica</footer></body></html>')
    return '\n'.join(o)


if __name__ == '__main__':
    semilla = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    semanas = generar_mes(1, semilla=semilla)
    if not semanas:
        print('sin combinación')
        sys.exit(1)
    with open('octubre-transicion.html', 'w', encoding='utf-8') as f:
        f.write(render(semanas))
    print('octubre-transicion.html escrito')
