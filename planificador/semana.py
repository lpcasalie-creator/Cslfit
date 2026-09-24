# -*- coding: utf-8 -*-
"""Una semana completa de CrossTrain EIM: bloque + WOD los cinco días, más el
Partner WOD del sábado. Y el mes entero, que es la unidad real de su planilla.
"""
import random
import generar2 as g
from prescribir import escribir
from bloque import (escribir_bloque, FASES, PCT_POR_MES,
                    TEST_DEL_MES, ROTULO_S4, MESES_SIN_DATO, AVISO_SIN_DATO)
from sabado import armar_sabado

PUNTO = {'fosfágeno': '🟢', 'glucolítico': '🟡', 'aeróbico': '🔴'}
ANCHO = 66


def _cargado(dias):
    """Lo que la semana puso encima: cada WOD entero, más los levantamientos
    del bloque de fuerza — nunca la lista de accesorios.

    La diferencia importa para la línea "Evita". Contando el bloque completo se
    colaban Pendlay Row, Hip Thrust, Single-Leg RDL y Skin the Cat, que son
    trabajo de calidad dentro de un "N sets x calidad" y él no los avisa nunca.
    Sus cuatro líneas del mes 3 nombran barra y gimnasia dura, nada más.

    Antes esto VOLVÍA A LEER el texto que el propio generador acababa de
    escribir, con `leer()`, y recortaba la primera línea buscando '+' y la
    palabra "calidad". Ese camino ya produjo dos errores —la línea "Evita" que
    se leía de más y el encabezado "INTERVALOS" que entraba como movimiento—
    así que ahora cada parte declara lo suyo y acá solo se junta.

    Se devuelve CON repeticiones: lo que salió dos veces en la semana pesa más
    que lo que salió una, y eso es lo que ordena la lista.
    """
    out = []
    for d in dias:
        out += d['movs_bloque']
        out += d['movs']
    return out


