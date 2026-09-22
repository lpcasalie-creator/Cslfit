# -*- coding: utf-8 -*-
"""El bloque de Skill/Fuerza: lo que va antes del WOD.

Cuatro estructuras distintas, derivadas de los 20 bloques de septiembre.
Ninguna inventada.

  STRENGTH     un levantamiento + escalera de % + notas con *
               El % lo manda la fase del mes (regla 12), no el azar.
  GYMNASTICS   "N sets x calidad:" + 2-3 bloques PROG.
               El foco del ciclo se mantiene las cuatro semanas y progresa;
               los acompañantes rotan. En septiembre Bar MU estuvo en las 4.
  METCON       modalidad — propósito + intervalos + *Registrar
               El propósito progresa: técnica → umbral → VO2max → activación.
  ACCESSORY    "N sets x calidad:" + SIEMPRE 5 movimientos.
               Sets = minutos del bloque ÷ 4.
"""
import random
from notas import (notas_de_fuerza, notas_de_test, nota_single_pesado,
                   nota_metcon)

# --- Fases del mes (regla 12) -------------------------------------------
FASES = {
 1: ('Base',              '@65-75%'),
 2: ('Desarrollo',        '@75-82%'),
 3: ('Consolidación',     '@78-85%'),
 4: ('Fuerza Máxima',     '@82-95%'),
}
# Porcentaje por semana. Esto estaba MAL y de forma sistemática: mi escalera
# decía @70-75% para la semana 1, y sus doce bloques de levantamiento simple
# de los meses 2, 3 y 4 van de 75% a 88% en semana 1. Ninguno de los doce
# coincidía con lo que yo escribía.
#
# Y el error de fondo era otro: el porcentaje NO es función de la semana del
# mes, es función del MES. Solo el mes 4 tiene una escalera limpia que sube
# hacia el test; los meses 2 y 3 se quedan en su banda sin rampa.
#
#   Mes 2   S1 80-85   S2 70-80   S3 78-83      plano
#   Mes 3   S1 83-88   S2 83      S3 80         incluso baja
#   Mes 4   S1 75-82   S3 88-92   S4 TEST       sube fuerte
PCT_POR_MES = {
 2: {1: '@80-85%', 2: '@75-80%', 3: '@78-83%', 4: '@80-85%'},
 3: {1: '@83-88%', 2: '@83%',    3: '@80-85%', 4: '@83-88%'},
 4: {1: '@75-82%', 2: '@82-88%', 3: '@88-92%', 4: 'TEST 1RM'},
}

# EL MES 1 NO TIENE NI UN DATO. No existe la planilla, así que todo lo de
# abajo es extrapolación, no medición: la banda sale de su regla 12 ("Base
# @65-75%") y la escalera de repetir la forma del mes 2, que es el mes medido
# más cercano. Va marcado para que el generador pueda avisarlo, porque la
# diferencia entre "esto lo mediste tú" y "esto lo supuse yo" es justamente
# lo que hace confiable al resto.
PCT_POR_MES[1] = {1: '@65-70%', 2: '@68-73%', 3: '@70-75%', 4: '@70-75%'}
MESES_SIN_DATO = {1}

# Compatibilidad: el promedio de los meses medidos, para quien no pase el mes.
PCT_POR_SEMANA = PCT_POR_MES[3]

# LA SEMANA 4 NO ES SEMANA DE TEST EN TODOS LOS MESES. Yo la tenía forzada a
# 1RM siempre, y sus tres planillas dicen otra cosa:
#
#   Mes 2, S8    UN solo 1RM — Back Squat el martes. Los otros cuatro días son
#                bloques normales (Power Snatch + OHS, complejo de jerks...).
#   Mes 3, S12   CERO 1RM. Dos "Buscar pesado del día" — Snatch Balance + OHS
#                y Power Clean 3-2-2-1-1. Nunca escribe 1RM ese mes.
#   Mes 4, S16   Test completo: lunes de activación, Back Squat 1RM el martes,
#                Deadlift + Power Clean 1RM el jueves.
#
# Que el test esté al final del ciclo y no al final de cada mes es coherente
# con las fases: no se testea un 1RM en el mes "Base".
TEST_DEL_MES = {1: 'ninguno', 2: 'parcial', 3: 'ninguno', 4: 'completo'}
# Y el rótulo de la semana 4 tiene que decir lo que realmente pasa.
ROTULO_S4 = {'completo': 'TEST 1RM', 'parcial': 'TEST 1RM parcial',
             'ninguno': 'Pesado del día'}

