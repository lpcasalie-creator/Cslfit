# -*- coding: utf-8 -*-
"""Un mes de programación de CrossFit.com (sept 2026), para comparar.

NO es el modelo de Luis y no hay que leerlo como si lo fuera: son 7 días por
semana, sin estructura fija de categorías, con atletas de open gym que eligen
qué día entrenar. Su CrossTrain EIM son 5 días + sábado partner, en clases con
horario. Lo que se puede comparar es el CONTENIDO: variedad, dominios,
esquemas, carga.

Campos: (semana, día, etiqueta, formato, dominio_estimado, movimientos, texto)
"""

DIAS = [
 # ---- Semana 1 ----
 (1,'Lun','BENCHMARK','ROUNDS-REPS','glucolítico',
  ['Wall Ball','Sumo Deadlift High Pull','Box Jump','Push Press','Row'],
  'FIGHT GONE BAD · 3 rounds for reps · 1:00 cada estación · rest 1:00'),
 (1,'Mar','HEAVY','ESCALERA-CARGA','fuerza',
  ['Front Squat'], 'Front squat 3-3-3-2-2-1-1'),
 (1,'Mié','','AMRAP','glucolítico',
  ['Burpee Pull-up','KB Swing'],
  'AMRAP 10 · 50 burpee pull-ups, 75 KB swings, max burpee pull-ups'),
 (1,'Jue','','FOR TIME','aeróbico',
  ['DB Overhead Squat','DB Step-over','Double under'],
  'For time · 50/50/150 → 25/25/75'),
 (1,'Vie','','21-15-9','glucolítico',
  ['Clean and Jerk','Bike'], '21-15-9 · clean and jerks + echo bike cal'),
 (1,'Sáb','','ROUNDS','aeróbico',
  ['Run','Air Squat','Push-up','Lunge'],
  '5 rounds · 200m run, 20 air squat, 20 push-up, 20 lunge'),
 (1,'Dom','','EMOM','fuerza',
  ['Strict Pull-up','Sandbag Carry'],
  'Every 2:00 x10 · 5 strict pull-ups + 30m sandbag bear-hug carry'),

 # ---- Semana 2 ----
 (2,'Lun','HEAVY','EMOM','fuerza',
  ['Push Press'], 'Every 3:00 x5 · 5 push presses'),
 (2,'Mar','','FOR TIME','aeróbico',
  ['Run','KB Swing','KB Goblet Squat'],
  'For time · 800m run, 42/21, 30/15, 18/9, 800m run'),
 (2,'Mié','','15-12-9','glucolítico',
  ['Hang Power Clean','Burpee over Bar'],
  '15-12-9 for load and time · unbroken obligatorio'),
 (2,'Jue','','INTERVALOS','aeróbico',
  ['Row'], '10 x 2:00 · 200/250m row, rest remainder'),
 (2,'Vie','BENCHMARK','FOR TIME','aeróbico',
  ['Hang Power Snatch','Push Press','Sumo Deadlift High Pull','Front Squat'],
  'ANDI · 100 de cada uno, misma barra'),
 (2,'Sáb','','AMRAP','glucolítico',
  ['Wall Walk','Legless Rope Climb'],
  'AMRAP 12 · 2 wall walks + 2 legless rope climbs, +1 wall walk por ronda'),
 (2,'Dom','PARTNER','AMRAP','aeróbico',
  ['Bike','Toes-to-Bar','Double under','Reverse Lunge'],
  'AMRAP 21 en pareja · 20cal bike, 40 T2B, 60 DU + 20 lunges cada 3:00'),

 # ---- Semana 3 ----
 (3,'Lun','','MIXTO','aeróbico',
  ['Run','Bench Press'], '0-10: 1600m run for time · 10-20: build a 5RM bench'),
 (3,'Mar','BENCHMARK','AMRAP','glucolítico',
  ['Back Rack Lunge','Pull-up','Front Rack Lunge','Chest-to-Bar Pull-up',
   'Overhead Lunge','Bar Muscle-up'],
  'SERVICE CUP 2 · AMRAP 8'),
 (3,'Mié','BENCHMARK','MIXTO','aeróbico',
  ['Shuttle Run','Clean and Jerk'],
  'SERVICE CUP 3 · 15:00 shuttle runs + C&J, después 3:00 para 1RM C&J'),
 (3,'Jue','','AMRAP','glucolítico',
  ['Sit-up','Row'], 'AMRAP 10 · 30 AbMat sit-ups, 10/15cal row'),
 (3,'Vie','BENCHMARK','FOR TIME','aeróbico',
  ['Wall Ball','Box Jump-Over','Med-ball Box Step-over','Lateral Burpee Box Jump-Over'],
  'SERVICE CUP 1 · 50 de cada uno, cap 25:00'),
 (3,'Sáb','BENCHMARK','FOR TIME','fosfágeno',
  ['Double under','DB Snatch'],
  'SERVICE CUP 4 · 100 DU, 50 DB snatch, 100 DU · cap 5:00'),
 (3,'Dom','PARTNER','AMRAP','aeróbico',
  ['Machine','Plank','Bar Hang'],
  'AMRAP 20 en pareja · max cal, el que no trabaja sostiene plancha o colgado'),

 # ---- Semana 4 ----
 (4,'Lun','BENCHMARK','FOR TIME','fosfágeno',
  ['Clean and Jerk'], 'GRACE · 30 clean and jerks'),
 (4,'Mar','','ROUNDS','glucolítico',
  ['Thruster','Pull-up','Run'],
  'SCAREDY O\'CONNOR · 3 rounds · 15 thrusters, 15 pull-ups, 400m run'),
 (4,'Mié','','MIXTO','glucolítico',
  ['Burpee','Shuttle Box Jump-Over'],
  'BEND AND SNAP · 15:00 · 100 burpees + max shuttle box jump-overs, 4 por minuto'),
 (4,'Jue','PARTNER','AMRAP','glucolítico',
  ['DB Deadlift','Bar Hang','Toes-to-Bar','DB Farmers Hold','DB Farmers Carry','Bike'],
  'ANTI-REST · 3 x AMRAP 5 en pareja, trabajo condicionado al isométrico del otro'),
 (4,'Vie','','AMRAP','aeróbico',
  ['Handstand Walk','Row','L-sit Ring Muscle-up'],
  'ARM FARM · AMRAP 20 · HS walk 30ft, 250m row, 3 L-sit ring MU, 250m row'),
 (4,'Sáb','HEAVY','COMPLEJO','fuerza',
  ['Hang Power Snatch','Overhead Squat','Hang Squat Snatch'],
  'SNATCH COMPLEX · 7 sets for load, subiendo'),
 (4,'Dom','','ROUNDS','glucolítico',
  ['Walking Lunge','Ring Dip'],
  'MONEY MAKER · 4 rounds · 100m walking lunge, 25 ring dips'),
]