def generar_semana(mes_del_ciclo, semana_del_mes, semilla=None,
                   sabados_del_mes=(), dias_previos=()):
    """Devuelve {'dias': [...], 'sabado': texto, 'usados_sabado': [...]}.

    `dias_previos` son los días ya generados de este mes. Sin eso la rotación
    de categoría se evalúa contra septiembre y sale igual las cuatro semanas.
    """
    rnd = random.Random(semilla)
    plan = g.proponer(semilla=semilla, previas=dias_previos)
    if not plan:
        return None
    # El lazo cerrado entre elegir movimientos y calcular el cap.
    #
    # `proponer` arma los cinco días cuidando que no haya dos dominios
    # seguidos iguales, pero el cap REAL lo calcula `escribir` después, a
    # partir del trabajo que quedó. Mientras el surtido era amplio los dos
    # coincidían casi siempre (3 de 800 días). Con los techos mensual y
    # semanal puestos, el surtido se achicó y el 13% de los días terminaba en
    # un dominio más corto del pedido — y de ahí salían 34 "dominios
    # consecutivos" por mes, que es una regla suya rota de verdad.
    #
    # Ahora la semana entera se descarta si un día no aterriza donde se pidió.
    # El reintento con otra semilla ya existía; solo faltaba usarlo para esto.
    dias, usados, dias_de_test = [], [], 0
    # Todo lo que la semana ya tiene repartido. El plan está cerrado desde
    # `proponer`, así que esto se conoce entero antes de escribir el lunes.
    de_la_semana_entera = {m for dd in plan for m in dd['movs']}
    for d in plan:
        # Se reintenta EL DÍA, no la semana. La deriva viene del sorteo de
        # repeticiones —con las mismas piezas, otra tirada llega a la duración
        # pedida— así que volver a sortear resuelve casi siempre. Descartar la
        # semana entera por un día desperdiciaba los reintentos: 8 de cada 20
        # meses se quedaban sin combinación incluso con 120 semillas.
        # Se resortean las repeticiones hasta que el día aterrice donde se
        # pidió, pero si no lo logra NO se descarta la semana: el día sale con
        # su dominio real y el marcador ▲ lo dice. Rechazar la semana entera
        # dejaba 28 de 40 meses sin combinación — una regla tan estricta que
        # impedía programar es peor que un día que se corrió de casillero.
        for _ in range(12):
            # `movs_escritos` puede traer más de lo que se planificó: un AMRAP
            # interrumpido agrega el movimiento que corta. Hay que quedarse con
            # esa lista y no con la del plan, o los techos, la separación y la
            # regla de días seguidos quedan mirando un día que no existe.
            txt_wod, fmt, cap, movs_escritos = escribir(
                rnd, d, evitar=de_la_semana_entera)
            dom_final = ('fosfágeno' if cap < 14 else
                         'glucolítico' if cap <= 19 else 'aeróbico')
            if dom_final == d['dom']:
                break
        skill_min = 20 if cap < 14 else (17 if cap <= 19 else 12)
        txt_bloque, levs, tipo_bloque = escribir_bloque(
            rnd, d['cat'], skill_min, semana_del_mes, mes_del_ciclo, usados,
            cap_del_wod=cap, dias_de_test=dias_de_test)
        if 'Buscar 1RM' in txt_bloque:
            dias_de_test += 1
        # `usados` guarda pares (levantamiento, tipo de bloque). El tipo está
        # porque él pidió permitir el mismo levantamiento dos veces en la
        # semana SI cambia el estímulo: Power Clean 5x5 el lunes y
        # "Power Clean + Split Jerk" el jueves sí, dos bloques normales no.
        usados += [(l, tipo_bloque) for l in levs]
        # El dominio se lee del cap FINAL, no del que se pidió al planificar.
        # Si el techo de volumen impidió llegar a los 20 minutos, el día es
        # glucolítico aunque se hubiera pedido aeróbico — y decir otra cosa
        # sería que el marcador mienta.
        dom_real = ('fosfágeno' if cap < 14 else
                    'glucolítico' if cap <= 19 else 'aeróbico')
        dias.append({**d, 'dom': dom_real, 'dom_pedido': d['dom'],
                     'movs': movs_escritos, 'movs_bloque': levs,
                     'cap': cap, 'skill': skill_min,
                     'bloque': txt_bloque, 'wod': txt_wod})

    # El sábado también respeta el techo mensual, contando los cinco días que
    # se acaban de armar: sin eso cruzaba el máximo justo al final de la semana.
    #
    # Va el WOD y NO los levantamientos del bloque, aunque ahora estén a mano.
    # Probé sumarlos y la auditoría saltó de 21 a 40 hallazgos en 90 meses. La
    # razón es que `TECHO_MENSUAL` se calibró contando SOLO los WODs de sus
    # planillas: los bloques viven en otra estructura y nunca entraron a ese
    # conteo. Meterlos acá los hace gastar un cupo que se midió sin ellos, y el
    # generador se queda corto por un motivo falso. Para contarlos habría que
    # recalibrar el techo con los bloques adentro, que es otro trabajo.
    de_la_semana = [{'cat': 'X', 'movs': d['movs']} for d in dias]
    # El sábado cierra la semana, así que el viernes es "ayer" para él: sin la
    # separación acá, un Power Clean del viernes volvía al día siguiente y el
    # techo mensual lo daba por bueno.
    sab = armar_sabado(rnd, sabados_del_mes=sabados_del_mes,
                       cargado_en_la_semana=_cargado(dias),
                       al_tope=lambda m: (g.al_tope(m, dias_previos, de_la_semana)
                                          or g.muy_pronto(m, dias_previos, de_la_semana)))
    if not sab:
        return None
    return {'dias': dias, 'sabado': sab[0], 'usados_sabado': sab[1]}


