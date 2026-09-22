# -*- coding: utf-8 -*-
"""La línea "Evita" del sábado, derivada de sus cuatro líneas reales del mes 3.

Lo que yo tenía estaba AL REVÉS. Yo listaba primero los movimientos del propio
sábado; sus cuatro líneas no nombran ni una sola vez algo que el sábado use.
Tiene sentido de coaching y yo no lo había visto: la línea no describe el
sábado, avisa qué quedó cargado ESA SEMANA y el sábado no alcanzó a descargar.
Lo que el sábado sí trabajó ya no hace falta evitarlo — acaba de hacerse.

Las cuatro reglas que salen de sus cuatro líneas:

  1. Nunca nada que el sábado use. 4 de 4, y a nivel de FAMILIA: el sábado 10
     lleva Hang Power Snatch, y ese Evita no nombra ningún Snatch.
  2. Entra el levantamiento principal de un bloque de fuerza aunque no esté en
     ningún WOD — el "Push Jerk" de la semana 9 sale solo del bloque del lunes.
     No entran los accesorios de una lista "N sets x calidad".
  3. Nada de relleno: ni Air Squat, ni Sit-Up, ni Run, ni Row, ni DU.
  4. Cuando salieron dos variantes del mismo levantamiento, escribe la familia
     ("Snatch"); cuando salió una sola, escribe esa ("Squat Clean"). 4 de 4.

Largo: 4 o 5. Nunca más.
"""
from collections import Counter
from familias import familia_de
from categorizar import categoria_de
from leer_wod import leer

RELLENO = {'Air Squat', 'Sit-up', 'Sit-Up', 'Push-up', 'Push-Up', 'Run', 'Row',
           'Bike', 'Ski', 'Double under', 'Single Under', 'Machine',
           'Shuttle Run', 'Box Jump'}

# Cómo lo escribe él en la línea, que no es el nombre largo del catálogo.
CORTO = {'Clean and Jerk': 'C&J', 'Toes-to-Bar': 'T2B', 'Wall Ball': 'WBS',
         'Chest-to-Bar Pull-up': 'C2B', 'Bar Muscle-up': 'Bar MU',
         'Strict Pull-up': 'Strict Pull-Up', 'Pull-up': 'Pull-Up'}

# Las variantes que colapsa a una familia cuando aparecen dos en la semana.
RAIZ = {
 'Squat Snatch': 'Snatch', 'Power Snatch': 'Snatch', 'Snatch': 'Snatch',
 'Hang Power Snatch': 'Snatch', 'Snatch Balance': 'Snatch',
 'Hang Snatch': 'Snatch', 'OHS': 'Snatch', 'Overhead Squat': 'Snatch',
 'Squat Clean': 'Clean', 'Power Clean': 'Clean', 'Hang Power Clean': 'Clean',
 'Clean Pull': 'Clean',
 'Push Jerk': 'Jerk', 'Split Jerk': 'Jerk', 'Push Press': 'Jerk',
 # Burpee over Bar y Bar-Facing Burpee son el mismo burpee con una barra al
 # lado. Contarlos aparte le robaba un puesto a la lista.
 'Burpee over Bar': 'Burpee', 'Bar-Facing Burpee': 'Burpee',
}

# El orden de sus listas no es por frecuencia: es la barra primero. Sus cuatro
# líneas abren con Snatch, con Deadlift, con C&J y con Front Squat, y la
# gimnasia exigente va detrás. Lo que nunca aparece —Ring Dip, DB Lunge, FR
# Lunge, KB Swing— es justamente lo que no es ni barra ni gimnasia dura.
PESO_DE_CLASE = {'Fuerza': 0, 'Gimnasia': 1, 'Musculación': 2, 'Cardio': 3}

TOPE = 5


def _raiz(m):
    return RAIZ.get(m, m)


def evita_de(movs_de_la_semana, movs_del_sabado, tope=TOPE):
    """`movs_de_la_semana` en orden de día, con repeticiones — el conteo importa."""
    # 1. Fuera todo lo que el sábado trabaja, a nivel de familia y de raíz.
    fuera = set()
    for m in movs_del_sabado:
        fuera |= {m, _raiz(m)}
        if familia_de(m):
            fuera |= {o for o in movs_de_la_semana if familia_de(o) == familia_de(m)}

    cands = [m for m in movs_de_la_semana if m not in fuera and _raiz(m) not in fuera
             and m not in RELLENO]
    if not cands:
        return []

    veces = Counter(_raiz(m) for m in cands)
    # Última aparición: lo más reciente de la semana pesa más.
    ultima = {}
    for i, m in enumerate(cands):
        ultima[_raiz(m)] = i

    # 4. Si de una raíz salieron dos variantes distintas, se escribe la raíz.
    variantes = {}
    for m in cands:
        variantes.setdefault(_raiz(m), set()).add(m)

    def clase(r):
        vs = variantes[r]
        return min(PESO_DE_CLASE.get(categoria_de(v), 4) for v in vs)

    orden = sorted(veces, key=lambda r: (clase(r), -veces[r], -ultima[r]))
    salida = []
    for r in orden[:tope]:
        vs = variantes[r]
        nombre = r if len(vs) > 1 else next(iter(vs))
        salida.append(CORTO.get(nombre, nombre))
    return salida


def cargado_en(jornadas, bloques, semana):
    """Lo que la semana puso encima: cada WOD entero + el levantamiento
    principal de cada bloque de fuerza (la primera línea), nunca los accesorios.
    """
    out = []
    for dia, cat, cap, sk, texto in jornadas:
        b = bloques.get((semana, dia), '')
        primera = b.split('\n')[0] if b else ''
        # Un bloque de fuerza abre con el levantamiento; uno de calidad abre
        # con "N sets x calidad:" o "EMOM 15'", y ahí no hay nada que sumar.
        # "Power Clean + Push Jerk" son DOS levantamientos. Sin cortar por el
        # "+" el lector devolvía un solo nombre inventado, y por eso el
        # Push Jerk de la semana 9 —que sale solo de ahí— nunca llegaba.
        if primera and 'calidad' not in primera.lower() and 'sets' not in primera.lower():
            for pieza in primera.split('+'):
                out += leer(pieza)['movimientos']
        out += leer(texto)['movimientos']
    return out
