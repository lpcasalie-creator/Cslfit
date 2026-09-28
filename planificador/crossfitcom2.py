# -*- coding: utf-8 -*-
"""Segundo mes de CrossFit.com (27 jul – 30 ago 2026). Duplica la muestra.

Con dos meses ya se puede separar lo que es patrón de lo que era casualidad
del primero. Mismos campos que crossfitcom.py.
"""

DIAS = [
 # ---- Semana 1 ----
 (1,'Lun','','INTERVALOS','aeróbico',['Run'],
  '2 rounds each for time · 1600m run · descansa exactamente tu tiempo'),
 (1,'Mar','BENCHMARK','ESCALERA-BAJA','aeróbico',
  ['Deadlift','Bench Press','Squat Clean'],
  'LINDA · 10-9-8...1 · cargas relativas al peso corporal (1.5x / 1x / .75x)'),
 (1,'Mié','','INTERVALOS-REPS','glucolítico',
  ['Row','DB Hang Snatch','Burpee'],
  '5 x 3:00 for reps · 15/20cal row, 20 DB snatch, max DB-facing burpees · rest 1:00'),
 (1,'Jue','','AMRAP-INTERRUMPIDO','glucolítico',
  ['Double under','Toes-to-Bar','Box Jump'],
  'AMRAP 12 · 24 DU + 12 T2B · cada 2:00 parar y hacer 12 box jumps, retomar donde iba'),
 (1,'Vie','','ESCALERA-SUBE-BAJA','glucolítico',
  ['Ring Muscle-up','Back Squat'],
  'For time · 2-4-6-8-6-4-2 de ring MU y back squat'),
 (1,'Sáb','PARTNER','ROUNDS','aeróbico',
  ['DB Hang Power Clean','DB Push Press','DB Farmers Carry'],
  '5 rounds en pareja · 20 DB HPC, 20 DB push press, 200m farmers carry'),
 (1,'Dom','','AMRAP-ESCALERA','glucolítico',
  ['Legless Rope Climb','Power Snatch'],
  'AMRAP 16 · 2 legless rope climbs, 4 power snatches · +1 snatch cada ronda'),

 # ---- Semana 2 ----
 (2,'Lun','','ROUNDS','aeróbico',['Run','Overhead Squat'],
  '3 rounds · 800m run, 15 overhead squats'),
 (2,'Mar','BENCHMARK','ESCALERA-BAJA','aeróbico',
  ['Double under','Sit-up','Strict Muscle-up'],
  'MUSCLE-UP ANNIE · 50/40/30/20/10 DU y sit-ups, 5/4/3/2/1 strict MU'),
 (2,'Mié','HEAVY','ESCALERA-CARGA','fuerza',['Power Clean'],
  'For load · power clean 3-3-3-3-3'),
 (2,'Jue','','AUTORREGULADO','aeróbico',['Bike'],
  'Every 4:00 x5 · bike sosteniendo watts · el primer minuto fija tu marca, '
  'las 4 rondas siguientes pedaleas mientras la mantengas'),
 (2,'Vie','BENCHMARK','FOR TIME','aeróbico',
  ['Row','Pull-up','Shoulder-to-Overhead'],
  'COMMUNITY CUP 1 · 1000m row, después 5 rounds de 25 pull-ups y 7 S2O'),
 (2,'Sáb','','ROUNDS','aeróbico',['Med-ball Clean','Ring Dip'],
  '5 rounds · 30 med-ball cleans, 20 ring dips'),
 (2,'Dom','PARTNER','ROUNDS','aeróbico',
  ['KB Swing','Bottoms-up KB Carry','L-sit'],
  '10 rounds en pareja alternando · 30 KB swings, 30m bottoms-up carry · '
  'el que descansa acumula tiempo en L-sit'),

 # ---- Semana 3 ----
 (3,'Lun','','INTERVALOS-TIEMPO','glucolítico',
  ['Box Jump-Over','DB Deadlift','DB Hang Power Clean','DB Shoulder-to-Overhead'],
  '5 sets each for time · 15/12/9/6 · rest exactamente 2:00 entre sets'),
 (3,'Mar','BENCHMARK','FOR TIME','aeróbico',['Row'], '5K ROW · 5000m row for time'),
 (3,'Mié','','ESCALERA-BAJA','glucolítico',
  ['DB Walking Lunge','Deficit Strict HSPU'],
  'For time · lunge 200/150/100/50 ft, deficit strict HSPU 20/15/10/5'),
 (3,'Jue','','ROUNDS','aeróbico',
  ['Toes-to-Bar','Rope Climb','Bike'],
  '3 rounds · 30 T2B, 3 rope climbs, 24/30cal bike'),
 (3,'Vie','BENCHMARK','MAX-CARGA','fuerza',
  ['Back Squat','Press','Deadlift'],
  'CROSSFIT TOTAL · 1RM back squat + 1RM press + 1RM deadlift'),
 (3,'Sáb','PARTNER','FOR TIME','aeróbico',
  ['Run','Air Squat','Burpee','Plate Run','Push Press','Pull-up','Power Clean'],
  'LGOP · equipos de 2-4 · 1940m run juntos, 250 air squats, 48 burpees, '
  '509m run con disco, 101 push press, 11 pull-ups c/u, 82 power cleans'),
 (3,'Dom','','INTERVALOS-SUBE','glucolítico',
  ['Double under','Snatch'],
  'For reps · 1:00 DU / 1:00 snatch / 2:00 DU / 2:00 snatch / 3:00 DU / 3:00 snatch'),

 # ---- Semana 4 ----
 (4,'Lun','','FOR TIME','glucolítico',
  ['Pull-up','Hang Squat Clean','Row'],
  'For time · 50 pull-ups, 50 hang squat cleans, 50cal row'),
 (4,'Mar','','21-18-15-12-9','glucolítico',
  ['DB Bench Press','Hand-release Push-up'],
  '21-18-15-12-9 · DB bench press y hand-release push-ups'),
 (4,'Mié','','ROUNDS','aeróbico',
  ['GHD Sit-up','Med-ball Box Step-up','Med-ball Run'],
  '3 rounds · 30 GHD sit-ups, 30 med-ball box step-ups, 400m med-ball run'),
 (4,'Jue','HEAVY','ESCALERA-CARGA','fuerza',['Split Jerk'],
  'For load · split jerk 1-1-1-1-1-1-1'),
 (4,'Vie','BENCHMARK','AMRAP-TRIPLE','glucolítico',
  ['Shuttle Run','Toes-to-Bar','Power Snatch','Overhead Squat','Squat Snatch'],
  'COMMUNITY CUP 3 · 3 x AMRAP 4 con 2:00 de descanso · misma entrada '
  '(10 shuttle, 21 T2B) y cambia el max: power snatch / OHS / squat snatch'),
 (4,'Sáb','','FOR TIME-ISO','glucolítico',
  ['L-sit','Deadlift','Burpee over Bar'],
  'For time · :30 L-sit entre cada bloque · 20 deadlifts, 40 bar-facing burpees, 20 deadlifts'),
 (4,'Dom','','AMRAP','aeróbico',
  ['Wall Ball','Bike','Wall Walk'],
  'AMRAP 20 · 25 wall balls, 10/15cal bike, 5 wall walks'),

 # ---- Semana 5 (parcial, cierra el mes) ----
 (5,'Lun','HEAVY','ESCALERA-CARGA','fuerza',['Snatch'],
  'For load · snatch 2-2-2-2-2-2-2'),
 (5,'Mar','','INTERVALOS-MAX','glucolítico',
  ['Run','Chest-to-Bar Pull-up','HSPU','DB Goblet Squat'],
  '2 rounds · tres bloques de 3:00 · 400m run + max de algo, 1:00 rest entre cada uno'),
 (5,'Mié','','ROUNDS','aeróbico',
  ['Row','Sit-up','Box Jump-Over'],
  '3 rounds · 600/750m row, 50 sit-ups, 25 box jump-overs'),
 (5,'Jue','','FOR TIME-ENCADENADO','aeróbico',
  ['Farmers Carry','Burpee','Rope Climb'],
  'For time · 400m farmers carry, y de ahí directo a 10 rounds de 5 burpees + 1 rope climb'),
 (5,'Vie','BENCHMARK','ROUNDS','aeróbico',
  ['Double under','Air Squat','DB Snatch'],
  'COMMUNITY CUP 4 · 2 rounds · 150 DU, 100 air squats, 50 DB snatches'),
 (5,'Sáb','','ESCALERA-CARGA-SUBE','glucolítico',
  ['Power Clean','High Ring Dip','Muscle-up'],
  'For time · 21/15/9 power cleans subiendo carga (95/125/155) + high ring dips · '
  'muscle-up para subir a las anillas cada vez que se corta'),
 (5,'Dom','PARTNER','FOR TIME','aeróbico',
  ['Shuttle Run','Walking Lunge Shuttle','Toes-to-Bar'],
  'En pareja · 40 shuttle runs, 20 walking lunge shuttles, 100 T2B · '
  'en cualquier orden, uno trabaja a la vez'),
]
