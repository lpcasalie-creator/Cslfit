# -*- coding: utf-8 -*-
"""Los formatos nuevos, aprobados por Luis el 22 de septiembre.

POR QUÉ HACEN FALTA

Sus 60 días usan seis formatos y el generador sabía hacer cinco:

    FOR TIME 27% · AMRAP 23% · ROUNDS 22% · EMOM 13% · CHIPPER 7% · ESCALERA 2%

La escalera es SUYA y no la sabía escribir. Los otros tres salen de medir dos
meses de CrossFit.com (63 días, 26 formatos distintos) — pero se agregan como
esquemas de escritura, no como programación copiada: el reparto de dominios,
los techos de volumen y la separación entre repeticiones siguen mandando
igual. Lo que cambia es CÓMO se escribe el mismo trabajo, no cuánto.

CADA UNO DEVUELVE (cabecera, cuerpo, cap) o None.

None significa "este formato no le sirve a este día" y el que llama vuelve al
formato clásico. Eso es a propósito: una escalera con 400m Run adentro no es
una escalera, y forzarla sería peor que no tenerla.
"""
from ritmos import estimar, MARGEN_CAP

# Los esquemas de escalera y su total de reps por movimiento. El total es lo
# que decide en qué dominio cae el día, así que están ordenados por eso.
#
#   21-15-9 es el canónico y el que él ya usó.
#   2-4-6-8-6-4-2 sube y baja: el alumno cree que va a la mitad y va al 60%.
ESCALERAS = [
 ('12-9-6',            [12, 9, 6]),
 ('15-12-9',           [15, 12, 9]),
 ('2-4-6-8-6-4-2',     [2, 4, 6, 8, 6, 4, 2]),
 ('21-15-9',           [21, 15, 9]),
 ('10-8-6-4-2',        [10, 8, 6, 4, 2]),
 ('21-18-15-12-9',     [21, 18, 15, 12, 9]),
]

# Cuánto sube la barra entre tramos de una escalera de carga. Los tres tramos
# de CrossFit.com van 95 → 125 → 155, o sea +30 y +30 en libras.
SALTO_DE_CARGA = 30

DESCANSOS = [60, 90, 120]        # segundos entre sets, de sus propios bloques


def _cap_de(trabajo_seg):
    return max(6, round((trabajo_seg + MARGEN_CAP) / 60))


def escalera(rnd, movs, dom, rango, linea, en_dist):
    """21-15-9 y familia. Todas las reps del esquema, en cada movimiento.

    No admite distancia: "21-15-9 de Run" no quiere decir nada. Tampoco más de
    tres movimientos — sus escaleras y las de CrossFit.com son de dos o tres,
    y con cuatro el esquema deja de leerse.
    """
    if any(en_dist(m) for m in movs) or not 2 <= len(movs) <= 3:
        return None
    lo, hi = rango
    opciones = []
    for nombre, esquema in ESCALERAS:
        total = sum(esquema)
        cap = _cap_de(estimar({m: total for m in movs}))
        if lo <= cap <= hi:
            opciones.append((nombre, esquema, cap))
    if not opciones:
        return None
    nombre, esquema, cap = rnd.choice(opciones)
    # Sin número por movimiento: el esquema del encabezado YA dice las reps.
    # La primera versión escribía el total (45 para un 21-15-9) debajo de cada
    # movimiento y se leía como 45 por ronda.
    return (f"ESCALERA {nombre} (Cap {cap}')",
            [linea(m, sin_reps=True) for m in movs], cap)


def escalera_de_carga(rnd, movs, dom, rango, linea, en_dist, peso_de):
    """21-15-9 con la barra subiendo: bajan las reps, sube el peso.

    Necesita exactamente UNA barra en la banda de carga (ver `_es_barra`). Con
    dos barras el esquema no se entiende, y sin ninguna no hay nada que subir.
    """
    if any(en_dist(m) for m in movs) or not 2 <= len(movs) <= 3:
        return None
    con_barra = [m for m in movs if _es_barra(peso_de(m))]
    if len(con_barra) != 1:
        return None
    barra = con_barra[0]
    lo, hi = rango
    opciones = []
    for nombre, esquema in ESCALERAS:
        if len(esquema) != 3:          # tres tramos, tres cargas
            continue
        total = sum(esquema)
        # La barra pesa más en los tramos de arriba, así que el trabajo real
        # es mayor que el de la misma escalera a carga fija. Un 15% es el
        # ajuste que deja los caps donde los deja su propio historial; sin él
        # la escalera de carga salía sistemáticamente corta.
        seg = estimar({m: total for m in movs}) * 1.15
        cap = _cap_de(seg)
        if lo <= cap <= hi:
            opciones.append((nombre, esquema, cap))
    if not opciones:
        return None
    nombre, esquema, cap = rnd.choice(opciones)

    cuerpo = [f'{nombre}:']
    cuerpo.append('· ' + barra + ' (' + _tres_cargas(peso_de(barra)) + ')')
    cuerpo += [linea(m, sin_reps=True) for m in movs if m != barra]
    return (f"ESCALERA DE CARGA (Cap {cap}')", cuerpo, cap)


