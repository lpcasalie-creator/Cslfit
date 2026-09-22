# -*- coding: utf-8 -*-
"""CrossTrain EIM — Mes 2 (Semanas 5-8). Transcrito de su planilla.

OJO: este mes usa OTRAS CATEGORÍAS. La planilla dice
    ■ HALTEROFILIA  ■ GIMNASIA  ■ FUERZA  ■ MUSCULACIÓN
y no existe METCON. En el mes 3 ya aparecen las de hoy —STRENGTH, GYMNASTICS,
METCON, ACCESSORY— con HALTEROFILIA y FUERZA fundidas en STRENGTH (por eso son
dos por semana) y METCON estrenándose. Se deja el nombre original y aparte la
equivalencia, para no borrar el cambio.

Y la leyenda de este mes trae el dato que más corrige lo que yo tenía:
    🟢 Corto <12'  ·  🟡 Medio 14-19'  ·  🔴 Largo 20'+
    Distribución objetivo: 30% / 50% / 20%
No 25/50/25, que es lo que yo venía usando.

Este mes NO lleva minutos de skill escritos por día, así que van en None.
"""

EQUIVALENCIA = {'HALTEROFILIA': 'STRENGTH', 'FUERZA': 'STRENGTH',
                'GIMNASIA': 'GYMNASTICS', 'MUSCULACIÓN': 'ACCESSORY'}

LEYENDA = {'corto': '<12', 'medio': '14-19', 'largo': '20+',
           'objetivo': {'corto': .30, 'medio': .50, 'largo': .20}}

