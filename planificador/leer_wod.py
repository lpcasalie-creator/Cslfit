# -*- coding: utf-8 -*-
"""Leer un WOD escrito como los escribe Luis. Prueba de concepto, no toca la app."""
import openpyxl, re, unicodedata

wb = openpyxl.load_workbook('CSL-Fit_Catalogo_Base.xlsx', data_only=True)
CAT = [str(r[0]) for r in wb['Movimientos'].iter_rows(min_row=2, values_only=True) if r[0]]

def norm(t):
    t = unicodedata.normalize('NFD', str(t).lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]', ' ', t)).strip()

# La distancia va adelante en su forma de escribir ("400m Run") y también hay
# entradas del catálogo así. Se saca de los dos lados para que calcen.
DISTANCIA = re.compile(r'^\d+\s*(m|km|cal|mts?)\b\s*')
def sin_distancia(t):
    return DISTANCIA.sub('', t).strip()

# Su taquigrafía: no está en el catálogo y sin esto no se lee casi nada.
ALIAS = {
 'wbs': 'Wall Ball', 'wall ball shot': 'Wall Ball', 'wall balls': 'Wall Ball',
 't2b': 'Toes-to-Bar', 'toes to bar': 'Toes-to-Bar',
 'du': 'Double under', 'su': 'Single Under',
 'c2b': 'Chest-to-Bar Pull-up', 'chest to bar': 'Chest-to-Bar Pull-up',
 'bar mu': 'Bar Muscle-up', 'ring mu': 'Ring Muscle-up', 'mu': 'Bar Muscle-up',
 'hspu': 'HSPU', 'hs': 'Handstand Hold',
 'hpc': 'Hang Power Clean', 'ohs': 'Overhead Squat',
 'kb swing': 'KB swing', 'fr lunge': 'Front Rack Lunge',
 'pistol': 'Pistol', 'run': 'Run', 'row': 'Row', 'bike': 'Bike',
 'c j': 'Clean and Jerk', 'clean jerk': 'Clean and Jerk',
 'wall walk': 'Wall Walk', 'db snatch': 'DB Snatch',
 # De los meses 2 y 3, que el catálogo no tenía:
 'cal machine': 'Machine', 'machine': 'Machine',
 'db lunge': 'DB Lunge', 'db fr lunge': 'DB Lunge', 'fr lunge': 'Front Rack Lunge',
 'bar facing burpee': 'Burpee over Bar', 'burpee over bar': 'Burpee over Bar',
 'shuttle run': 'Shuttle Run', 'bear crawl': 'Bear Crawl',
 'skin the cat': 'Skin the Cat', 'hang power snatch': 'Hang Power Snatch',
 'split jerk': 'Split Jerk', 'clean jerk': 'Clean and Jerk',
 'power clean jerk': 'Clean and Jerk', 'hpc': 'Hang Power Clean',
 'ring row': 'Ring Row', 'box dip': 'Box Dip', 'pike push up': 'Pike Push-up',
 'v up': 'V-Up', 'hollow rock': 'Hollow Rock', 'l sit': 'L-Sit',
 'rope climb': 'Rope Climb', 'turkish get up': 'Turkish Get-Up',
}

# Su planilla mezcla singular y plural — "Thrusters (115/75)", "15 Air Squats" —
# y sin esto el lector saltaba esas líneas enteras. Se prueba la clave tal cual
# y, si no calza, sin la "s" final.
def _sin_plural(t):
    return re.sub(r'\b(\w{3,})s\b', r'\1', t)

def _clave(t):
    return sin_distancia(norm(t))

# Patrones con límite de palabra, del más largo al más corto. Sin el límite,
# "run" calzaba dentro de otras palabras y "mu" dentro de cualquier cosa.
_pares = [(_clave(k), v) for k, v in ALIAS.items()] + [(_clave(c), c) for c in CAT]
_pares = [(k, v) for k, v in _pares if k]

