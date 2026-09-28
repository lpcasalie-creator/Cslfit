# -*- coding: utf-8 -*-
"""CrossTrain EIM — Mes 3 (Semanas 9-12), agosto 2026. Transcrito de su planilla.

Estructura declarada en el encabezado:
    2 STRENGTH · 1 GYMNASTICS · 1 METCON · 1 ACCESSORY por semana

Mismo formato que septiembre.MES:
    (semana, fechas, fase, [(dia, cat, cap, skill, texto)], texto_sabado)
"""

MES = [
 (9, '4–9 Agosto', 'Mes 3', [
  ('Lunes', 'STRENGTH', 7, 20,
   "FOR TIME (Cap 7')\n3 Rounds:\n· 6 Squat Snatch (95/65)\n"
   "· 4 Wall Walk (Rx) / 8 Bear Crawl 10m (Esc)"),
  ('Martes', 'GYMNASTICS', 22, 12,
   "3 Rounds (Cap 22')\n· 15 Strict Pull-Up / Ring Row x2 (Esc)\n· 15 T2B\n"
   "· 20 Box Jump Over 24\"\n· 200m Run"),
  ('Miércoles', 'STRENGTH', 10, 20,
   "\"FRAN\" MOD (Cap 10')\n21-15-9:\n· Thrusters (115/75)\n· Pull-Up"),
  ('Jueves', 'METCON', 16, 17,
   "EMOM 16'\n1: 10 Power Snatch (75/55)\n2: 12 WBS (20/14)\n3: 10 T2B\n4: Rest"),
  ('Viernes', 'ACCESSORY', 8, 20,
   "AMRAP 8'\n· 12 DB Lunge (50/35)\n· 10 Ring Dip / Box Dip (Esc)\n· 15 Sit-Up"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n· 400m Run JUNTOS\n"
  "· 10 Power Clean (95/65) @~55% — relay\n· 10 KB Swing (24/16) — relay\n"
  "· 10 T2B — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas | "
  "Evita: Snatch · Wall Walk · WBS · Push Jerk"),

 (10, '11–16 Agosto', 'Mes 3', [
  ('Lunes', 'STRENGTH', 15, 17,
   "AMRAP 15'\n· 10 Deadlift (225/155)\n· 15 Box Jump Over 24\"\n· 20 Air Squat"),
  ('Martes', 'METCON', 8, 20,
   "FOR TIME (Cap 8')\n10-8-6-4-2:\n· Squat Clean (135/95)\n"
   "· C2B (Rx) / Pull-Up x2 (Esc)"),
  ('Miércoles', 'ACCESSORY', 25, 12,
   "CHIPPER (Cap 25')\n· 40 WBS (20/14)\n· 30 T2B\n"
   "· 20 HSPU / 40 Pike Push-Up (Esc)\n· 15 Ring Dip / 20 Box Dip (Esc)\n· 400m Run"),
  ('Jueves', 'STRENGTH', 7, 20,
   "FOR TIME (Cap 7')\n3 Rounds:\n· 7 Power Snatch (95/65)\n· 7 Burpee over Bar"),
  ('Viernes', 'GYMNASTICS', 18, 17,
   "EMOM 18'\n1: 14 FR Lunge (115/75)\n2: 15 Box Jump Over 24\"\n3: 10 Burpee\n"
   "4: 40 DU\n5: Rest"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n· 50 DU JUNTOS (25 c/u)\n"
  "· 8 Hang Power Snatch (75/55) @~55% — relay\n· 15 WBS (20/14) — relay\n"
  "· 10 Box Jump Over 24\" — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas | "
  "Evita: Deadlift · Squat Clean · C2B · Burpee"),

 (11, '18–23 Agosto', 'Mes 3', [
  ('Lunes', 'METCON', 6, 20,
   "FOR TIME (Cap 6')\n7-5-3:\n· Clean & Jerk (155/105)\n· T2B"),
  ('Martes', 'STRENGTH', 17, 17,
   "4 Rounds (Cap 17')\n· 5 Bar MU / 12 C2B + 5 Ring Dip (Esc)\n"
   "· 10 HSPU / 20 Pike Push-Up (Esc)\n· 15 Box Jump Over 24\"\n· 200m Run"),
  ('Miércoles', 'GYMNASTICS', 9, 20,
   "FOR TIME (Cap 9')\n5 Rounds:\n· 5 Back Squat (155/105)\n· 10 Burpee"),
  ('Jueves', 'ACCESSORY', 26, 12,
   "5 Rounds (Cap 26')\n· 400m Run\n· 12 Power Snatch (95/65)\n· 15 WBS (20/14)"),
  ('Viernes', 'STRENGTH', 16, 17,
   "AMRAP 16'\n· 12 T2B\n· 8 Devil Press (50/35)\n· 200m Run"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n"
  "· 200m Farmer Carry KB JUNTOS (24/16)\n"
  "· 8 Push Press (95/65) @~55% — relay\n"
  "· 12 Pull-Up / Ring Row (Esc) — relay\n· 12 Box Jump Over 24\" — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas | "
  "Evita: C&J · Snatch · Back Squat · T2B · Devil Press"),

 (12, '25–30 Agosto', 'Mes 3', [
  ('Lunes', 'GYMNASTICS', 14, 17,
   "AMRAP 14'\n· 8 Front Squat (135/95)\n· 10 Box Jump Over 24\"\n· 15 WBS (20/14 lb)"),
  ('Martes', 'ACCESSORY', 28, 12,
   "CHIPPER (Cap 16')\n· 50 Air Squat\n· 30 Burpee\n· 30 T2B\n· 300m Row\n"
   "· 20 HSPU / 40 Pike Push-Up (Esc)\n· 10 Pull-Up / C2B\n"
   "· 5 Wall Walk / 10 Bear Crawl (Esc)"),
  ('Miércoles', 'METCON', 8, 20,
   "FOR TIME (Cap 8')\n4 Rounds:\n· 5 Squat Clean (135/95)\n· 12 KB Swing (32/24 kg)"),
  ('Jueves', 'STRENGTH', 18, 17,
   "EMOM 18'\n1: 3 Squat Snatch (95/65)\n2: 12 KB Swing (32/24 kg)\n"
   "3: 15/10 Cal Machine\n4: 15 WBS (20/14 lb)\n5: 200m Run\n6: Rest"),
  ('Viernes', 'STRENGTH', 22, 12,
   "\"DIANE\" MOD (Cap 12')\n21-15-9:\n· Deadlift (225/155)\n"
   "· HSPU / 2x Pike Push-Up (Esc)\n+ 50 DU entre sets"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n· 400m Run JUNTOS\n"
  "· 8 Power Clean + Jerk (95/65) @~60% — relay\n"
  "· 12 C2B / Pull-Up (Esc) — relay\n· 10 Devil Press (50/35) — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas | "
  "Evita: Front Squat · Deadlift · Snatch · HSPU · T2B"),
]

# El bloque de skill/fuerza de cada día. Va aparte porque septiembre.MES no lo
# lleva, y la línea "Evita" del sábado SÍ lo mira: el "Push Jerk" que evita la
# semana 9 no está en ningún WOD — está solo en el bloque del lunes.
BLOQUES = {
 (9, 'Lunes'):      "Power Clean + Push Jerk\n3+2 x 2 @72%\n2+1 x 2 @80%\n1+1 x 3 @88%+",
 (9, 'Martes'):     "3 sets x calidad:\nPROG. BAR MU:\n· 10 Kip Swing + 5 Hip to Bar\n"
                    "PROG. SKIN THE CAT:\n· 3 German Hang + 3 Skin the Cat\n"
                    "· 10 Hollow Rock + 10 Arch Rock",
 (9, 'Miércoles'):  "Back Squat 6x3 @83-88%\n*3 Broad Jump entre sets",
 (9, 'Jueves'):     "Row — Técnica + Intervals:\n4 x 500m @pace 2k + 20\"\n"
                    "· :90 descanso entre intervalos\n· SPM objetivo: 26-28\n"
                    "· Foco: piernas primero\n*Registrar pace cada 500m",
 (9, 'Viernes'):    "5 sets x calidad:\n· 5/5 Turkish Get-Up (accesorio)\n"
                    "· 10 DB Lateral Raise\n· 10 Face Pull\n· 12 Russian Twist KB\n"
                    "· :30 Side Plank c/lado",

 (10, 'Lunes'):     "Deadlift 5x3 @83%\n*5 Box Jump entre sets",
 (10, 'Martes'):    "Bike Sprints — Potencia:\n8 x 10\" sprint ALL OUT\n· :50 descanso activo\n"
                    "*Registrar watts máximos\n---\nRun Intervals:\n4 x 200m @95% pace\n"
                    "· :90 descanso\n*Registrar pace c/repetición",
 (10, 'Miércoles'): "3 sets x calidad:\n· 10 Single Arm DB Row\n· 10 Chest Supported Row\n"
                    "· 10 Single Leg RDL DB\n· 10 Hip Thrust con barra\n"
                    "· 5/5 Turkish Get-Up (accesorio)",
 (10, 'Jueves'):    "Power Snatch + OHS\n3+2 x 2 @72%\n2+1 x 2 @80%\n1+1 x 3 @87%+",
 (10, 'Viernes'):   "4 sets x calidad:\nPROG. BAR MU:\n· 3 Hip to Bar + transición Pull+Press\n"
                    "PROG. HSPU:\n· 5 HSPU con AbMat\nPROG. RING DIP:\n· 5/3 Ring Dip estricto",

 (11, 'Lunes'):     "Tri-Modal Aeróbico:\n· 5' Row @80% pace\n· 3' descanso activo\n"
                    "· 5' Bike @80% pace\n· 3' descanso activo\n· 5' Run @80% pace\n"
                    "*Foco: pace constante\n*No sprint — aeróbico base",
 (11, 'Martes'):    "Push Press 4x3 @80%\nBench Press 4x3 @80%",
 (11, 'Miércoles'): "4 sets x calidad:\nPROG. BAR MU:\n· 3/2 Bar MU negativo + 1-2 intentos\n"
                    "PROG. L-SIT:\n· :20 L-Sit en anillas o barras\n"
                    "PROG. PISTOL:\n· 5/5 Pistol Box o asistido\n· 5/3 Strict Pull-Up",
 (11, 'Jueves'):    "3 sets x calidad:\n· 8 DB Floor Press\n· 10 DB Fly\n· 10 Skull Crusher\n"
                    "· :30 Pallof Press c/lado\n· 10 Ab Wheel",
 (11, 'Viernes'):   "Snatch 3-2-1-1-1\n(Buscar pesado del día)\n*5 sets — WOD medio",

 (12, 'Lunes'):     "4 sets x calidad:\nPROG. BAR MU:\n· 3/2 Bar MU completo / C2B + Ring Dip (Esc)\n"
                    "PROG. SKIN THE CAT:\n· 3 Skin the Cat completo\n"
                    "PROG. HSPU:\n· 5/3 HSPU kipping",
 (12, 'Martes'):    "3 sets x calidad:\n· 10 DB Curl + 10 Hammer Curl\n· 10 Band Pull Apart\n"
                    "· 10 Single Leg Hip Thrust\n· :30 Copenhagen Plank c/lado\n"
                    "· 5/5 Turkish Get-Up (accesorio)",
 (12, 'Miércoles'): "Run — Pace Work:\n· 800m @pace objetivo\n· :2' descanso\n· x 4 rondas\n"
                    "*Foco: mantener mismo pace\n*Registrar tiempo c/800m\n---\n"
                    "Bike — Cadencia:\n· 3' @cadencia 100+ RPM\n· :2' descanso x 3",
 (12, 'Jueves'):    "Snatch Balance + OHS\n2+2 x 2 @72%\n2+1 x 2 @80%\n1+2 x 2 @85%+",
 (12, 'Viernes'):   "Power Clean 3-2-2-1-1\n(Buscar pesado del día)\n*3 sets — WOD largo",
}
