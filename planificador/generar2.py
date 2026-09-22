# -*- coding: utf-8 -*-
"""Propone una semana, componiendo el WOD como los compone Luis.

LA REGLA DE COMPOSICIÓN no se inventó: salió de medir sus 20 WODs de
septiembre. El WOD es peso corporal con UNO o DOS movimientos de la
categoría del día encima — no un WOD "de la categoría".

  STRENGTH     exactamente 1 de Fuerza. La barra nunca va con otra barra.
  GYMNASTICS   2 de Gimnasia
  METCON       1 de Cardio. Uno solo: no es un WOD de máquinas.
  ACCESSORY    1 de Musculación

El resto es Gimnasia, y a veces un Cardio de relleno — que es el "descanso
real de hombro" del que habla su regla 7.
"""
import random, openpyxl
from collections import Counter, defaultdict
from leer_wod import leer
from familias import familia_de
from prescribir import PESOS, DIST
from septiembre import MES

# --- Techo mensual por movimiento ---------------------------------------
#
# El generador no tenía ninguno, y se notaba: en un octubre de prueba puso
# "5 Bar Muscle-up / 10 C2B (Esc)" SEIS veces, idéntico las seis. Luis lo
# programa una o dos veces al mes. Siete movimientos se pasaban de su máximo
# observado; Row era el peor, 9 contra 3.
#
# La regla que sale de sus tres meses es clara y tiene sentido de coaching:
# cuanto más difícil el movimiento, menos veces al mes.
#
#     relleno        Run 9 · DU 6 · Air Squat 5 · Sit-up 4
#     gimnasia       T2B 7 · Box Jump Over 7 · WBS 6 · C2B 6 · Pull-up 4
#     alta destreza  Bar MU 2 · Wall Walk 2 · Pistol 1 · Strict Pull-up 1
#     barra          casi todo entre 1 y 3
#
# El techo es el máximo que él usó en un mes MÁS UNO. El +1 no es adorno: son
# tres meses de muestra, y tratar un máximo observado como una frontera dura
# convierte "no lo hizo" en "no se puede", que son cosas distintas.
import mes2 as _mes2, mes3 as _mes3

def _cuenta_mes(_M):
    c = Counter()
    for _s, _f, _fa, _jor, _sab in _M:
        for _d, _c, _cap, _sk, _t in _jor:
            for _m in leer(_t)['movimientos']: c[_m] += 1
        for _m in leer(_sab.split('Score:')[0])['movimientos']: c[_m] += 1
    return c

TECHO_MENSUAL = Counter()
for _c in (_cuenta_mes(_mes2.MES), _cuenta_mes(_mes3.MES), _cuenta_mes(MES)):
    for _m, _n in _c.items():
        TECHO_MENSUAL[_m] = max(TECHO_MENSUAL[_m], _n)
for _m in list(TECHO_MENSUAL):
    TECHO_MENSUAL[_m] += 1
TECHO_POR_DEFECTO = 2      # nunca visto en sus planillas: se usa con cuidado

# Y un techo SEMANAL, que es lo que impide que el cupo del mes se gaste en las
# primeras dos semanas. Sin él, la semana 4 se quedaba sin combinación 8 veces
# de cada 40 — el generador es voraz y no reserva para después.
#
# Él reparte: de los movimientos que suma 3 o más veces al mes, casi ninguno
# pasa de 3 en una misma semana, ni siquiera los que llega a poner 7 veces.
#
#     Toes-to-Bar    total 7   [3, 1, 2, 1]
#     Box Jump-Over  total 7   [1, 3, 2, 1]
#     Run            total 9   [1, 4, 1, 3]   ← el único que llega a 4
TECHO_SEMANAL = Counter()
for _M in (_mes2.MES, _mes3.MES, MES):
    for _s, _f, _fa, _jor, _sab in _M:
        _c = Counter()
        for _d, _ct, _cap, _sk, _t in _jor:
            for _m in leer(_t)['movimientos']: _c[_m] += 1
        for _m in leer(_sab.split('Score:')[0])['movimientos']: _c[_m] += 1
        for _m, _n in _c.items():
            TECHO_SEMANAL[_m] = max(TECHO_SEMANAL[_m], _n)
TECHO_SEMANAL_POR_DEFECTO = 1