def generar_mes(mes_del_ciclo, semilla=None, por_semana=30, trabajo_maximo=400):
    """Las cuatro semanas, arrastrando los sábados para que no se repitan.

    CON VUELTA ATRÁS, y la razón importa. Antes esto reintentaba la misma
    semana con otra semilla y se rendía a las treinta. Al medirlo, los cinco
    meses de cada cuarenta que no generaban fallaban los cinco en la SEMANA 4,
    y las treinta veces en el mismo punto: el plan de días. No es mala suerte
    del sorteo — es que las tres semanas anteriores ya gastaron los cupos y a
    la cuarta no le queda dónde caer. Resortear la cuarta no puede arreglar
    algo que decidió la tercera.

    Así que cuando una semana se queda sin salida se rehace la ANTERIOR, con
    la semilla siguiente, y la que falló vuelve a empezar con su presupuesto
    entero. `trabajo_maximo` corta el total de semanas intentadas para que un
    mes imposible no se quede dando vueltas.
    """
    semanas, sabados, previos = [], [], []
    intento = [0] * 6              # presupuesto gastado por cada semana
    pila = []                      # estado con el que empezó cada semana hecha
    trabajo, n = 0, 1

    while n <= 4:
        estado_inicial = ([list(s) for s in sabados], list(previos))
        sem = None
        while intento[n] < por_semana and trabajo < trabajo_maximo:
            base = (None if semilla is None
                    else semilla * 10 + n + intento[n] * 977)
            intento[n] += 1
            trabajo += 1
            sem = generar_semana(mes_del_ciclo, n, semilla=base,
                                 sabados_del_mes=sabados, dias_previos=previos)
            if sem:
                break

        if not sem:
            if n == 1 or trabajo >= trabajo_maximo:
                return None
            # Atrás: la semana anterior se rehace desde donde quedó su
            # presupuesto, y esta vuelve a tener el suyo completo.
            intento[n] = 0
            n -= 1
            sabados, previos = pila.pop()
            semanas.pop()
            continue

        pila.append(estado_inicial)
        sabados.append(sem['usados_sabado'])
        previos += [{'dia': d['dia'], 'cat': d['cat'], 'movs': d['movs']}
                    for d in sem['dias']]
        # El sábado también gasta cupo del mes. Sin contarlo, el tope mentía:
        # el sábado 17 y el jueves ponían el mismo Bar Muscle-up y el
        # generador creía haberlo usado una sola vez.
        previos.append({'dia': 'Sábado', 'cat': 'PARTNER',
                        'movs': list(sem['usados_sabado'])})
        semanas.append(sem)
        n += 1
    return semanas


# --- Impresión -----------------------------------------------------------

LEYENDA = [
 '🟢 Corto <14\'   🟡 Medio 14-19\'   🔴 Largo 20\'+   ·   objetivo 30 / 50 / 20',
 '(Esc)  versión escalada — se elige por movimiento, no por alumno',
 '@%     porcentaje del 1RM de la fase del mes',
 'relay  uno trabaja, el otro descansa   ·   JUNTOS  los dos a la vez',
 '*      nota de coaching, no es trabajo extra',
]


def encabezado(mes, semana_del_mes):
    """El rótulo de la semana 4 depende del mes: no todos los meses testean.

    Decía "TEST 1RM" en los cuatro, y en el mes 3 no hay un solo 1RM.
    """
    fase, rango = FASES[mes]
    test = TEST_DEL_MES.get(mes, 'ninguno')
    escalera = PCT_POR_MES.get(mes, PCT_POR_MES[3])
    pct = (ROTULO_S4[test] if semana_del_mes == 4 and test != 'ninguno'
           else escalera[semana_del_mes])
    aviso = ('\n⚠ ' + AVISO_SIN_DATO) if mes in MESES_SIN_DATO else ''
    return (f'CROSSTRAIN EIM — Mes {mes} · {fase} {rango}\n'
            f'Semana {semana_del_mes} de 4 · {pct}{aviso}\n'
            + '=' * ANCHO)


def imprimir_semana(sem, mes, semana_del_mes, con_leyenda=True):
    print(encabezado(mes, semana_del_mes))
    for d in sem['dias']:
        aviso = ('   ▲ se pidió ' + d['dom_pedido']
                 if d.get('dom_pedido') and d['dom_pedido'] != d['dom'] else '')
        print()
        print(f"{d['dia'].upper()}  —  {d['cat']} {PUNTO[d['dom']]} "
              f"{d['cap']}'  |  Skill: {d['skill']}'{aviso}")
        print('-' * ANCHO)
        print(d['bloque'])
        print()
        print(d['wod'])
    print()
    print(f"SÁBADO  —  PARTNER  ·  35'")
    print('-' * ANCHO)
    print(sem['sabado'])
    if con_leyenda:
        print()
        print('-' * ANCHO)
        for linea in LEYENDA:
            print(linea)


def imprimir_mes(semanas, mes):
    for n, sem in enumerate(semanas, 1):
        if n > 1:
            print('\n')
        imprimir_semana(sem, mes, n, con_leyenda=(n == len(semanas)))


if __name__ == '__main__':
    import sys
    mes = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    semanas = generar_mes(mes, semilla=11)
    if semanas:
        imprimir_mes(semanas, mes)
    else:
        print('sin combinación')