def _es_barra(peso):
    """¿Ese peso es una barra? Su planilla lo dice sin decirlo: la barra va en
    libras y la mancuerna y la pesa rusa en kilos.

    Pero libras solo no alcanza: el Wall Ball también va en libras (20/14). Por
    eso además se pide carga de barra. Sin esto, la escalera de carga le subía
    veinte kilos a un Devil Press — 22 → 42 kg de mancuerna, que no existe.
    """
    if not peso:
        return False
    try:
        numeros, unidad = peso.rsplit(' ', 1)
        h = int(numeros.split('/')[0])
    except (ValueError, AttributeError):
        return False
    # Y una banda: con el Rx al medio, la barra va de h-30 a h+30. Abajo de 85 el
    # tramo liviano queda en 55 libras, que es menos que la barra vacía; arriba
    # de 155 el tramo pesado pasa de 185 y nueve reps ahí es una fila de gente
    # esperando discos. La banda es criterio mío: él nunca escribió una
    # escalera de carga.
    return unidad == "lb" and 85 <= h <= 155


def _tres_cargas(peso):
    """'95/65 lb' → '95/65 → 125/85 → 155/105 lb'.

    Solo llega acá lo que pasó por `_es_barra`, así que siempre son libras.

    El salto de la mujer NO es el mismo que el del hombre. Subir +30 a las dos
    columnas llevaba el Rx femenino de 65 a 125 libras —casi el doble— mientras
    el masculino subía un 63%. El salto se escala en la misma proporción en que
    ya están las dos cargas, que es la proporción que él usa en toda su
    planilla.
    """
    try:
        numeros, unidad = peso.rsplit(' ', 1)
        h, m = (int(x) for x in numeros.split('/'))
    except (ValueError, AttributeError):
        return peso
    salto_m = max(5, int(round(SALTO_DE_CARGA * m / h / 5)) * 5)
    # Su Rx queda en el tramo DEL MEDIO, no en el primero. El peso que él
    # escribe es para las 8-10 reps de un WOD normal: usarlo como arranque de
    # un 21-15-9 pedía 21 push press a 115 libras, que no es el mismo ejercicio.
    # Centrado, el tramo de 21 va más liviano y el de 9 más pesado, que es
    # justo lo que la escalera de carga quiere hacer.
    tramos = [f'{h + SALTO_DE_CARGA*i}/{m + salto_m*i}' for i in (-1, 0, 1)]
    return ' → '.join(tramos) + ' ' + unidad


def intervalos(rnd, movs, dom, rango, linea, reps):
    """N sets con descanso fijo. Dos sabores, y los dos miden cosas distintas.

    'for time' mide cuánto te demoras y el descanso es fijo: el alumno ve su
    caída de ritmo set a set. 'for reps' fija el reloj y mide cuánto entra.
    """
    lo, hi = rango
    trabajo = estimar(reps)
    if trabajo <= 0:
        return None
    for sets in (3, 4, 5):
        for descanso in DESCANSOS:
            cap = _cap_de(sets * (trabajo + descanso))
            if lo <= cap <= hi:
                if rnd.random() < 0.5:
                    cab = f"INTERVALOS — {sets} sets for time (Cap {cap}')"
                    cola = [f'Rest {descanso//60}:{descanso%60:02d} entre sets',
                            '*Anotar el tiempo de cada set']
                else:
                    bloque = max(2, round((trabajo + 30) / 60))
                    cab = (f"INTERVALOS — {sets} x {bloque}:00 for reps "
                           f"(Cap {cap}')")
                    cola = [f'Rest {descanso//60}:{descanso%60:02d} entre sets',
                            '*Score: reps totales de los cinco sets'
                            if sets == 5 else '*Score: reps totales']
                return cab, [linea(m) for m in movs] + cola, cap
    return None


def amrap_interrumpido(rnd, movs, dom, rango, linea, cap, corta_con):
    """AMRAP con una interrupción cada 2:00, y se retoma donde iba.

    El movimiento que interrumpe NO puede ser uno de los del AMRAP: si ya está
    adentro, parar para hacerlo no interrumpe nada.
    """
    if cap < 10 or not corta_con:
        return None
    mov, n = corta_con
    return (f"AMRAP {cap}' — interrumpido",
            [linea(m) for m in movs]
            + [f'Cada 2:00 parar: {n} {mov}, y retomar donde ibas'], cap)


def amrap_escalera(rnd, movs, dom, rango, linea, cap):
    """AMRAP que suma una rep del primer movimiento en cada ronda.

    Sube solo el primero. Subiendo todos, la ronda 8 es el triple de la 1 y
    nadie llega; subiendo uno, el WOD se alarga parejo.
    """
    if cap < 10 or len(movs) < 2:
        return None
    sube = movs[0]
    return (f"AMRAP {cap}' — escalera",
            [linea(m) for m in movs]
            + [f'+1 {sube} por ronda'], cap)
