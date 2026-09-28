# -*- coding: utf-8 -*-
"""Lee el GEN_POOLS de la app y lo deja en una estructura de Python.

SOLO LECTURA. Este módulo no toca index.html, y es a propósito: el plan es que
el catálogo termine siendo la única fuente de verdad y que GEN_POOLS se GENERE
desde él, pero el orden importa. Hoy la app tiene datos que el catálogo no
tiene, así que primero hay que leerla y usarla para enriquecer el catálogo.

Por qué la app sabe más que el catálogo:

  · El `Patrón` del catálogo no distingue vertical de horizontal. Un Strict
    Press y un Bench Press son los dos 'push'. En GEN_POOLS son push_vertical
    y push_horizontal, y esa diferencia es la que hace que un día de empuje
    vertical no sea un día de empuje horizontal.
  · Lo mismo con pull_vertical/pull_horizontal y con olympic_main/olympic_acc.
  · La `Categoría` del catálogo está vacía en 255 de 380 filas. De los 108
    movimientos que la app usa como fuerza, 77 no tienen categoría.

El parser NO usa un JSON: el bloque es JavaScript escrito a mano y tiene de
todo —`dip:  {` con dos espacios, `skill:{` sin ninguno, listas partidas en
dos líneas—. Se lee por líneas y se verifica el total al final. Si alguien
edita el bloque y el parser deja de recuperarlo entero, `leer_pools` levanta
una excepción en vez de devolver datos incompletos en silencio: un pool que
se pierde sin aviso es un movimiento que desaparece del generador de la app.

    python3 pools.py     ->  el resumen de lo que hay
"""
import re
import sys
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / 'index.html'

# Cuántas listas y cuántas entradas tiene que haber. Medido sobre el bloque
# actual: 19 claves × 2 niveles de equipo × 6 movimientos cada una.
LISTAS_ESPERADAS = 38
ENTRADAS_ESPERADAS = 228

EQUIPOS = ('limitado', 'completo')

# El patrón fino que la app conoce y el catálogo no. La clave es la del pool;
# el valor es lo que dice hoy la columna `Patrón` del catálogo.
PATRON_GRUESO = {
    'push_vertical': 'push', 'push_horizontal': 'push',
    'pull_vertical': 'pull', 'pull_horizontal': 'pull',
    'olympic_main': 'olympic', 'olympic_acc': 'olympic',
}

_FOCO = re.compile(r'^  (\w+): \{\s*$')
_CIERRE = re.compile(r'^  \},?\s*$')
# `squat: { limitado:[...],`  ·  `dip:  { limitado:[...],`  ·  `skill:{ limitado:[...]`
_CLAVE = re.compile(r'^    (\w+)\s*:\s*\{\s*(.*)$')
_LISTA = re.compile(r'(limitado|completo)\s*:\s*\[(.*?)\]')


def _movs(texto):
    return re.findall(r'"([^"]+)"', texto)


def leer_pools(ruta=APP):
    """{foco: {clave: {'limitado': [...], 'completo': [...]}}}"""
    fuente = Path(ruta).read_text(encoding='utf-8')
    i = fuente.find('const GEN_POOLS')
    if i < 0:
        raise RuntimeError(f'no encontré GEN_POOLS en {ruta}')
    fin = fuente.find('\n};', i)
    bloque = fuente[i:fin]

    pools, foco, clave = {}, None, None
    for linea in bloque.split('\n')[1:]:
        m = _FOCO.match(linea)
        if m:
            foco, clave = m.group(1), None
            pools[foco] = {}
            continue
        if _CIERRE.match(linea):
            foco = clave = None
            continue
        if foco is None:
            continue
        m = _CLAVE.match(linea)
        if m:
            clave = m.group(1)
            pools[foco][clave] = {}
            resto = m.group(2)
        else:
            # La continuación de una clave abierta en la línea anterior.
            resto = linea
        if clave is None:
            continue
        for equipo, lista in _LISTA.findall(resto):
            pools[foco][clave][equipo] = _movs(lista)

    listas = sum(len(c) for f in pools.values() for c in f.values())
    entradas = sum(len(v) for f in pools.values() for c in f.values()
                   for v in c.values())
    if listas != LISTAS_ESPERADAS or entradas != ENTRADAS_ESPERADAS:
        raise RuntimeError(
            f'el parser recuperó {listas} listas y {entradas} entradas, '
            f'esperaba {LISTAS_ESPERADAS} y {ENTRADAS_ESPERADAS}. '
            'Si el bloque cambió a propósito, actualizá las dos constantes; '
            'si no, el parser se está comiendo algo.')
    faltan = [(f, c) for f, cs in pools.items() for c, e in cs.items()
              for q in EQUIPOS if q not in e]
    if faltan:
        raise RuntimeError(f'claves sin los dos niveles de equipo: {faltan}')
    return pools


