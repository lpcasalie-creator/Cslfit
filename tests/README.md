# Tests

Scripts de Node simples con Playwright — sin framework de testing ni paso de build. Cada archivo se corre directo:

```
node tests/smoke-views.js
node tests/crossfit-generator.js
node tests/signup-flow.js
```

No hace falta levantar ningún servidor a mano: cada test sirve `index.html` en memoria con `tests/lib/harness.js`.

## Qué cubre cada uno

- **smoke-views.js** — recorre las 16 vistas de la app para 3 personas (coach, alumno coacheado, alumno solo-seguimiento) y falla si alguna tira un error de página. Red de seguridad amplia: ¿algo rompió CUALQUIER vista al tocarla?
- **crossfit-generator.js** — regresión de 2 bugs reales de variabilidad: repetición de Fuerza/Skills en el borde entre semanas, y el pool de movimientos "agotado" que no activaba la red de respaldo por culpa de la ponderación por nivel.
- **signup-flow.js** — regresión del bug de producción donde los alumnos aparecían como "Alumno" genérico en Mensajes: el nombre tiene que viajar en los metadatos del signUp y, si hay sesión activa, escribirse también directo en `profiles`.

## Por qué existe esta carpeta

Antes estos tests vivían como scripts sueltos en el scratchpad de cada sesión de trabajo — que se borra entre sesiones (y una vez se borró a mitad de sesión por un reinicio del entorno, perdiendo horas de verificación). Guardarlos en el repo los hace sobrevivir.

## Si algo se rompe al correrlos

- Mismos 3 tests fallan todos por el mismo error raro (ej. "no se encontró el módulo playwright") → revisar `tests/lib/harness.js`, probablemente cambió algo del entorno (versión de Chromium, ruta de Playwright).
- Falla solo uno → revisar qué se tocó en `index.html` relacionado a ese test puntual.
