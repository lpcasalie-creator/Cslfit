# -*- coding: utf-8 -*-
"""Familias de movimiento: qué cuenta como "el mismo" de un día al otro.

POR QUÉ NO ALCANZA CON EL MOVIMIENTO BASE

El movimiento base identifica el ejercicio exacto: Butterfly Pull-up y Kipping
Pull-up son los dos "Pull-up". Pero Chest-to-Bar es SU PROPIO base —y tiene que
serlo, porque en el bloque de skill la diferencia es justamente lo que se
entrena— y aun así poner Pull-up el martes y C2B el miércoles es repetir.

La familia agrupa por demanda: mismo patrón, mismos músculos, misma fatiga
acumulada al día siguiente. Es lo que mira la regla de días consecutivos.
El base sigue mandando en el skill.
"""
import re, unicodedata

def norm(t):
    t = unicodedata.normalize('NFD', str(t).lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9]', ' ', t)).strip()

# Orden: de lo más específico a lo más general.
# EL ORDEN MANDA: la primera que calza gana, así que va de lo más específico a
# lo más general. Devil Press tiene que mirarse antes que "press", y el remo de
# máquina antes que el remo de tracción.
FAMILIAS = [
 # --- Combinados que llevan el nombre de otra cosa ----------------------
 ('Burpee', [r'\bburpee\b', r'\bdevil press\b', r'\bman maker\b']),
 ('Sentadilla + empuje', [r'\bthruster\b', r'\bwall ball\b', r'\bwbs\b', r'\bmedicine ball clean\b']),

 # --- Monostructural: antes que los patrones de tracción ---------------
 ('Remo máquina', [r'^row\b', r'\browing\b', r'\bcal row\b', r'\brow erg\b', r'^rowing\b']),
 ('Bici', [r'\bbike\b', r'\bairbike\b', r'\bassault\b']),
 ('Ski', [r'\bski\b(?!n)']),
 ('Carrera', [r'\brun\b', r'\brunning\b', r'\bshuttle\b', r'\bhigh knees\b', r'\bsprint\b']),
 ('Cuerda de saltar', [r'\bunder(s)?\b', r'\bjump rope\b']),
 ('Trepa de cuerda', [r'\brope climb\b']),
 ('Carry', [r'\bcarry\b', r'\bfarmer', r'\bsuitcase\b', r'\bsled\b', r'\byoke\b']),
 ('Desplazamiento en suelo', [r'\bcrawl\b', r'\bmountain climber\b']),
 ('Natación', [r'\bswim']),

 # --- Empuje: la mancuerna antes que la barra --------------------------
 ('Vertical invertido', [r'\bhspu\b', r'\bhandstand\b', r'\bpike push\b', r'\bwall walk\b',
   r'\bpress to handstand\b']),
 ('Fondos', [r'\bdip\b']),
 ('Flexiones', [r'\bpush up\b', r'\bpushup\b', r'\barcher push\b']),
 ('Press overhead mancuerna', [r'\b(db|dumbbell|kb|kettlebell)\b.*\b(press|jerk)\b', r'\barnold\b',
   r'\bbottoms up press\b']),
 ('Press horizontal', [r'\bbench\b', r'\bfloor press\b', r'\bfly\b', r'\bpec deck\b',
   r'\bskull crusher\b', r'\btricep']),
 ('Press overhead barra', [r'\bjerk\b', r'\bpush press\b', r'\bstrict press\b',
   r'\bshoulder press\b', r'\bpress\b(?!.*(pallof|leg))']),

 # --- Tracción ----------------------------------------------------------
 ('Tracción vertical', [r'\bpull up\b', r'\bpullup\b', r'\bchin up\b', r'\bchest to bar\b',
   r'\bc2b\b', r'\bmuscle up\b', r'\bhip to bar\b', r'\bkip swing\b', r'\bpulldown\b',
   r'\bdead hang\b', r'\bactive hang\b', r'\bscapular pull\b']),
 ('Remo horizontal', [r'\brow\b', r'\bseal row\b', r'\bface pull\b', r'\bpull apart\b']),

 # --- Pierna ------------------------------------------------------------
 ('Sentadilla + empuje', [r'\bthruster\b']),
 ('Sentadilla con barra', [r'\b(back|front|overhead) squat\b', r'\bohs\b', r'\bgoblet\b']),
 ('Sentadilla libre', [r'\bair squat\b', r'\bwall sit\b']),
 ('Sentadilla unilateral', [r'\bpistol\b', r'\bbulgarian\b', r'\bcossack\b', r'\bsplit squat\b',
   r'\bstep up\b', r'\bstep down\b']),
 ('Estocada', [r'\blunge\b']),
 ('Salto a cajón', [r'\bbox jump\b']),
 ('Salto', [r'\bbroad jump\b', r'\bvertical jump\b']),

 # --- Bisagra -----------------------------------------------------------
 ('Clean', [r'\bclean\b']),
 ('Snatch', [r'\bsnatch\b']),
 ('Peso muerto', [r'\bdeadlift\b', r'\brdl\b', r'\bromanian\b', r'\bstiff leg',
   r'\bgood morning\b', r'\bback extension\b', r'\bhip extension\b', r'\bglute ham\b',
   r'\breverse hyper\b']),
 ('Swing', [r'\bswing\b']),
 ('Puente de cadera', [r'\bhip thrust\b', r'\bglute bridge\b', r'\bfrog pump\b',
   r'\bglute kickback\b']),

 # --- Core --------------------------------------------------------------
 ('Core colgante', [r'\btoes to\b', r'\bt2b\b', r'\bknees to\b', r'\bknee raise\b',
   r'\bleg raise\b', r'\bl sit\b', r'\bskin the cat\b', r'\bgerman hang\b']),
 ('Core en suelo', [r'\bsit up\b', r'\bv up\b', r'\bghd\b', r'\bhollow\b', r'\barch\b',
   r'\bplank\b', r'\bab wheel\b', r'\bdead bug\b', r'\bbird dog\b', r'\bpallof\b',
   r'\brussian twist\b', r'\bcopenhagen\b']),

 # --- Aislamiento -------------------------------------------------------
 ('Aislamiento brazo', [r'\bcurl\b', r'\bhammer\b']),
 ('Aislamiento hombro', [r'\braise\b', r'\brear delt\b', r'\bshrug\b', r'\by t w\b',
   r'\bexternal rotation\b']),
]

def familia_de(nombre):
    n = norm(nombre)
    for fam, patrones in FAMILIAS:
        if any(re.search(p, n) for p in patrones): return fam
    return ''
