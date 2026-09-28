# -*- coding: utf-8 -*-
"""Las semanas 16 a 20 con el formato exacto de su planilla.

CALCADA DE LA FOTO DE SU MES 3, no inventada. Lo que la define:

  · Es una TABLA densa, sin aire entre celdas. Se lee como planilla, no como
    presentación. Bordes finos, todo pegado.
  · Cada día abre con una FRANJA DEL COLOR DE SU CATEGORÍA que lleva el
    nombre, el punto del dominio, el cap y el Skill en una sola línea:
    "STRENGTH 🟢 6' | Skill: 20'".
  · El bloque va suelto debajo, en gris, sin encabezado.
  · El WOD lleva SU PROPIA BARRA: "WOD — FOR TIME (Cap 7')".
  · LOS CUATRO SÁBADOS VAN JUNTOS AL FINAL, cada uno con su franja lima
    "SÁBADO — SEMANA 9 | 9 Agosto", y cierra con una franja lima con
    "Score: ... | Mejor dupla: ... | Evita: ...".
  · El encabezado y el pie van con pipes:
    "CrossTrain EIM — Mes 3 (Semanas 9–12) | Agosto 2026 | @luis_casali | CSL-Fit"

La versión anterior eran tarjetas con espacio entre medio y un sábado después
de cada semana. Se veía, en sus palabras, "demasiado generada por IA" — y la
mitad de eso era el layout, no el texto.

    python3 transicion.py [semilla]   ->  octubre-transicion.html
"""
import html
import sys
from datetime import date, timedelta

from semana import generar_mes, PUNTO
from septiembre import MES as SEPTIEMBRE

PRIMER_LUNES_OCT = date(2026, 9, 29)
DIAS = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']
MESES_ES = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
            'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Los colores de las franjas, leídos de su planilla del mes 3.
COLOR_CAT = {
    'STRENGTH':   '#23409c',
    'GYMNASTICS': '#7a2d9e',
    'METCON':     '#0e7a63',
    'ACCESSORY':  '#a32570',
}

CSS = """
*{box-sizing:border-box}
body{margin:0; background:#1a1a1a; padding:14px;
     font-family:'Barlow Condensed','Arial Narrow',Arial,sans-serif;}
table.p{width:100%; border-collapse:collapse; background:#0a0a0a; color:#fff;
        table-layout:fixed; font-size:12.5px; line-height:1.3}
td,th{border:1px solid #333; padding:0; vertical-align:top}
.tit{background:#CCFF00; color:#000; text-align:center; font-weight:700;
     font-size:15px; padding:5px; letter-spacing:.3px}
.meta{background:#0a0a0a; color:#9a9a9a; text-align:center; font-size:11px;
      padding:3px; letter-spacing:.2px}
.dias th{background:#141433; color:#fff; text-align:center; font-weight:700;
         font-size:13px; padding:4px; letter-spacing:1px}
.sem{background:#CCFF00; color:#000; font-weight:700; font-size:13px;
     padding:4px 8px; letter-spacing:.5px}
.cab{color:#fff; font-weight:700; font-size:12px; padding:3px 6px;
     letter-spacing:.3px; white-space:nowrap; overflow:hidden}
.blo{padding:5px 6px; color:#c9c9c9; font-size:11.5px; white-space:pre-wrap}
.wodbar{background:#1a1a3d; color:#fff; font-weight:700; font-size:12px;
        padding:3px 6px; border-top:1px solid #333; border-bottom:1px solid #333}
.wod{padding:5px 6px; color:#e8e8e8; font-size:11.5px; white-space:pre-wrap}
.sabtit{background:#CCFF00; color:#000; font-weight:700; font-size:13px;
        padding:4px 8px; letter-spacing:.5px}
.sabcab{color:#fff; font-weight:700; font-size:12.5px; padding:4px 8px}
.sabcuerpo{padding:2px 8px 5px; color:#e8e8e8; font-size:11.5px; white-space:pre-wrap}
.score{background:#CCFF00; color:#000; font-weight:700; font-size:10.5px;
       padding:2px 8px}
.pie{background:#0a0a0a; color:#bbb; text-align:center; font-size:11px; padding:5px}
.sq{display:inline-block; width:8px; height:8px; margin-right:4px}
"""


def rango(primer_lunes, n):
    lu = primer_lunes + timedelta(weeks=n - 1)
    sa = lu + timedelta(days=5)
    if lu.month == sa.month:
        return f'{lu.day} – {sa.day} {MESES_ES[lu.month]}'
    return f'{lu.day} {MESES_ES[lu.month]} – {sa.day} {MESES_ES[sa.month]}'


def _parte_wod(texto):
    """Su planilla separa la barra del WOD de su cuerpo. La barra es la
    primera línea; el generador ya la escribe con 'WOD — ' adelante y
    septiembre no, así que se normaliza acá."""
    lineas = texto.split('\n')
    barra = lineas[0].strip()
    if not barra.upper().startswith('WOD'):
        barra = f'WOD — {barra}'
    return barra, '\n'.join(lineas[1:])


