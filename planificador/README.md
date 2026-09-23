# Planificador de WODs — CrossTrain EIM

Genera un mes de programación (4 semanas × 5 días + Partner WOD del sábado)
con las reglas sacadas de medir las planillas reales de Luis, no de inventar
criterios. Es una herramienta aparte: **no toca la app** (`index.html`).

## Correr

    cd planificador
    python3 octubre.py          # el mes 1 (Base), con fechas
    python3 semana.py 2         # un mes del ciclo 2, a pantalla
    python3 auditar.py 2 20     # 20 meses generados por el validador
    python3 medir.py 40         # separación entre repeticiones, con y sin regla

Necesita `openpyxl`. Los tres `.xlsx` son el catálogo de movimientos y los lee
desde esta carpeta, así que hay que correrlo desde acá.

## De dónde salen las reglas

Tres meses transcritos de sus planillas — `mes2.py` (semanas 5-8), `mes3.py`
(9-12) y `septiembre.py` (13-16), 72 días en total — más dos meses de
CrossFit.com (`crossfitcom.py`, `crossfitcom2.py`, 63 días) que sirven
**solo de contraste**, nunca de modelo: son 7 días por semana de open gym
contra sus 5 días de clases con horario.

Cada regla del generador tiene el número que la respalda escrito arriba, en el
módulo donde vive. Las que no están medidas dicen que no lo están.

## Los módulos

| archivo | qué hace |
|---|---|
| `generar2.py` | elige categorías, dominios y movimientos de la semana. Techos mensual y semanal, y la separación mínima entre repeticiones |
| `prescribir.py` | escribe el WOD: formato, repeticiones, distancias, cargas y cap |
| `bloque.py` | el bloque de skill/fuerza previo al WOD, con la escalera de porcentajes por fase |
| `sabado.py` | el Partner WOD, que repasa la semana a ritmo de pareja |
| `semana.py` | arma la semana y el mes, con vuelta atrás cuando una semana se queda sin salida |
| `validar.py` | las 14 reglas, corriendo sobre un mes escrito a mano o generado |
| `auditar.py` | pasa N meses generados por el validador |
| `medir.py` | mide la separación entre repeticiones, con y sin la regla |
| `separacion.py` | la misma medida sobre sus tres meses (es de donde sale el 4) |
| `planilla_html.py` | la salida con la marca, para imprimir |

## Lo que falta

`octubre.py` sale con un aviso amarillo porque el **Mes 1 (Base) es el único
sin planilla de referencia**: los porcentajes y la escalera de series son
extrapolados. Para sacarlo faltan cuatro datos que solo tiene Luis:

1. en qué porcentaje arranca el mes Base;
2. si el mes 1 lleva notas de potenciación (meses 2-3) o descanso + foco
   técnico (mes 4);
3. si el Base cierra con algún max o sin test;
4. las cargas de Back Squat, Clean and Jerk, Overhead Squat, Split Jerk y
   Thruster, que hoy se generan sin peso.
