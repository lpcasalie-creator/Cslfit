# -*- coding: utf-8 -*-
"""La planilla de las semanas 16 a 20 como archivo de Excel.

MISMO FORMATO QUE EL HTML, no una tabla de datos. Pidió Excel porque la imagen
no se leía bien —quiere hacer zoom, imprimir y editar—, no porque quisiera
otro diseño. Así que el .xlsx repite la planilla: franja lima por semana, las
cinco columnas de días, la franja de color de cada categoría, la barra del WOD
y los cinco sábados juntos al final.

Cada día ocupa cuatro filas, que es en lo que se descompone una celda del HTML:

    categoría   STRENGTH 🟢 17' | Skill: 17'      ← franja del color de la categoría
    bloque      Push Press 5x5 @75% ...
    barra WOD   WOD — AMRAP 17'
    WOD         · 9 Push Press (115/75 lb) ...

Sin fórmulas: es un documento para leer y repartir, no un modelo de cálculo.

    python3 excel.py [semilla]   ->  octubre-semanas-16-20.xlsx
"""
import sys
from datetime import timedelta

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from semana import generar_mes, PUNTO
from septiembre import MES as SEPTIEMBRE
from transicion import (PRIMER_LUNES_OCT, DIAS, MESES_ES, COLOR_CAT,
                        rango, _parte_wod)

LIMA = 'CCFF00'
NEGRO = '0D0D0D'
PANEL = '141414'
BARRA_WOD = '1A1A3D'
CAB_DIAS = '141433'
BLANCO = 'FFFFFF'
GRIS = 'C9C9C9'

FUENTE = 'Arial Narrow'      # condensada y estándar, como su Barlow Condensed
BORDE = Border(*[Side(style='thin', color='333333')] * 4)


def _pinta(c, fondo=NEGRO, color=BLANCO, negrita=False, tam=10,
           ajuste=True, arriba=True, centro=False):
    c.font = Font(name=FUENTE, size=tam, bold=negrita, color=color)
    c.fill = PatternFill('solid', fgColor=fondo)
    c.alignment = Alignment(wrap_text=ajuste,
                            vertical='top' if arriba else 'center',
                            horizontal='center' if centro else 'left')
    c.border = BORDE
    return c


def _franja(ws, fila, texto, fondo=LIMA, color='000000', tam=11, negrita=True,
            centro=False):
    """Una fila que cruza las cinco columnas."""
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=5)
    _pinta(ws.cell(fila, 1, texto), fondo, color, negrita, tam,
           ajuste=False, arriba=False, centro=centro)
    for col in range(2, 6):
        _pinta(ws.cell(fila, col), fondo, color, negrita, tam)
    ws.row_dimensions[fila].height = 18
    return fila + 1


