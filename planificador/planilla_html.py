# -*- coding: utf-8 -*-
"""Rinde un mes generado como la planilla que él usa, en HTML.

Se lee en el teléfono: en pantalla angosta los cinco días se apilan, en ancha
quedan en las cinco columnas de siempre. Marca CSL-Fit —negro y lima—, pero
firmado como CrossTrain EIM, que es de quien es la programación.
"""
import html
import sys
from datetime import date, timedelta

from semana import generar_mes, PUNTO
from bloque import FASES, PCT_POR_MES, TEST_DEL_MES, ROTULO_S4, MESES_SIN_DATO

MESES_ES = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
            'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

COLOR_CAT = {
    'STRENGTH':   '#3d5afe',
    'GYMNASTICS': '#b14cff',
    'METCON':     '#00bfa5',
    'ACCESSORY':  '#e5399b',
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
header{border-bottom:2px solid var(--lima); padding-bottom:12px; margin-bottom:20px}
h1{font-size:26px; margin:0 0 4px; color:var(--lima); letter-spacing:.5px; text-transform:uppercase}
.sub{color:var(--gris); font-size:15px}
.aviso{
  border:1px solid #ffcc00; background:#2a2200; color:#ffcc00;
  padding:12px 14px; margin:16px 0; font-size:15px; border-radius:4px;
}
.aviso b{display:block; margin-bottom:4px; letter-spacing:.5px}
.semana{
  background:var(--lima); color:#000; font-weight:700; letter-spacing:1px;
  padding:7px 12px; margin:26px 0 0; font-size:17px; text-transform:uppercase;
}
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
footer{margin-top:34px; padding-top:14px; border-top:1px solid var(--borde); color:var(--gris); font-size:13px}
footer .cred{color:var(--lima)}
.leyenda{margin-top:20px; padding:12px; background:var(--panel); border:1px solid var(--borde); font-size:14px; color:var(--gris)}
.leyenda div{margin-bottom:3px}
"""


def rango(primer_lunes, n):
    lu = primer_lunes + timedelta(weeks=n - 1)
    sa = lu + timedelta(days=5)
    if lu.month == sa.month:
        return f'{lu.day}–{sa.day} {MESES_ES[lu.month]}'
    return f'{lu.day} {MESES_ES[lu.month]} – {sa.day} {MESES_ES[sa.month]}'


def render(semanas, mes, primer_lunes, primera_semana, titulo_mes):
    fase, banda = FASES[mes]
    test = TEST_DEL_MES.get(mes, 'ninguno')
    e = html.escape
    o = [
        '<!doctype html><html lang="es"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f'<title>CrossTrain EIM — Mes {mes} · {e(titulo_mes)}</title>',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">',
        f'<style>{CSS}</style></head><body>',
        '<header>',
        f'<h1>CrossTrain EIM — Mes {mes} · {e(fase)}</h1>',
        f'<div class="sub">Semanas {primera_semana}–{primera_semana + 3} · {e(titulo_mes)} · '
        f'{e(banda)} · 2 STRENGTH · 1 GYMNASTICS · 1 METCON · 1 ACCESSORY por semana</div>',
        '</header>',
    ]
    if mes in MESES_SIN_DATO:
        o.append(
            '<div class="aviso"><b>⚠ Mes sin planilla de referencia</b>'
            'Los porcentajes y la escalera de series son <b style="display:inline">extrapolados</b>, '
            'no medidos. La banda sale de tu regla 12; la escalera, de la forma del mes 2. '
            'Revísalos antes de publicar el mes.</div>')

    for n, sem in enumerate(semanas, 1):
        escalera = PCT_POR_MES.get(mes, PCT_POR_MES[3])
        pct = ROTULO_S4[test] if n == 4 and test != 'ninguno' else escalera[n]
        o.append(f'<div class="semana">Semana {primera_semana + n - 1} · '
                 f'{e(rango(primer_lunes, n))} · {e(pct)}</div>')
        o.append('<div class="dias">')
        for d in sem['dias']:
            col = COLOR_CAT.get(d['cat'], '#666')
            aviso = (f' <span class="min">▲ se pidió {e(d["dom_pedido"])}</span>'
                     if d.get('dom_pedido') and d['dom_pedido'] != d['dom'] else '')
            o.append(f'<div class="dia" style="border-top-color:{col}">')
            o.append(f'<div class="cab"><span class="cat" style="color:{col}">{e(d["dia"])} · {e(d["cat"])}</span><br>'
                     f'<span class="min">{PUNTO[d["dom"]]} {d["cap"]}\' · Skill {d["skill"]}\'{aviso}</span></div>')
            o.append(f'<div class="bloque">{e(d["bloque"])}</div>')
            o.append(f'<div class="wod">{e(d["wod"])}</div>')
            o.append('</div>')
        o.append('</div>')
        o.append('<div class="sabado"><div class="tit">Sábado · Partner · 35\'</div>'
                 f'<pre>{e(sem["sabado"])}</pre></div>')

    o.append('<div class="leyenda">')
    for linea in ['🟢 Corto &lt;14\'   🟡 Medio 14-19\'   🔴 Largo 20\'+   ·   objetivo 30 / 50 / 20',
                  '(Esc) versión escalada — se elige por movimiento, no por alumno',
                  '@% porcentaje del 1RM de la fase del mes',
                  'relay uno trabaja, el otro descansa   ·   JUNTOS los dos a la vez',
                  '* nota de coaching, no es trabajo extra']:
        o.append(f'<div>{linea}</div>')
    o.append('</div>')

    o.append('<footer>CrossTrain EIM · Head Coach <span class="cred">Luis Casali</span> · '
             '<span class="cred">@luis_casali</span><br>'
             'CF-L3 · CCFT · USAW L1 · HYROX Official Coach · Lead Coach Burgener Strength Latinoamérica'
             '</footer></body></html>')
    return '\n'.join(o)


if __name__ == '__main__':
    semilla = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    semanas = generar_mes(1, semilla=semilla)
    if not semanas:
        print('sin combinación'); sys.exit(1)
    salida = render(semanas, 1, date(2026, 9, 29), 17, 'Octubre 2026')
    with open('octubre.html', 'w', encoding='utf-8') as f:
        f.write(salida)
    print(f'octubre.html escrito — {len(salida)} chars')
