'use strict';
// Harness compartido para los tests de esta carpeta — scripts de Node
// simples, sin framework de testing ni dependencias nuevas (mismo criterio
// que el resto de la app: cero build step). Cada archivo de este directorio
// se corre directo con `node tests/<archivo>.js`.
//
// Por qué existe este archivo: todos los tests ad-hoc de una sesión de
// trabajo anterior vivían en un scratchpad que se borra entre sesiones — y
// de hecho se borró en medio de esa misma sesión por un reinicio del
// entorno, perdiendo horas de trabajo de verificación. Estos 3 tests son
// los de mayor valor que sobrevivieron, guardados acá para no repetir eso.

const fs = require('fs');
const path = require('path');
const http = require('http');

function resolvePlaywright(){
  const candidates = ['playwright', '/opt/node22/lib/node_modules/playwright'];
  for(const c of candidates){
    try { return require(c); } catch(e) { /* probar el siguiente */ }
  }
  throw new Error('No se encontró el módulo playwright. Probé: ' + candidates.join(', '));
}

function resolveChromiumPath(){
  // El symlink sin número de versión es más estable que hardcodear
  // "chromium-1243" — ya cambió una vez en esta sesión y rompió todos los
  // scripts viejos que sí lo hardcodeaban.
  const candidates = [process.env.PLAYWRIGHT_CHROMIUM_PATH, '/opt/pw-browsers/chromium'].filter(Boolean);
  for(const c of candidates){
    if(fs.existsSync(c)) return c;
  }
  return undefined; // Playwright usa su propio default si no hay ninguno
}

const INDEX_HTML_PATH = path.join(__dirname, '..', '..', 'index.html');

// Sirve index.html en memoria — evita depender de un proceso aparte
// (`python3 -m http.server`) que hay que recordar levantar y matar.
function serveIndexHtml(port){
  return new Promise((resolve, reject) => {
    const html = fs.readFileSync(INDEX_HTML_PATH);
    const server = http.createServer((req, res) => {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
    });
    server.on('error', reject);
    server.listen(port, '127.0.0.1', () => resolve(server));
  });
}

async function launchBrowser(){
  const { chromium } = resolvePlaywright();
  const executablePath = resolveChromiumPath();
  return chromium.launch(executablePath ? { executablePath } : {});
}

// Mock de Supabase reutilizable — mismo patrón usado en todos los tests de
// esta app esta sesión. `tables` es { nombreTabla: array-de-filas |
// función(api)=>{data,error} }; lo que no se especifica devuelve [].
//
// Gotcha documentado (picó varias veces durante el trabajo real en esta
// app): update()/delete() tienen que ser funciones SÍNCRONAS que devuelven
// `api` para poder seguir encadenando .eq() — si se declaran `async`, la
// cadena `sb.from(t).update(x).eq('id', y)` revienta con
// "TypeError: ....update(...).eq is not a function" porque update() ya
// devolvió una Promise en vez del objeto encadenable.
function buildSupabaseMock(tables){
  tables = tables || {};
  function chain(table){
    const api = {
      select(){ return api; }, eq(){ return api; }, neq(){ return api; },
      is(){ return api; }, order(){ return api; }, in(){ return api; },
      limit(){ return api; }, gte(){ return api; }, lte(){ return api; },
      async single(){ return { data: null, error: { message: 'n/a' } }; },
      async maybeSingle(){ return { data: null, error: null }; },
      async insert(row){ return { data: [{ id: 'mock-id', ...row }], error: null }; },
      update(){ return api; },
      async upsert(row){ return { data: [row], error: null }; },
      async delete(){ return { data: null, error: null }; },
      then(resolve){
        const t = tables[table];
        if(typeof t === 'function') return resolve(t(api));
        resolve({ data: t || [], error: null });
      },
    };
    return api;
  }
  return { from: (t) => chain(t) };
}

module.exports = { launchBrowser, serveIndexHtml, buildSupabaseMock, INDEX_HTML_PATH };
