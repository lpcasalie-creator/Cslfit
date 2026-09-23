# -*- coding: utf-8 -*-
"""El Partner WOD del sábado. Regla 8, más lo medido en sus cuatro sábados.

LA ESTRUCTURA, IDÉNTICA EN LOS CUATRO

  1. Monostructural JUNTOS     50 DU · 400m Run · 200m Farmer Carry
  2. 8 [levantamiento] @~55%   siempre 8 reps, siempre relay
  3. 10-15 [gimnasia]          con su (Esc) si el movimiento la lleva
  4. 10-12 [cuarto]            relay
  + Score: rondas + reps | Mejor dupla: 5-6 rondas | Evita: ...

LO QUE DICEN SUS CUATRO SÁBADOS (y corrige lo que yo había supuesto)

  · El levantamiento del sábado REPITE uno de la semana, más liviano:
    Push Jerk (lunes), Hang Power Clean (martes), Front Squat (lunes).
    3 de 4. Yo lo tenía al revés: excluía lo de la semana.
  · Los movimientos 3 y 4 también repiten la semana — 6 de 8 slots.
    El sábado es el repaso de la semana a ritmo de pareja, no un día nuevo.
  · Lo que NUNCA se repite es entre sábados del mismo mes: 4 levantamientos
    distintos, 8 movimientos distintos, cero cruces.
  · La apertura sí puede repetirse en el mes (Run en el sábado 2 y en el 4),
    pero nunca en sábados seguidos.
  · Nunca aparecen Air Squat ni Sit-Up en el sábado. Son relleno de día de
    semana; acá los cuatro puestos pesan.
"""
import random
from escalas import escala_de
from familias import familia_de

# Aperturas: nunca máquina (regla 8). Van "JUNTOS", no relay.
APERTURAS = [
 ('50 DU JUNTOS (25 c/u)',                  'Double under'),
 ('400m Run JUNTOS',                        'Run'),
 ('200m Farmer Carry KB JUNTOS (24/16 kg)', 'Farmer Carry'),
 ('800m Run JUNTOS',                        'Run'),
 ('100 Single Under JUNTOS (50 c/u)',       'Single Under'),
]

# El levantamiento del sábado: 8 reps al ~55%. Sus cuatro sábados del mes 3
# dicen @~55% en tres y @~60% en uno; yo tenía 60 fijo mirando septiembre.
LEVANTAMIENTOS = [
 ('Push Jerk', '115/75 lb'), ('Hang Power Clean', '115/75 lb'),
 ('Front Squat', '135/95 lb'), ('Power Snatch', '95/65 lb'),
 ('Power Clean', '115/75 lb'), ('Push Press', '115/75 lb'),
 ('Squat Clean', '115/75 lb'), ('Thruster', '95/65 lb'),
 ('Deadlift', '185/125 lb'), ('Squat Snatch', '95/65 lb'),
]

# Los puestos 3 y 4. Sin Air Squat ni Sit-Up: en sus cuatro sábados los ocho
# puestos son movimientos que pesan, y el relleno queda para el día de semana.
MOVIMIENTOS = [
 ('Pull-up', 12, None), ('Chest-to-Bar Pull-up', 10, None),
 ('Ring Dip', 10, None), ('Toes-to-Bar', 10, None), ('HSPU', 10, None),
 ('Bar Muscle-up', 5, None), ('Box Jump-Over', 12, '24"'),
 ('Burpee', 10, None), ('Wall Ball', 15, '20/14 lb'),
 ('KB swing', 12, '24/16 kg'), ('Devil Press', 10, '22/15 kg'),
 ('DB Snatch', 12, '22/15 kg'),
]

# La línea "Evita" vive en evita.py: sus cuatro líneas reales del mes 3 dicen
# que NUNCA nombra algo que el sábado use, y yo la tenía exactamente al revés.
from evita import evita_de, RELLENO


