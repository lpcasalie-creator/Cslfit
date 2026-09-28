# -*- coding: utf-8 -*-
"""Las notas con * de los bloques, derivadas de sus 60 bloques reales.

Antes eran una lista plana y se sacaban al azar. Dos problemas con eso:

  · "*Foco: velocidad de barra" no aparece en NINGUNO de sus 60 bloques.
    La inventé yo.
  · Al azar salían combinaciones que él nunca escribe — dos descansos
    distintos en el mismo ejercicio, o una pausa en el fondo sobre un
    Deadlift, donde no hay fondo.

Sus notas no son decoración: cada tipo pertenece a un tipo de bloque.

LOS DOS ESTILOS, QUE NUNCA SE MEZCLAN

    meses 2-3   POTENCIACIÓN   "*3 Broad Jump entre sets"
    mes 4       DESCANSO+FOCO  "*Pausa 2\\" en el fondo" + "*Descanso 3' entre sets"

    6 bloques de cada uno, 0 que mezclen. Es una decisión de ciclo, no azar.

LA POTENCIACIÓN VA POR PATRÓN DEL LEVANTAMIENTO, y es 1:1 en sus datos:

    Back Squat  → 3 Broad Jump   (S5 y S9, las dos veces)
    Front Squat → 4 Broad Jump
    Deadlift    → 5 Box Jump     (S6 y S10, las dos veces)
    Strict Press→ 10 Lateral Raise

EL DESCANSO ESCALA CON LA INTENSIDAD

    5x5 @75-80%  → 3'      4x2 @88-92% → 4'      1RM → 4-5' + spot
"""

# --- Estilo potenciación (meses 2 y 3) ----------------------------------
# El movimiento de contraste sigue el patrón del levantamiento: salto
# horizontal para sentadilla, salto a cajón para bisagra, hombro para hombro.
POTENCIACION = {
 'Back Squat':    '*3 Broad Jump entre sets',
 'Front Squat':   '*4 Broad Jump entre sets',
 'Overhead Squat':'*3 Broad Jump entre sets',
 'Deadlift':      '*5 Box Jump entre sets',
 'Clean Pull':    '*5 Box Jump entre sets',
 'Strict Press':  '*10 Lateral Raise entre sets',
 'Push Press':    '*10 Lateral Raise entre sets',
 'Bench Press':   '*10 Band Pull Apart entre sets',
}

# --- Estilo descanso + foco (mes 4) -------------------------------------
# El descanso lo manda el porcentaje de la semana, no el gusto.
DESCANSO_POR_SEMANA = {1: "*Descanso 3' entre sets", 2: "*Descanso 3' entre sets",
                       3: "*Descanso 4' entre sets", 4: "*Descanso 4-5' entre sets pesados"}

# El foco técnico va por patrón. Solo estos dos existen en sus planillas: en
# los levantamientos olímpicos no escribe foco técnico, y no se lo invento.
FOCO_TECNICO = {
 'Back Squat':  '*Pausa 2" en el fondo',
 'Front Squat': '*Pausa 2" en el fondo',
 'Deadlift':    '*Foco: posición espalda baja',
}

# --- METCON --------------------------------------------------------------
# Siempre lleva un "*Registrar", y la métrica depende de la máquina: pace en
# Row y Run, watts en Bike. La unidad es la del intervalo, no una genérica.
METRICA = {'Row': 'pace', 'Run': 'pace', 'Bike': 'watts', 'Ski': 'pace'}


def nota_metcon(maquina, distancia=None, aerobico=False):
    """Las notas de un bloque de METCON: registrar, y si es pace work, el foco."""
    metrica = METRICA.get(maquina, 'tiempo')
    unidad = f'c/{distancia}m' if distancia else 'c/repetición'
    notas = [f'*Registrar {metrica} {unidad}']
    if aerobico:
        notas.append('*Foco: pace constante')
        notas.append('*No sprint — aeróbico base')
    return notas


def notas_de_fuerza(levantamiento, semana_del_mes, mes_del_ciclo, hay_test_en_s4):
    """Las notas con * de un bloque de fuerza normal (no de test)."""
    # El mes 1 entra acá por respuesta suya (22 sept): el Base lleva notas de
    # potenciación, como los meses 2 y 3, no descanso + foco técnico como el 4.
    # Hasta ahora caía en el `else` por descarte, que era una suposición mía.
    if mes_del_ciclo in (1, 2, 3):
        pot = POTENCIACION.get(levantamiento)
        return [pot] if pot else []

    notas = [DESCANSO_POR_SEMANA[semana_del_mes]]
    foco = FOCO_TECNICO.get(levantamiento)
    if foco:
        notas.append(foco)
    # La semana 3 mira hacia adelante cuando la 4 realmente testea. Sus dos
    # bloques de S15 dicen "*Preparar para 1RM S16" — y solo porque en S16
    # había test de verdad.
    if semana_del_mes == 3 and hay_test_en_s4:
        notas.append('*Preparar para 1RM')
    return notas


def notas_de_test(levantamiento):
    notas = ["*Descanso 4-5' entre sets pesados"]
    # El spot solo donde la barra puede caer encima: sentadilla y banca.
    if levantamiento in ('Back Squat', 'Front Squat', 'Bench Press'):
        notas.append('*Spot obligatorio en intentos máximos')
    return notas


def nota_single_pesado(cap_del_wod):
    """Un bloque de single pesado ajusta sus SETS al largo del WOD.

    Sus dos casos, los dos del mes 3:
        Snatch 3-2-1-1-1  con AMRAP 16'  → "*5 sets — WOD medio"
        Power Clean 3-2-2-1-1 con 22'    → "*3 sets — WOD largo"
    Menos WOD, más sets. Es la misma lógica del skill: lo que no se gasta en
    el WOD se puede gastar en la barra.
    """
    if cap_del_wod >= 20:
        return 3, '*3 sets — WOD largo'
    if cap_del_wod >= 14:
        return 5, '*5 sets — WOD medio'
    return 6, '*6 sets — WOD corto'