MES = [
 (5, 'Semana 5', 'Mes 2', [
  ('Lunes', 'HALTEROFILIA', 8, None,
   "FOR TIME (Cap 8')\n3 Rounds:\n· 7 Power Clean (155/105)\n· 7 Bar-Facing Burpee"),
  ('Martes', 'GIMNASIA', 14, None,
   "AMRAP 14'\n· 15 C2B o Pull-Up\n· 12 Box Jump Over 30\"\n· 9 HSPU / Pike\n· 50 DU"),
  ('Miércoles', 'FUERZA', 20, None,
   "EMOM 20'\n1: 5 Thrusters (115/75)\n2: 10 KB Swing (24/16)\n3: 15 Air Squats\n"
   "4: 12 Cal Bike\n5: Rest"),
  ('Jueves', 'HALTEROFILIA', 16, None,
   "4 Rounds (Cap 16')\n· 10 Power Snatch (75/55)\n· 12 WBS (20/14)\n"
   "· 3/2 Wall Walk\n· 200m Run"),
  ('Viernes', 'MUSCULACIÓN', 10, None,
   "AMRAP 10'\n· 6 Ring Dip o Box Dip\n· 9 DB Push Press (50/35)\n· 12 DB FR Lunge"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n· 400m Run JUNTOS\n"
  "· 15 KB Swing (24/16) — relay\n· 10 T2B — relay\n· 10 Burpee — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas"),

 (6, 'Semana 6', 'Mes 2', [
  ('Lunes', 'FUERZA', 7, None,
   "FOR TIME (Cap 7')\n21-15-9:\n· Deadlift (225/155)\n· Bar-Facing Burpee"),
  ('Martes', 'HALTEROFILIA', 10, None,
   "BENCHMARK\n\"Grace\"\n30 Clean & Jerk for Time (135/95)\n*Cap: 10'"),
  ('Miércoles', 'GIMNASIA', 9, None,
   "AMRAP 9'\n· 5 HSPU / Pike\n· 10 Box Jump Over 24\"\n· 15 DU"),
  ('Jueves', 'HALTEROFILIA', 22, None,
   "5 Rounds (Cap 22')\n· 400m Run\n· 10 HPC (115/75)\n· 10 T2B"),
  ('Viernes', 'FUERZA', 18, None,
   "EMOM 18'\n1: 14 DB FR Lunge (50/35)\n2: 50\" Max Cal Machine\n"
   "3: 12 Push Jerk (115/75)\n4: 40 DU\n5: 10 DB Row c/lado\n6: Rest"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n· 50 DU JUNTOS (25 c/u alternando)\n"
  "· 15 WBS (20/14) — relay\n· 10 Power Clean (115/75) — relay\n"
  "· 10 DB Lunge (50/35) — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas"),

 (7, 'Semana 7', 'Mes 2', [
  ('Lunes', 'FUERZA', 8, None,
   "FOR TIME (Cap 8')\n5 Rounds:\n· 5 Front Squat (135/95)\n· 10 Burpee over Bar"),
  ('Martes', 'GIMNASIA', 20, None,
   "3 Rounds (Cap 20')\n· 500m Row\n· 15 C2B / Pull-Up\n· 12 HSPU / Pike\n· 20 DU"),
  ('Miércoles', 'HALTEROFILIA', 14, None,
   "AMRAP 14'\n· 5 DB Snatch c/lado (70/50)\n· 10 Box Jump 24\"/20\"\n· 15 WBS (20/14)"),
  ('Jueves', 'FUERZA', 10, None,
   "AMRAP 10'\n· 8 KB Swing (32/24)\n· 10 Push-Up\n· 12 Air Squat\n· 14 Cal Bike"),
  ('Viernes', 'HALTEROFILIA', 24, None,
   "\"JACKIE\" MOD\n· 1000m Row\n· 50 Thrusters (45/35)\n· 30 Pull-Up / C2B\n· 400m Run"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n· 400m Run JUNTOS\n"
  "· 15 KB Swing (32/24) — relay\n· 10 Devil Press (50/35) — relay\n"
  "· 10 Wall Ball (20/14) — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas"),

 (8, 'Semana 8', 'Mes 2', [
  ('Lunes', 'HALTEROFILIA', 10, None,
   "FOR TIME (Cap 10')\n10-8-6-4-2:\n· Power Snatch (95/65)\n· Bar Muscle-Up o C2B"),
  ('Martes', 'FUERZA', 24, None,
   "\"NANCY\" MOD\n5 Rounds:\n· 400m Run\n· 15 OHS (95/65)"),
  ('Miércoles', 'GIMNASIA', 25, None,
   "CHIPPER (Cap 25')\n· 50 WBS (20/14)\n· 40 Box Jump Over\n· 30 HSPU / Pike\n"
   "· 20 DU\n· 10 Bar MU o C2B"),
  ('Jueves', 'HALTEROFILIA', 30, None,
   "EMOM 30'\n1: 3 Clean & Jerk (145/95)\n2: 10/6 C2B\n3: 15/10 Cal Machine\n"
   "4: 12 T2B\n5: 100m Shuttle Run\n6: Rest"),
  ('Viernes', 'MUSCULACIÓN', 24, None,
   "ESCALERA EMPUJE\n· 21 Push Jerk (135/85)\n· 800m Run\n· 15 Push Jerk (155/105)\n"
   "· 400m Run\n· 9 Split Jerk (175/115)\n· 200m Run"),
 ],
  "PARTNER WOD — AMRAP 35' | I go / You go\n"
  "· 200m Farmer Carry KB JUNTOS (24/16)\n· 15 T2B — relay\n· 12 Pull-Up — relay\n"
  "· 10 DB Snatch c/lado (50/35) — relay\n"
  "Score: rondas + reps | Mejor dupla: 5-6 rondas"),
]

BLOQUES = {
 (5, 'Lunes'):      "Power Clean + Split Jerk\n3+1 x 3 @70%\n2+1 x 3 @78%\n1+1 x 3 @85%+",
 (5, 'Martes'):     "4 sets:\n· 4/2 Strict Pull-Up + C2B\n· 3/2 Ring Dip estricto\n"
                    "· 5 Box Jump 30\"/24\"\n· 10 V-Up",
 (5, 'Miércoles'):  "Back Squat 5x4 @80-85%\n*3 Broad Jump entre sets",
 (5, 'Jueves'):     "Power Snatch + Hang Snatch\n3+2 x 2 @70%\n2+1 x 3 @78%\n1+1 x 3 @85%+",
 (5, 'Viernes'):    "4 sets:\n· 8 Bench Press @70%\n· 10 Bent Over Row\n"
                    "· 10 DB Arnold Press\n· 10 Biceps + 10 Triceps",

 (6, 'Lunes'):      "Deadlift 5x4 @80%\n*5 Box Jump entre sets",
 (6, 'Martes'):     "Snatch Balance + OHS\n3+3 x 2 @65%\n2+2 x 2 @73%\n1+2 x 3 @80%+",
 (6, 'Miércoles'):  "EMOM 15'\n1: 5 HSPU / Pike\n2: 4/3 Rope Climb o 6 Ring Row\n"
                    "3: 20-30\" HS libre\n4: 3/2 Wall Walk\n5: 10 T2B estricto",
 (6, 'Jueves'):     "Clean Pull + Squat Clean\n3+2 x 2 @73%\n2+2 x 2 @80%\n1+1 x 3 @87%+",
 (6, 'Viernes'):    "Strict Press 5x4 @70-78%\n*10 Lateral Raise entre sets",

 (7, 'Lunes'):      "Front Squat 5x3 @83%+\n*4 Broad Jump entre sets",
 (7, 'Martes'):     "4 sets:\n· 5/3 Bar MU o 5 C2B + 5 Dip\n· 5/3 Strict HSPU\n"
                    "· 10 Hollow Rock\n· :30 L-Sit",
 (7, 'Miércoles'):  "Power Snatch + Snatch Balance\n3+2 x 2 @70%\n2+2 x 2 @78%\n1+1 x 3 @85%+",
 (7, 'Jueves'):     "Bench Press 5x5 @78%\nStrict Pull-Up 5x5\n(lastrado si >10 reps)",
 (7, 'Viernes'):    "Power Clean 3-3-2-2-1-1\n(Buscar pesado, +5kg vs Mes 1)",

 (8, 'Lunes'):      "Power Snatch + OHS\n3+3 x 2 @65%\n3+2 x 2 @73%\n2+1 x 3 @82%\n"
                    "Snatch: 3x3 AHAP",
 (8, 'Martes'):     "Back Squat 1RM\n40%x5\n60%x3\n75%x2\n85%x1\n92%x1\n1RM",
 (8, 'Miércoles'):  "4 sets:\n· 3 Wall Walk + 15 Shoulder Tap\n· 5/3 Strict HSPU\n"
                    "· 4/2 Bar MU o 6 C2B\n· 20 DU unbroken",
 (8, 'Jueves'):     "Push Press + Push Jerk + Split Jerk\n3+2+1 x 2 @68%\n"
                    "2+2+1 x 2 @76%\n1+1+1 x 3 @83%+",
 (8, 'Viernes'):    "4 sets:\n· 6 Turkish Get-Up c/lado\n· 10 Pendlay Row\n"
                    "· 10 Biceps Curl\n· 12 Alt Reverse Lunge\n· 10 Skull Crusher",
}