LEVANTAMIENTOS = ['Back Squat', 'Deadlift', 'Front Squat', 'Power Clean',
                  'Squat Snatch', 'Push Press', 'Power Snatch', 'Bench Press']
# Un 1RM se busca en los levantamientos que se pueden fallar sin técnica: los
# suyos son Back Squat (mes 2 y mes 4), Deadlift y Power Clean (mes 4). Nunca
# testea un snatch — fallar un snatch al 95% es un problema de técnica, no de
# fuerza, y el número no dice nada.
LEVANTAMIENTOS_DE_TEST = ['Back Squat', 'Deadlift', 'Power Clean']
COMPLEJOS = ['Power Clean + Split Jerk', 'Snatch Balance + OHS',
             'Clean Pull + Squat Clean', 'Push Press + Push Jerk']

# Progresiones de gimnasia: foco del ciclo + acompañantes
PROGRESIONES = {
 'BAR MU':       ['5 Hip to Bar + 3 transición Pull+Push', '3/2 Bar MU completo',
                  '3/2 Bar MU — máximo intento', 'Max Bar MU unbroken'],
 'HSPU':         ['5/3 HSPU estricto', '5/3 HSPU con AbMat', '5/3 HSPU kipping',
                  'Max HSPU estricto unbroken'],
 'RING DIP':     ['6/4 Ring Dip estricto', '5/3 Ring Dip estricto',
                  '5/3 Ring Dip + :10 hold', 'Max Ring Dip estricto'],
 'SKIN THE CAT': ['3 German Hang :20', '3 Skin the Cat completo',
                  '3 Skin the Cat completo', '5 Skin the Cat + 10 Hollow Rock'],
 'L-SIT':        [':15 L-Sit en barras', ':20 L-Sit en anillas',
                  ':25 L-Sit en anillas', 'Max L-Sit en anillas'],
 'PISTOL':       ['5/5 Pistol a caja', '5/5 Pistol asistido',
                  '3/3 Pistol libre', 'Max Pistol libre c/lado'],
}
FOCO_DEL_CICLO = 'BAR MU'      # regla 6: no cambia el punto de partida cada semana

ACCESORIOS = [
 '10 DB Lateral Raise', '10 Face Pull', '8 Single Arm DB Row',
 '10 Glute Bridge con barra', '30" Side Plank c/lado', '10 Pendlay Row',
 '10 Single Leg RDL DB', '5/5 Turkish Get-Up (accesorio)',
 '30" Copenhagen Plank c/lado', '10 Ab Wheel', '20" L-Sit en anillas',
 '8 DB Row pesado c/lado', '10 Hip Thrust con barra', '10 Band Pull Apart',
 '12 Russian Twist KB', '10 Chest Supported Row', '10 DB Floor Press',
]

METCON_PROPOSITO = [
 ('Row — Pace + Técnica',  ['5 x 400m @pace 2k', '· 90" descanso',
                            'SPM objetivo: 26-28', '· Foco: drive de piernas',
                            '*Registrar pace c/400m']),
 ('Bike + Run — Threshold:',['4 x 1\' Bike @95% pace', '· 1\' descanso activo', '---',
                            '4 x 200m Run @90% pace', '· 90" descanso',
                            '*Registrar watts + pace']),
 ('Row — VO2max:',          ['6 x 250m @máximo pace', '· 1:30 descanso',
                            '*Registrar tiempo c/250m',
                            '*Objetivo: mantener pace constante']),
 ('Run — Pace Work:',       ['6 x 200m @90-95% pace', '· 90" descanso',
                            '*Foco: mantener el mismo pace',
                            '*Registrar tiempo c/200m']),
]

# La lista plana de notas se fue entera a notas.py, donde cada nota depende
# del levantamiento, del porcentaje de la semana y del mes del ciclo. De paso
# se cayó "*Foco: velocidad de barra", que yo había inventado: no aparece en
# ninguno de sus 60 bloques.


