# -*- coding: utf-8 -*-
"""Categoría de entrenamiento, según el criterio real de CrossTrain EIM.

No es la taxonomía de un manual: se dedujo leyendo los 134 movimientos que
Luis ya había clasificado a mano. Las diferencias con el manual importan.

  Cardio       máquina o locomoción cíclica. Nada más.
  Gimnasia     PESO CORPORAL, con o sin destreza. Incluye el accesorio
               corporal (Copenhagen, Pallof, Box Step-up, Back Extension) y
               los movimientos lastrados que siguen siendo del propio cuerpo
               (Weighted Pull-up, Overhead Lunge).
  Fuerza       BARRA A REPS BAJAS: los levantamientos y sus accesorios de
               rack y banco (Good Morning, Bulgarian, Glute-Ham, Reverse Hyper).
  Musculación  CARGA DE ACONDICIONAMIENTO: mancuerna, kettlebell, med ball,
               sled, carries con implemento, y los complejos con nombre.
               También Thruster y Wall Ball — que son barra, pero de ciclo
               alto. Es el bloque ACCESSORY de la semana.

Lo que separa Fuerza de Musculación NO es el implemento: es la intención.
Fuerza máxima contra trabajo cargado repetido.
"""
import re, unicodedata

def norm(t):
    t = unicodedata.normalize('NFD', str(t).lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]', ' ', t)).strip()

CARDIO = [r'\brun\b', r'\brunning\b', r'\bshuttle\b', r'^row', r'\browing\b', r'^bike',
  r'\bairbike\b', r'\bassault\b', r'^ski\b', r'\bski erg\b', r'\berg\b', r'\bunder(s)?\b', r'\bjump rope\b',
  r'\bswim', r'\bcal (bike|row|machine|ski|erg)\b']

# Implementos que marcan Musculación
MUSCULACION = [r'\bdb\b', r'\bdumbbell\b', r'\bkb\b', r'\bkettlebell\b', r'\bmedicine ball\b',
  r'\bmed ball\b', r'\bsled\b', r'\bwall ball\b', r'\bwbs\b', r'\bthruster\b',
  r'\bdevil press\b', r'\bcomplex\b', r'\bbear complex\b', r'\bcurtis\b', r'\bman maker\b',
  r'\bgoblet\b', r'\bturkish\b', r'\bsuitcase\b', r'\bovercarry\b', r'\bovhd carry\b',
  r'\bovercabeza\b', r'\bfarmers carry\b', r'\boverhead carry\b', r'\bswing\b',
  r'\bcurl\b', r'\b(lateral|front|rear|calf) raise\b', r'\bfly\b', r'\bflye\b', r'\bskull crusher\b',
  r'\bface pull\b', r'\bpull apart\b', r'\bpull through\b', r'\bbanded\b', r'\bband\b', r'\bcable\b', r'\bmachine\b', r'\bpolea\b', r'\bshrug\b', r'\brear delt\b', r'\bhammer\b',
  r'\barnold\b', r'\blateral\b', r'\bpulldown\b', r'\btricep', r'\bbicep']

# Barra y accesorios de fuerza
FUERZA = [r'\bsquat\b', r'\bdeadlift\b', r'\bclean\b', r'\bsnatch\b', r'\bjerk\b',
  r'\bpress\b', r'\bbench\b', r'\bbarbell\b', r'\bpendlay\b', r'\bbent over\b',
  r'\bgood morning\b', r'\bbulgarian\b', r'\bglute ham\b', r'\breverse hyper\b',
  r'\bromanian\b', r'\brdl\b', r'\bstiff leg', r'\bsumo\b', r'\bhigh pull\b',
  r'\bclean pull\b', r'\bsnatch pull\b', r'\bbalance\b', r'\bohs\b', r'\boverhead squat\b',
  r'\bfloor press\b', r'\bhip thrust\b', r'\bone arm dumbbell row\b']

CUERPO = [r'\bair squat\b', r'\bpistol\b', r'\bpallof\b', r'\bpress to handstand\b',
  r'\bhandstand\b', r'\bhspu\b', r'\bpike push\b', r'\bpush up\b', r'\bpull up\b',
  r'\bmuscle up\b', r'\bring (dip|row|support)\b', r'\bbox (dip|jump|step)\b',
  r'\btoes to\b', r'\bknees to\b', r'\bl sit\b', r'\bhollow\b', r'\barch\b',
  r'\bskin the cat\b', r'\bgerman hang\b', r'\bburpee\b', r'\bsit up\b', r'\bv up\b',
  r'\bplank\b', r'\bcrawl\b', r'\bwall walk\b', r'\brope climb\b', r'\bback extension\b',
  r'\bhip extension\b', r'\bcopenhagen\b', r'\bghd\b', r'\bscapular\b', r'\bdead hang\b',
  r'\bactive hang\b', r'\bkip\b', r'\bbroad jump\b']

REMO_CARGADO = r'\b(db|dumbbell|chest supported|seal|one arm|single arm|t bar|cable|machine)\b.*\brow\b'

def categoria_de(nombre):
    n = norm(nombre)
    if any(re.search(p, n) for p in CARDIO): return 'Cardio'
    # El cuerpo manda: Air Squat es squat, pero es Gimnasia.
    if any(re.search(p, n) for p in CUERPO): return 'Gimnasia'
    if re.search(REMO_CARGADO, n): return 'Musculación'
    # El row de tracción no es cardio: se distingue por llevar implemento delante
    if re.search(r'\b(db|dumbbell|barbell|bent|pendlay|ring|inverted|seal|chest supported|one arm)\b.*\brow\b', n):
        pass
    if any(re.search(p, n) for p in MUSCULACION): return 'Musculación'
    if any(re.search(p, n) for p in FUERZA): return 'Fuerza'
    return 'Gimnasia'   # por descarte: si no es máquina, implemento ni barra, es el cuerpo