MUSC_LISTAS_ESPERADAS = 24       # 4 grupos × 3 roles × 2 equipos


def leer_musc(ruta=APP):
    """{grupo: {rol: {'limitado': [...], 'completo': [...]}}}

    MUSC_POOLS es el generador de musculación DE VERDAD. GEN_POOLS.musculacion
    existe pero no lo lee nadie: lo dice su propio comentario en index.html
    —"contenido MUERTO (verificado — _musculacionDay y _musculacionFullBody
    usan exclusivamente MUSC_POOLS) ... No se modifica ni se borra"— y quedó de
    una versión anterior al enfoque propio de Musculación.

    Acá los nombres traen el esquema pegado ('Leg Curl 3x15'), al revés de
    GEN_POOLS, que los tiene pelados.
    """
    fuente = Path(ruta).read_text(encoding='utf-8')
    i = fuente.find('const MUSC_POOLS')
    if i < 0:
        raise RuntimeError(f'no encontré MUSC_POOLS en {ruta}')
    bloque = fuente[i:fuente.find('\n};', i)]

    musc, grupo, rol = {}, None, None
    for linea in bloque.split('\n')[1:]:
        m = _FOCO.match(linea)
        if m:
            grupo, rol = m.group(1), None
            musc[grupo] = {}
            continue
        if _CIERRE.match(linea):
            grupo = rol = None
            continue
        if grupo is None:
            continue
        m = _CLAVE.match(linea)
        if m:
            rol = m.group(1)
            musc[grupo][rol] = {}
            resto = m.group(2)
        else:
            resto = linea
        if rol is None:
            continue
        for equipo, lista in _LISTA.findall(resto):
            musc[grupo][rol][equipo] = _movs(lista)

    listas = sum(len(r) for g in musc.values() for r in g.values())
    if listas != MUSC_LISTAS_ESPERADAS:
        raise RuntimeError(
            f'el parser recuperó {listas} listas de MUSC_POOLS, '
            f'esperaba {MUSC_LISTAS_ESPERADAS}')
    return musc


def por_movimiento(pools):
    """{movimiento: [(foco, clave, equipo), ...]}

    Un movimiento puede estar en más de un pool —Back Squat es fuerza/squat y
    también musculacion/legs, y Push-up está en limitado y en completo— así que
    esto es una lista, no un valor.
    """
    donde = {}
    for foco, claves in pools.items():
        for clave, niveles in claves.items():
            for equipo, movs in niveles.items():
                for m in movs:
                    donde.setdefault(m, []).append((foco, clave, equipo))
    return donde


if __name__ == '__main__':
    pools = leer_pools()
    donde = por_movimiento(pools)
    for foco, claves in pools.items():
        print(f'{foco}: {len(claves)} claves')
        for clave, niveles in claves.items():
            grueso = PATRON_GRUESO.get(clave)
            aviso = f'   (el catálogo solo dice "{grueso}")' if grueso else ''
            print(f'  {clave:17} '
                  f'limitado {len(niveles["limitado"])} · '
                  f'completo {len(niveles["completo"])}{aviso}')
    repetidos = {m: d for m, d in donde.items() if len(d) > 1}
    print(f'\n{len(donde)} movimientos distintos, '
          f'{sum(len(d) for d in donde.values())} entradas en total')
    print(f'{len(repetidos)} están en más de un pool:')
    for m, d in sorted(repetidos.items())[:12]:
        print(f'  {m:38} {[f"{f}/{c}/{e}" for f, c, e in d]}')
    if len(repetidos) > 12:
        print(f'  ... y {len(repetidos) - 12} más')
    sys.exit(0)