def al_tope(mov, previas, de_esta_semana=()):
    """¿Este movimiento gastó su cupo del mes, o el de esta semana?

    `previas` son todos los días del mes ya armados (incluidos los sábados);
    `de_esta_semana`, los días de la semana en curso.
    """
    esta = sum(1 for d in de_esta_semana for m in d['movs'] if m == mov)
    # El mensual cuenta TAMBIÉN la semana en curso. Dejarla fuera —que fue mi
    # primera versión— hacía que la última semana pudiera cruzar el techo del
    # mes sin que nada lo viera.
    usado = sum(1 for d in previas for m in d['movs'] if m == mov) + esta
    if usado >= TECHO_MENSUAL.get(mov, TECHO_POR_DEFECTO):
        return True
    return esta >= TECHO_SEMANAL.get(mov, TECHO_SEMANAL_POR_DEFECTO)


wb = openpyxl.load_workbook('CSL-Fit_Catalogo_Completo.xlsx', data_only=True)
CATEG, CAD, TECNICO = {}, {}, set()
for r in wb['Movimientos'].iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    b = r[1] or r[0]
    CATEG[b] = r[5]
    CAD[b] = [c for c in (r[3], r[4]) if c]
def cadenas(m): return CAD.get(m, [])
def empujes(movs):
    """Cuántos movimientos cargan el hombro en empuje."""
    return sum(1 for m in movs if any('empuje' in c for c in cadenas(m)))

# El vocabulario sale de lo que PROGRAMÓ, no del catálogo entero: 400
# movimientos incluyen progresiones y accesorios que nunca van a WOD.
#
# Y sale de sus TRES meses, no solo de septiembre. Esto leía un mes y se
# notaba: 28 movimientos en vez de 47, y sobre todo, Run y Row como única
# distancia. Con los techos mensuales puestos, su cupo combinado (14) era
# exactamente igual a los días que necesitan trabajo largo (14) — cero
# holgura, y el generador se quedaba sin combinación 8 veces de cada 20.
# Bike, Ski, Shuttle Run y Farmer Carry ya estaban transcritos; nadie los
# estaba mirando.
historia, vocab = [], Counter()
for _fuente in (_mes2.MES, _mes3.MES, MES):
    for semana, f, fase, jornadas, sab in _fuente:
        for dia, cat, cap, skill, texto in jornadas:
            movs = leer(texto)['movimientos']
            historia.append({'semana': semana, 'dia': dia, 'cat': cat, 'movs': movs})
            vocab.update(movs)
POOL = list(vocab)
def de(categoria): return [m for m in POOL if CATEG.get(m) == categoria]

MAPA   = {'STRENGTH':'Fuerza', 'GYMNASTICS':'Gimnasia', 'METCON':'Cardio', 'ACCESSORY':'Musculación'}
CUANTOS= {'STRENGTH':1, 'GYMNASTICS':2, 'METCON':1, 'ACCESSORY':1}
DIAS   = ['Lunes','Martes','Miércoles','Jueves','Viernes']
DOM    = lambda c: 'fosfágeno' if c < 14 else ('glucolítico' if c <= 19 else 'aeróbico')
SKILL  = lambda c: 20 if c < 14 else (17 if c <= 19 else 12)
CAPS   = {'fosfágeno':[6,7,8,9,10,11], 'glucolítico':[14,15,16,17,18], 'aeróbico':[20,22,24]}

# Cuántos movimientos lleva un WOD según su duración. Medido sobre los 20 de
# septiembre: nunca hay 2 movimientos en un WOD de más de 12 minutos.
#   corto <14'   2-3      medio 14-19'  3-4      largo 20'+  4-5
CUANTOS_MOVS = {'fosfágeno': [2,2,3,3], 'glucolítico': [3,4,4,4], 'aeróbico': [4,4,5]}