def _celda(cat, cap, skill, bloque, wod, punto):
    e = html.escape
    col = COLOR_CAT.get(cat, '#444')
    barra, cuerpo = _parte_wod(wod)
    sk = f" | Skill: {skill}'" if skill else ''
    o = [f'<td><div class="cab" style="background:{col}">'
         f"{e(cat)} {punto} {cap}'{e(sk)}</div>"]
    if bloque:
        o.append(f'<div class="blo">{e(bloque)}</div>')
    o.append(f'<div class="wodbar">{e(barra)}</div>')
    o.append(f'<div class="wod">{e(cuerpo)}</div></td>')
    return ''.join(o)


def _sabado(titulo, texto):
    """El sábado de su planilla: franja lima con el título, el encabezado del
    partner, el cuerpo, y la línea de Score/Evita en otra franja lima."""
    e = html.escape
    lineas = [l for l in texto.split('\n') if l.strip()]
    cab = lineas[0]
    score = ''
    cuerpo = lineas[1:]
    if cuerpo and cuerpo[-1].lower().startswith('score'):
        score = cuerpo[-1]
        cuerpo = cuerpo[:-1]
    o = [f'<tr><td colspan="5" class="sabtit">{e(titulo)}</td></tr>',
         f'<tr><td colspan="5"><div class="sabcab">{e(cab)}</div>'
         f'<div class="sabcuerpo">{e(chr(10).join(cuerpo))}</div>']
    if score:
        o.append(f'<div class="score">{e(score)}</div>')
    o.append('</td></tr>')
    return ''.join(o)


def render(semanas):
    e = html.escape
    s16 = SEPTIEMBRE[-1]

    o = ['<!doctype html><html lang="es"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>CrossTrain EIM — Semanas 16-20</title>',
         '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">',
         f'<style>{CSS}</style></head><body><table class="p">',
         '<tr><td colspan="5" class="tit">CrossTrain EIM — Semanas 16–20 '
         '| Septiembre–Octubre 2026 | @luis_casali | CSL-Fit</td></tr>',
         '<tr><td colspan="5" class="meta">2 STRENGTH · 1 GYMNASTICS · 1 METCON '
         '· 1 ACCESSORY por semana | PROG. = Progresión | (Rx) = Rx | (Esc) = Escala</td></tr>',
         '<tr class="dias">' + ''.join(f'<th>{d}</th>' for d in DIAS) + '</tr>']

    # Semana 16 — el cierre del Mes 4, de su planilla.
    o.append(f'<tr><td colspan="5" class="sem">SEMANA {s16[0]} | '
             f'{e(s16[1].replace("sept", "Septiembre"))}</td></tr>')
    o.append('<tr>')
    for dia, cat, cap, skill, texto in s16[3]:
        dom = 'fosfágeno' if cap < 14 else ('glucolítico' if cap <= 19 else 'aeróbico')
        o.append(_celda(cat, cap, skill, None, texto, PUNTO[dom]))
    o.append('</tr>')

    # Semanas 17 a 20.
    for n, sem in enumerate(semanas, 1):
        numero = 16 + n
        o.append(f'<tr><td colspan="5" class="sem">SEMANA {numero} | '
                 f'{e(rango(PRIMER_LUNES_OCT, n))}</td></tr>')
        o.append('<tr>')
        for d in sem['dias']:
            o.append(_celda(d['cat'], d['cap'], d['skill'], d['bloque'],
                            d['wod'], PUNTO[d['dom']]))
        o.append('</tr>')

    # LOS SÁBADOS, TODOS JUNTOS AL FINAL. Así los ordena su planilla.
    sab16 = SEPTIEMBRE[-1]
    o.append(_sabado(f'SÁBADO — SEMANA {sab16[0]} | 27 Septiembre', sab16[4]))
    for n, sem in enumerate(semanas, 1):
        lu = PRIMER_LUNES_OCT + timedelta(weeks=n - 1)
        sa = lu + timedelta(days=5)
        o.append(_sabado(f'SÁBADO — SEMANA {16 + n} | {sa.day} {MESES_ES[sa.month]}',
                         sem['sabado']))

    cuadros = ''.join(
        f'<i class="sq" style="background:{COLOR_CAT[c]}"></i>{c}&nbsp;&nbsp; '
        for c in ('STRENGTH', 'GYMNASTICS', 'METCON', 'ACCESSORY'))
    o.append(f'<tr><td colspan="5" class="pie">{cuadros}| PROG. = Progresión '
             '| (Rx) = Rx | (Esc) = Escala | 🟢 Corto &lt;14\' · 🟡 Medio 14-19\' '
             '· 🔴 Largo 20\'+ · Objetivo 33/33/33</td></tr>')
    o.append('</table></body></html>')
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