def _alto(textos, ancho_car=46, minimo=15):
    """Alto de fila que alcanza para el texto más largo de la fila."""
    lineas = 0
    for t in textos:
        for ln in (t or '').split('\n'):
            lineas += max(1, -(-len(ln) // ancho_car))
    return max(minimo, min(260, 12.5 * max(1, lineas // max(1, len(textos)) + 1)))


def _semana(ws, fila, titulo, dias):
    """Una semana: franja + las cuatro filas de los cinco días."""
    fila = _franja(ws, fila, titulo)

    cabs, bloques, barras, cuerpos = [], [], [], []
    for d in dias:
        cabs.append((d['cat'], f"{d['cat']} {PUNTO[d['dom']]} {d['cap']}'"
                     + (f" | Skill: {d['skill']}'" if d['skill'] else '')))
        bloques.append(d.get('bloque') or '')
        b, c = _parte_wod(d['wod'])
        barras.append(b)
        cuerpos.append(c)

    for i, (cat, txt) in enumerate(cabs, 1):
        _pinta(ws.cell(fila, i, txt), COLOR_CAT.get(cat, '444444')[1:],
               BLANCO, True, 10, ajuste=False, arriba=False)
    ws.row_dimensions[fila].height = 16
    fila += 1

    if any(bloques):
        for i, txt in enumerate(bloques, 1):
            _pinta(ws.cell(fila, i, txt), PANEL, GRIS, False, 9.5)
        ws.row_dimensions[fila].height = _alto(bloques)
        fila += 1

    for i, txt in enumerate(barras, 1):
        _pinta(ws.cell(fila, i, txt), BARRA_WOD, BLANCO, True, 10,
               ajuste=False, arriba=False)
    ws.row_dimensions[fila].height = 16
    fila += 1

    for i, txt in enumerate(cuerpos, 1):
        _pinta(ws.cell(fila, i, txt), NEGRO, 'E8E8E8', False, 9.5)
    ws.row_dimensions[fila].height = _alto(cuerpos)
    return fila + 1


def _sabado(ws, fila, titulo, texto):
    fila = _franja(ws, fila, titulo)
    lineas = [l for l in texto.split('\n') if l.strip()]
    cab, cuerpo = lineas[0], lineas[1:]
    score = ''
    if cuerpo and cuerpo[-1].lower().startswith('score'):
        score, cuerpo = cuerpo[-1], cuerpo[:-1]
    fila = _franja(ws, fila, cab, NEGRO, BLANCO, 10)
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=5)
    _pinta(ws.cell(fila, 1, '\n'.join(cuerpo)), NEGRO, 'E8E8E8', False, 9.5)
    for col in range(2, 6):
        _pinta(ws.cell(fila, col), NEGRO)
    ws.row_dimensions[fila].height = max(15, 12.5 * len(cuerpo))
    fila += 1
    if score:
        fila = _franja(ws, fila, score, LIMA, '000000', 9)
    return fila


def construir(semanas, destino):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Semanas 16-20'
    ws.sheet_view.showGridLines = False
    for col in range(1, 6):
        ws.column_dimensions[get_column_letter(col)].width = 34

    f = _franja(ws, 1, 'CrossTrain EIM — Semanas 16–20 | Septiembre–Octubre 2026 '
                '| @luis_casali | CSL-Fit', LIMA, '000000', 13, True, centro=True)
    f = _franja(ws, f, '2 STRENGTH · 1 GYMNASTICS · 1 METCON · 1 ACCESSORY por semana '
                '| PROG. = Progresión | (Rx) = Rx | (Esc) = Escala',
                NEGRO, '9A9A9A', 9, False, centro=True)
    for i, d in enumerate(DIAS, 1):
        _pinta(ws.cell(f, i, d), CAB_DIAS, BLANCO, True, 11,
               ajuste=False, arriba=False, centro=True)
    ws.row_dimensions[f].height = 18
    f += 1

    s16 = SEPTIEMBRE[-1]
    dias16 = []
    for dia, cat, cap, skill, texto in s16[3]:
        dom = 'fosfágeno' if cap < 14 else ('glucolítico' if cap <= 19 else 'aeróbico')
        dias16.append({'cat': cat, 'cap': cap, 'skill': skill, 'dom': dom,
                       'bloque': '', 'wod': texto})
    f = _semana(ws, f, f'SEMANA {s16[0]} | {s16[1].replace("sept", "Septiembre")}',
                dias16)

    for n, sem in enumerate(semanas, 1):
        f = _semana(ws, f, f'SEMANA {16 + n} | {rango(PRIMER_LUNES_OCT, n)}',
                    sem['dias'])

    f = _sabado(ws, f, f'SÁBADO — SEMANA {s16[0]} | 27 Septiembre', s16[4])
    for n, sem in enumerate(semanas, 1):
        sa = PRIMER_LUNES_OCT + timedelta(weeks=n - 1, days=5)
        f = _sabado(ws, f, f'SÁBADO — SEMANA {16 + n} | {sa.day} {MESES_ES[sa.month]}',
                    sem['sabado'])

    f = _franja(ws, f, '■ STRENGTH   ■ GYMNASTICS   ■ METCON   ■ ACCESSORY   '
                '| PROG. = Progresión | (Rx) = Rx | (Esc) = Escala',
                NEGRO, GRIS, 9, False, centro=True)
    _franja(ws, f, "🟢 Corto <14'  ·  🟡 Medio 14-19'  ·  🔴 Largo 20'+  ·  "
            'Objetivo 33/33/33', NEGRO, GRIS, 9, False, centro=True)

    ws.freeze_panes = 'A4'          # el encabezado y los días quedan fijos
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(destino)
    return destino


if __name__ == '__main__':
    semilla = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    semanas = generar_mes(1, semilla=semilla)
    if not semanas:
        print('sin combinación')
        sys.exit(1)
    print(construir(semanas, 'octubre-semanas-16-20.xlsx'), 'escrito')