# Varias entradas comparten clave ("200m Run", "400m Run" -> "run"). Gana el
# nombre más corto, que es el más cercano al movimiento base. Los alias ganan
# siempre, porque son la forma en que Luis los escribe.
_canonico = {}
for k, v in _pares:
    if k not in _canonico or len(v) < len(_canonico[k]):
        _canonico[k] = v
for k, v in ALIAS.items():
    _canonico[_clave(k)] = v

INDICE = [(re.compile(r'\b' + re.escape(k) + r'\b'), v)
          for k, v in sorted(_canonico.items(), key=lambda x: -len(x[0]))]

# El orden manda: gana el primero que calza. Los formatos nuevos van ARRIBA de
# 'for time' porque lo llevan adentro del encabezado — "INTERVALOS — 3 sets for
# time" se leía como FOR TIME a secas, y "ESCALERA DE CARGA" como ESCALERA.
FORMATOS = [
 (r'\bescalera de carga\b', 'ESCALERA-CARGA'),
 (r'\bintervalos\b', 'INTERVALOS'),
 (r'\bamrap\b.*\binterrumpido\b', 'AMRAP-INTERRUMPIDO'),
 (r'\bamrap\b.*\bescalera\b', 'AMRAP-ESCALERA'),
 (r'\bescalera\b', 'ESCALERA'),
 (r'\bfor time\b', 'FOR TIME'), (r'\bamrap\b', 'AMRAP'), (r'\bemom\b', 'EMOM'),
 (r'\bchipper\b', 'CHIPPER'), (r'\btabata\b', 'TABATA'),
 (r'\b\d+\s*rounds?\b', 'ROUNDS'),
]

# Palabras que nunca son un movimiento aunque calcen con algo del catálogo.
#
# 'intervalos' está en el catálogo como entrada sin categoría, así que el
# encabezado "INTERVALOS — 3 sets for time" metía un movimiento fantasma
# llamado Intervalos en cada día de ese formato. Dos días seguidos de
# intervalos y el validador marcaba "movimiento en días seguidos" por algo que
# no existe: 30 fantasmas en 15 meses, y siete hallazgos falsos.
RUIDO = {'rest', 'descanso', 'esc', 'rx', 'cap', 'rounds', 'round',
         'intervalos', 'escalera'}

def leer(texto):
    t = norm(texto)
    formato = next((f for p, f in FORMATOS if re.search(p, t)), None)
    cap = None
    m = re.search(r'cap\s*(\d+)', t) or re.search(r'(?:amrap|emom)\s*(\d+)', t)
    if m: cap = int(m.group(1))

    movs, escalas = [], []
    for linea in texto.split('\n'):
        # El corte va sobre la línea CRUDA: normalizar primero borraba la barra.
        partes = re.split(r'\s*/\s*|\s+o\s+', linea)
        for idx, parte in enumerate(partes):
            # Lo que viene después de la barra y dice (Esc) es la ESCALA del
            # movimiento anterior, no un movimiento aparte. Contarlos como dos
            # hacía saltar la regla de cadena muscular con un falso positivo:
            # HSPU + Pike Push-up son el mismo ejercicio en dos niveles.
            es_escala = idx > 0 and re.search(r'\(\s*esc', parte, re.I)
            p = sin_distancia(norm(parte))
            p = ' '.join(w for w in p.split() if w not in RUIDO)
            if not p: continue
            encontrado = next((n for pa, n in INDICE if pa.search(p)), None)
            if encontrado is None:
                sp = _sin_plural(p)
                if sp != p:
                    encontrado = next((n for pa, n in INDICE if pa.search(sp)), None)
            if encontrado:
                destino = escalas if es_escala else movs
                if encontrado not in movs and encontrado not in escalas:
                    destino.append(encontrado)
    return {'formato': formato, 'cap': cap, 'movimientos': movs, 'escalas': escalas}