def sets_para(minutos):
    """Sus sets: 20'→5, 17'→4, 12'→3. Es minutos entre cuatro."""
    return max(3, min(5, round(minutos / 4)))


def escribir_bloque(rnd, categoria, minutos, semana_del_mes, mes_del_ciclo,
                    usados=(), cap_del_wod=None, dias_de_test=0):
    """Devuelve el texto del bloque, con la fase del mes ya aplicada.

    `dias_de_test` son los días de test ya usados esta semana: el mes 2 hace
    UNO y el mes 4 hace dos, así que no alcanza con mirar la semana.
    """
    test = TEST_DEL_MES.get(mes_del_ciclo, 'ninguno')
    escalera = PCT_POR_MES.get(mes_del_ciclo, PCT_POR_MES[3])
    pct = (ROTULO_S4[test] if semana_del_mes == 4 and test != 'ninguno'
           else escalera[semana_del_mes])
    hay_test_en_s4 = test != 'ninguno'

    if categoria == 'STRENGTH':
        cupo_de_test = {'completo': 2, 'parcial': 1, 'ninguno': 0}[test]
        if semana_del_mes == 4 and dias_de_test < cupo_de_test:
            lev = rnd.choice([l for l in LEVANTAMIENTOS_DE_TEST if l not in usados]
                             or LEVANTAMIENTOS_DE_TEST)
            return (f'{lev.upper()} — Buscar 1RM:\n'
                    '60%x5 → 72%x3 → 82%x2\n'
                    '→ 90%x1 → 95%x1 → 1RM\n'
                    + '\n'.join(notas_de_test(lev)))
        if semana_del_mes == 4:
            # Semana 4 sin cupo de test: single pesado, como su mes 3.
            lev = rnd.choice([l for l in LEVANTAMIENTOS if l not in usados] or LEVANTAMIENTOS)
            sets, nota = nota_single_pesado(cap_del_wod or 16)
            esquema = '3-2-1-1-1' if sets >= 5 else '3-2-2-1-1'
            return f'{lev} {esquema}\n(Buscar pesado del día)\n{nota}'
        if rnd.random() < 0.3:
            c = rnd.choice(COMPLEJOS)
            base = {1: 70, 2: 75, 3: 80}[semana_del_mes]
            return (f'{c}\n2+1 x 2 @{base}%\n2+1 x 2 @{base+6}%\n1+1 x 3 @{base+12}%+')
        lev = rnd.choice([l for l in LEVANTAMIENTOS if l not in usados] or LEVANTAMIENTOS)
        series = {1: '5x5', 2: '5x4', 3: '4x3'}[semana_del_mes]
        notas = notas_de_fuerza(lev, semana_del_mes, mes_del_ciclo, hay_test_en_s4)
        return f'{lev} {series} {pct}' + ('\n' + '\n'.join(notas) if notas else '')

    if categoria == 'GYMNASTICS':
        n = sets_para(minutos)
        acompañantes = [p for p in PROGRESIONES if p != FOCO_DEL_CICLO]
        rnd.shuffle(acompañantes)
        elegidas = [FOCO_DEL_CICLO] + acompañantes[:rnd.choice([1, 2])]
        lineas = [f'{n} sets x calidad:']
        for p in elegidas:
            lineas.append(f'PROG. {p}:')
            lineas.append('· ' + PROGRESIONES[p][semana_del_mes - 1])
        return '\n'.join(lineas)

    if categoria == 'METCON':
        # La activación solo existe si hay algo que testear. En su mes 3, que
        # no testea, el miércoles de la S12 es un Run — Pace Work normal.
        if semana_del_mes == 4 and test == 'completo':
            return ('Activación pre-test semana:\n'
                    "10' Row @60% pace suave\n5' Bike @60% pace suave\n"
                    '*No fatigar — activar CNS\n*Hidratación + movilidad')
        titulo, cuerpo = METCON_PROPOSITO[(semana_del_mes - 1) % len(METCON_PROPOSITO)]
        return titulo + '\n' + '\n'.join(cuerpo)

    # ACCESSORY: siempre cinco movimientos
    n = sets_para(minutos)
    movs = rnd.sample(ACCESORIOS, 5)
    return f'{n} sets x calidad:\n' + '\n'.join('· ' + m for m in movs)