def dias_bloqueados(cat, previas):
    """Los días donde esa categoría ya NO puede caer este mes.

    Dos correcciones a lo que había:

    1. Esto leía `historia`, que se carga una vez desde septiembre y no cambia
       nunca. Su septiembre ya tenía GYMNASTICS en lunes, miércoles, jueves y
       viernes, así que al generador solo le quedaba el martes — las cuatro
       semanas. METCON quedaba clavado en jueves y ACCESSORY en lunes. La
       regla que existe para que nadie diga "los martes son de gimnasia"
       estaba produciendo exactamente eso.

    2. El criterio era "nunca en un día ya usado", y eso es más estricto que
       lo que él programa: su septiembre pone ACCESSORY el viernes de S13 y
       otra vez el de S16. Lo que evita no es la repetición, es que se vuelva
       predecible. La regla medida es máximo 2 veces al mes en el mismo día,
       y nunca dos semanas seguidas.
    """
    # OJO: `previas` trae también los sábados, que consumen cupo mensual pero
    # NO son parte de la rotación de categorías. La semana se cuenta sobre los
    # días de lunes a viernes; mezclarlos corría el índice y la rotación se
    # evaluaba contra la semana equivocada.
    laborales = [d for d in previas if d['cat'] != 'PARTNER']
    porDia = defaultdict(list)
    for i, d in enumerate(laborales):
        if d['cat'] == cat:
            porDia[d['dia']].append(i // 5)          # semana del mes, 0-based
    semana_actual = len(laborales) // 5
    return {dia for dia, semanas in porDia.items()
            if len(semanas) >= 2 or semanas[-1] == semana_actual - 1}
def fam(m): return familia_de(m)
def familias_de(movs): return {familia_de(m) for m in movs if familia_de(m)}
def hace_cuanto(mov, previas=None):
    """Cuántos días atrás salió ese movimiento, contando el mes en curso."""
    fuente = previas if previas is not None else historia
    for i, d in enumerate(reversed(fuente)):
        if mov in d['movs']: return i
    return 999

def peso_tipico(m):
    ps = PESOS.get(m)
    if not ps: return 0
    h, _, u = max(set(ps), key=ps.count)
    return h if u == 'lb' else 0     # solo la barra se mide contra el cap


# --- Separación mínima entre repeticiones --------------------------------
#
# El techo mensual dice CUÁNTAS veces, no CADA CUÁNTO, y son cosas distintas:
# tres Bar Muscle-up en el mes pasan el techo aunque caigan martes, jueves y
# sábado de la misma semana. El alumno no cuenta al mes — cuenta los días que
# lleva con las manos rotas.
#
# Hueco entre dos apariciones, medido sobre sus tres meses (72 días):
#
#     grupo           mínimo  mediana  ≤2 días   n
#     barra pesada         4       11       0%    8
#     gimnasia dura       14       19       0%    2
#     resto                1        5      22%   87
#     relleno              1        4      38%   47
#
# Lo de la barra es una regla SUYA, no mía: ocho huecos en seis movimientos y
# ni uno bajo cuatro días. Deadlift 16, Squat Clean 13, Power Clean 11,
# Push Jerk 5-9-12, Front Squat 5, Hang Power Clean 4. Nunca la escribió en
# ninguna parte y la cumple sin excepción.
#
# La gimnasia dura NO está medida: dos huecos en total (Wall Walk 19,
# Push-up 14). El 4 de acá abajo es decisión de coaching, no un dato suyo, y
# por eso va en una constante aparte — para poder moverlo sin tocar el de la
# barra, que sí está respaldado.
SEPARACION_BARRA = 4      # medido
SEPARACION_DESTREZA = 4   # elegido

# "Alta destreza" no se decide a ojo. Son los gimnásticos que cumplen las DOS
# condiciones, y cada una viene de algo que ya existía:
#
#   · tienen línea (Esc) en la tabla de escalas — que es la definición que esa
#     tabla usa de sí misma: "los movimientos de alta destreza";
#   · y tienen techo mensual bajo, o sea, él los programa una o dos veces.
#
# Hace falta la intersección, no cualquiera de las dos sueltas:
#
#   solo el techo bajo   → entran Box Jump, Box Dip y Push-up, que no son
#                          difíciles, son raros en su planilla por otra razón
#                          (dos de ellos son escalas de otra cosa).
#   solo las escalas     → entran Toes-to-Bar, C2B, Pull-up y HSPU, que son su
#                          volumen. Ponerle 4 días de separación al T2B
#                          contradice su propia planilla: sus huecos medidos
#                          son 2-2-2-2-3-3-4-4-4-8-12.
from escalas import ESCALAS
ALTA_DESTREZA = {m for m in POOL
                 if CATEG.get(m) == 'Gimnasia' and m in ESCALAS
                 and TECHO_MENSUAL.get(m, TECHO_POR_DEFECTO) <= 3}

# El Burpee ya tenía separación propia, escrita a mano adentro de `proponer` y
# con otra convención de conteo. Dos mecanismos para lo mismo es lo que después
# se rompe sin que nadie lo vea, así que pasa a la tabla. Su hueco mínimo
# medido es 3, pero el 4 es el que ya estaba corriendo y el que él vio
# funcionando: se conserva.
SEPARACION_EXTRA = {'Burpee': 4}


def separacion_de(mov):
    """Días que tienen que pasar antes de que ese movimiento pueda volver."""
    if mov in SEPARACION_EXTRA:
        return SEPARACION_EXTRA[mov]
    # La barra se define por CATEGORÍA, no por kilos. Definirla por peso era
    # heredar un agujero: Back Squat, Clean and Jerk, Overhead Squat y Split
    # Jerk devuelven 0 lb porque son justo los cinco que todavía no tienen
    # carga cargada, y Power Snatch y Squat Snatch se quedaban abajo del corte
    # por 20 libras. Con el umbral en 115 el Clean and Jerk quedaba exento — y
    # sus huecos medidos son 11 y 14, de los más largos que tiene.
    #
    # Y al mirarlos todos, la regla es más fuerte de lo que yo había medido:
    # NINGÚN movimiento de barra de sus tres meses vuelve antes de 4 días.
    # Power Snatch 6-6-15, Clean and Jerk 11-14, Thruster 14, Squat Snatch 21.
    if CATEG.get(mov) == 'Fuerza':
        return SEPARACION_BARRA
    if mov in ALTA_DESTREZA:
        return SEPARACION_DESTREZA
    return 0


def muy_pronto(mov, previas, de_esta_semana=()):
    """¿Volvería antes de tiempo? El día de ayer cuenta como 1.

    La secuencia es cronológica y trae los sábados en su lugar, así que un
    Bar Muscle-up del sábado bloquea el lunes igual que uno del viernes.
    """
    minimo = separacion_de(mov)
    if not minimo:
        return False
    secuencia = list(previas) + list(de_esta_semana)
    for atras, d in enumerate(reversed(secuencia), start=1):
        if atras >= minimo:
            return False
        if mov in d['movs']:
            return True
    return False

# Lo que cuenta como "trabajo monostructural" para llenar un WOD medio o largo.
# NO es solo distancia: de sus 33 WODs medios/largos, 22 llevan Run o Row, y de
# los 11 restantes 7 resuelven con Double Under o una máquina. Exigir distancia
# en los 14 días del mes —que es lo que yo hacía— pedía más Run y Row de los
# que él programa, y con el techo mensual puesto el generador se quedaba sin
# combinación. Su tasa real de WODs medios/largos con algo monostructural es
# 29 de 33, el 88%.
MONOSTRUCTURAL = {'Run', 'Row', 'Bike', 'Ski', 'Double under', 'Single Under',
                  'Machine', 'Shuttle Run'}

# Para el día AERÓBICO no sirve cualquier distancia: tiene que poder crecer.
# El Shuttle Run lo programó una sola vez, "100m Shuttle Run" dentro de un
# EMOM de 30', así que el generador conoce un único valor. Cinco rondas de eso
# son 500 metros — no estiran el WOD a veinte minutos, y el día se quedaba en
# 13-16'. Los seis casos que revisé de días aeróbicos cortos tenían Shuttle Run.
# Califica el movimiento cuyo repertorio de distancias llega a 400m o más.
def _puede_crecer(m):
    from prescribir import DISTANCIAS
    opciones = set(DISTANCIAS.get(m, [])) | set(DIST.get(m, []))
    return bool(opciones) and max(opciones) >= 400

DISTANCIA_LARGA = {m for m in ('Run', 'Row', 'Bike', 'Ski', 'Shuttle Run',
                               'Farmer Carry', 'Machine') if _puede_crecer(m)}


def arma_wod(rnd, categoria, prohibidos, cuantos_total, cap=None,
             exigir_distancia=False, dominio=None):
    """Un movimiento de la categoría del día, el resto peso corporal."""
    elegidos, cuenta = [], Counter()
    familias_puestas = set()
    def cabe(m):
        if m in prohibidos or m in elegidos: return False
        # La barra pesada solo va en WODs cortos. En septiembre los cinco WODs
        # con 135 lb o más tienen cap de 8 o 9 minutos; el único de 16' con
        # barra usa 115. Meter 155 lb en un AMRAP de 17' es otra cosa.
        if cap is not None and cap >= 12 and peso_tipico(m) >= 135: return False
        # Una sola de cada familia por WOD. No es invento: en los 24 WODs de
        # septiembre no hay un solo caso de dos movimientos de la misma
        # familia juntos. Pull-up y C2B en el mismo WOD es redundante.
        f = fam(m)
        if f and f in familias_puestas: return False
        cads = cadenas(m)
        return not any(cuenta[c] >= 2 for c in cads)
    def poner(m):
        elegidos.append(m)
        if fam(m): familias_puestas.add(fam(m))
        for c in cadenas(m): cuenta[c] += 1

    propios = [m for m in de(MAPA[categoria]) if cabe(m)]
    rnd.shuffle(propios)
    for m in propios[:CUANTOS[categoria]]:
        if cabe(m): poner(m)
    if len(elegidos) < CUANTOS[categoria]: return None

    # Los WODs medios y largos llegan a su duración con trabajo monostructural,
    # no con más rondas: sin esto el generador subía a 8 rondas y salían 40 Bar
    # Muscle-up. Pero el monostructural no tiene por qué ser distancia — él usa
    # Double Under o máquina en 7 de los 11 casos donde no hay Run ni Row.
    #
    # Y la distancia se RESERVA para los días aeróbicos. Un Double Under no
    # llena veinte minutos: cuando el cupo de Run y Row se gastaba en los días
    # glucolíticos, el día largo caía a DU, el cap salía corto y el día
    # terminaba siendo medio. Eso se veía como 14% de días en un dominio
    # distinto al pedido, y de ahí 34 "dominios consecutivos" por mes.
    # La condición y los candidatos tienen que mirar el MISMO conjunto. Tenerlos
    # distintos —probar contra MONOSTRUCTURAL y elegir de DISTANCIA_LARGA— hacía
    # que un Double Under entrado como relleno diera el requisito por cumplido,
    # y el día aeróbico se quedaba sin nada que lo estirara. El DU salía en 11
    # de los 17 días aeróbicos que terminaban cortos.
    acepta = DISTANCIA_LARGA if dominio == 'aeróbico' else MONOSTRUCTURAL
    if exigir_distancia and not any(m in acepta for m in elegidos):
        # La distancia se RESERVA para el día aeróbico, que es el que la
        # necesita para llegar a los 20 minutos. En glucolítico vale también el
        # Double Under, que es lo que él hace en 1 de cada 3 de esos días.
        #
        # Probé exigir distancia de verdad en los catorce días medios y largos:
        # peor por partida doble. Contradice su propio 67%, y deja al generador
        # tan apretado que un mes tarda minutos en salir.
        candidatos = [m for m in POOL if m in acepta and cabe(m)]
        rnd.shuffle(candidatos)
        candidatos.sort(key=lambda m: m not in DIST)
        if not candidatos: return None
        poner(candidatos[0])

    # Relleno: gimnasia, y un cardio de vez en cuando
    relleno = de('Gimnasia') + (de('Cardio') if rnd.random() < 0.55 else [])
    rnd.shuffle(relleno)
    for m in relleno:
        if len(elegidos) >= cuantos_total: break
        if cabe(m): poner(m)
    return elegidos if len(elegidos) >= cuantos_total else None

# Cuántos días de cada dominio lleva la semana. NO es fijo, y tenerlo fijo era
# un problema que no se veía hasta mirar el mes entero: con 3 glucolíticos
# clavados y la regla de "no dos iguales seguidos", los únicos órdenes posibles
# son 🟡x🟡y🟡 con {x,y} = {🟢,🔴}. Dos formas. En 160 semanas generadas
# salieron exactamente esas dos el 98% de las veces — el mes se leía a máquina.
#
# Sus cuatro semanas de septiembre son 3-1-1, 2-2-1, 3-2-0 y 3-2-0: la
# composición cambia todas las semanas. Estas cuatro suman 6-10-4 en el mes,
# que es el 30/50/20 que dice la leyenda de su planilla del mes 2.
COMPOSICIONES = [
 ['fosfágeno', 'glucolítico', 'glucolítico', 'glucolítico', 'aeróbico'],
 ['fosfágeno', 'fosfágeno', 'glucolítico', 'glucolítico', 'aeróbico'],
 ['fosfágeno', 'fosfágeno', 'glucolítico', 'glucolítico', 'aeróbico'],
 ['fosfágeno', 'glucolítico', 'glucolítico', 'glucolítico', 'aeróbico'],
]


def proponer(intentos=6000, semilla=None, previas=None, composicion=None):
    """`previas` son los días ya generados de ESTE mes, en orden.

    Sin ellos cada semana se arma como si fuera la primera y como si el día
    anterior fuera siempre el último viernes de septiembre.
    """
    previas = list(previas or [])
    if composicion is None:
        laborales = sum(1 for d in previas if d['cat'] != 'PARTNER')
        composicion = COMPOSICIONES[(laborales // 5) % len(COMPOSICIONES)]
    rnd = random.Random(semilla)
    for _ in range(intentos):
        cats = ['STRENGTH','STRENGTH','GYMNASTICS','METCON','ACCESSORY']
        rnd.shuffle(cats)
        plan = dict(zip(DIAS, cats))
        # Los dos días de fuerza no van pegados. Él lo pidió con estas
        # palabras — "se puede pero ideal que no pase tan seguido dos días que
        # tengan mucho peso"— y su planilla lo respalda donde la estructura es
        # comparable: en el mes 3 y septiembre, que llevan DOS días de fuerza
        # como esto, los huecos son 2-3-3-1-2-2-3-2. Uno pegado de ocho, y ese
        # uno es una semana 4.
        #
        # El mes 2 tiene 4 de 7 pegados, pero ahí lleva tres y cuatro días de
        # fuerza por semana —HALTEROFILIA y FUERZA eran categorías separadas—
        # y con cuatro días en cinco no existe forma de separarlos. No es un
        # contraejemplo, es otra estructura.
        fuerza = [i for i, c in enumerate(cats) if c == 'STRENGTH']
        if fuerza[1] - fuerza[0] < 2: continue
        if any(plan[d] == c and d in dias_bloqueados(c, previas)
               for c in ('GYMNASTICS','METCON','ACCESSORY') for d in DIAS): continue

        doms = list(composicion)
        rnd.shuffle(doms)
        if any(doms[i] == doms[i+1] for i in range(4)): continue

        semana, ok = [], True
        # El "ayer" del lunes es el último día generado de este mes; solo la
        # primera semana del mes se apoya en septiembre.
        anterior = previas[-1] if previas else (historia[-1] if historia else None)
        ayer_fams = familias_de(anterior['movs']) if anterior else set()
        wods_de_empuje = 0
        box = 0
        for i, dia in enumerate(DIAS):
            cap = rnd.choice(CAPS[doms[i]])
            # Prohibido: mismo movimiento en la semana, o misma FAMILIA ayer.
            # Pull-up el martes y C2B el miércoles es repetir, aunque sean
            # bases distintas.
            prohibidos = {m for m in POOL if fam(m) in ayer_fams}
            # Y lo que ya gastó su cupo del mes. `previas` incluye los sábados,
            # que también consumen: el sábado 17 y el WOD del jueves ponían el
            # mismo Bar Muscle-up sin que nada lo contara.
            prohibidos |= {m for m in POOL if al_tope(m, previas, semana)}
            # Y lo que volvería demasiado pronto. El techo mensual limita
            # cuántas veces; esto, cada cuánto.
            prohibidos |= {m for m in POOL if muy_pronto(m, previas, semana)}
            if box >= 2: prohibidos |= {m for m in POOL if 'Box Jump' in m}
            cuantos = rnd.choice(CUANTOS_MOVS[doms[i]])
            movs = arma_wod(rnd, plan[dia], prohibidos, cuantos, cap=cap,
                            exigir_distancia=(doms[i] != 'fosfágeno'),
                            dominio=doms[i])
            if not movs: ok = False; break
            # Máximo un WOD empuje-dominante por semana. En septiembre hubo
            # dos en todo el mes —S13 jueves y S16 viernes— y Luis lo confirmó:
            # "un WOD así una vez al mes tampoco está mal, pero que no sea
            # mucho al mes". Dos por mes es una por cada dos semanas.
            if empujes(movs) >= 2:
                if wods_de_empuje >= 1: ok = False; break
                wods_de_empuje += 1
            box += sum(1 for m in movs if 'Box Jump' in m)
            semana.append({'dia':dia,'cat':plan[dia],'cap':cap,'dom':doms[i],
                           'skill':SKILL(cap),'movs':movs})
            ayer_fams = familias_de(movs)
        if ok: return semana
    return None

if __name__ == '__main__':
    p = proponer(semilla=11)
    if not p: print('Sin combinación que pase todas las reglas.')
    else:
        print("PROPUESTA — Semana 17 · Mes 5 · Base @65-75%\n")
        for d in p:
            pt = {'fosfágeno':'🟢','glucolítico':'🟡','aeróbico':'🔴'}[d['dom']]
            print(f"  {d['dia']:<11} {d['cat']:<11} {pt} {d['cap']}'  Skill {d['skill']}'")
            for m in d['movs']:
                print(f"       · {m:<24} {CATEG.get(m,'?')}")
            print()