def armar_sabado(rnd, semana=None, sabados_del_mes=(), cargado_en_la_semana=(),
                 al_tope=None):
    """Devuelve (texto, movimientos_usados) o None si no hay combinación.

    `sabados_del_mes` son los movimientos de los sábados anteriores del mes:
    eso es lo único que se prohíbe de verdad. `cargado_en_la_semana` NO
    prohíbe — al contrario, orienta la elección del levantamiento.

    `al_tope(mov)` dice si ese movimiento ya gastó su cupo del mes. El sábado
    se arma DESPUÉS de los cinco días, así que sin esto pasaba por encima del
    techo: un movimiento que quedaba a uno del máximo lo cruzaba acá, y el
    Bar Muscle-up terminaba saliendo una vez de más todos los meses.
    """
    tope = al_tope or (lambda _m: False)
    usados_antes = {m for s in sabados_del_mes for m in s}
    semana_mov = list(cargado_en_la_semana)

    # 1. Apertura: nunca máquina, y nunca la misma que el sábado pasado.
    ultimo = set(sabados_del_mes[-1]) if sabados_del_mes else set()
    libres = [a for a in APERTURAS if a[1] not in ultimo and not tope(a[1])] \
             or [a for a in APERTURAS if a[1] not in ultimo] or APERTURAS
    texto_apertura, mov_apertura = rnd.choice(libres)

    # 2. Levantamiento: el sábado repasa un levantamiento de la semana, más
    #    liviano. Si ninguno sirve (ya salió en otro sábado del mes), se cae
    #    a la lista completa antes que a no generar nada.
    candidatos = [l for l in LEVANTAMIENTOS if l[0] not in usados_antes and not tope(l[0])]
    if not candidatos:
        return None
    de_la_semana = [l for l in candidatos if l[0] in semana_mov]
    lev, peso = rnd.choice(de_la_semana or candidatos)

    # 3 y 4. Dos movimientos más. Prohibido repetir sábados del mes; repetir
    #        la semana está permitido y de hecho es lo habitual (6 de 8).
    fam_lev = familia_de(lev)
    resto = [g for g in MOVIMIENTOS
             if g[0] not in usados_antes and g[0] not in (mov_apertura, lev)
             and familia_de(g[0]) != fam_lev and not tope(g[0])]
    if len(resto) < 2:
        return None
    rnd.shuffle(resto)

    # Uno repasa la semana y el otro no. En sus cuatro sábados el reparto es
    # 1 y 1 tres veces, y 0 y 2 una vez — nunca los dos de la semana.
    #
    # Y los dos puestos salen de familias distintas, con a lo más una escala
    # entre ambos: sus cuatro pares son Swing+Core colgante, Sentadilla+Fondos,
    # Tracción+Burpee y Tracción+Salto, y ninguno lleva dos (Esc).
    def compatible(a, b):
        if familia_de(a[0]) == familia_de(b[0]):
            return False
        return not (escala_de(a[0], a[1]) and escala_de(b[0], b[1]))

    de_semana = [g for g in resto if g[0] in semana_mov]
    fuera     = [g for g in resto if g[0] not in semana_mov]
    elegidos  = next((
        [a, b] for a in (de_semana or resto) for b in fuera if compatible(a, b)), None)
    if not elegidos:
        elegidos = next((
            [a, b] for i, a in enumerate(resto) for b in resto[i + 1:]
            if compatible(a, b)), None)
    if not elegidos:
        return None
    rnd.shuffle(elegidos)

    lineas = ["PARTNER WOD — AMRAP 35' | I go / You go", f'· {texto_apertura}']
    lineas.append(f'· 8 {lev} ({peso}) @~55% — relay')
    for mov, reps, peso_mov in elegidos:
        esc = escala_de(mov, reps)
        pieza = f'· {reps} {mov}' + (f' ({peso_mov})' if peso_mov else '')
        if esc:
            pieza += f' / {esc} (Esc)'
        lineas.append(pieza + ' — relay')

    usados_hoy = [mov_apertura, lev] + [m for m, _, _ in elegidos]
    evita = evita_de(semana_mov, usados_hoy)
    lineas.append('Score: rondas + reps | Mejor dupla: 5-6 rondas'
                  + (f" | Evita: {' · '.join(evita)}" if evita else ''))

    return '\n'.join(lineas), usados_hoy
