'use strict';
// Smoke test: recorre todas las vistas de la app para 3 personas (coach,
// alumno coacheado, alumno solo-seguimiento) y falla si alguna tira un error
// de página. No valida contenido específico de cada vista — eso lo cubren
// los otros 2 tests de esta carpeta para las áreas más propensas a romperse
// (generador de CrossFit, registro). Este test es la red de seguridad amplia:
// "¿algo rompió CUALQUIER vista al tocarla?".

const assert = require('assert');
const { launchBrowser, serveIndexHtml } = require('./lib/harness');

const PORT = 8139;
const VIEWS = ['home','settings','wod','timer','rm','pct','body','skills','prog','athletes','ranking','mov','hyrox','messages','scores','analysis'];

async function runForPersona(page, persona){
  const pageErrors = [];
  const onError = (e) => pageErrors.push(`[${persona.label}] ${e.message}`);
  page.on('pageerror', onError);

  await page.evaluate((p) => {
    // Asignación DIRECTA (sin "window."): sb/currentUser/currentProfile
    // están declarados con `let` en el script de la app — asignarlos vía
    // "window.sb = ..." crea una propiedad aparte en vez de tocar esa
    // misma variable léxica, y el resto del código seguiría viendo el
    // valor original (null), fallando con "Cannot read properties of
    // null" aunque window.sb tenga el mock. Mismo criterio usado en todos
    // los tests ad-hoc de esta app durante esta sesión.
    sb = window.__buildMock();
    currentUser = { id: p.userId };
    currentProfile = { role: p.role, full_name: p.fullName, plan: p.plan, coach_id: p.coachId };
    document.getElementById('authGate').style.display = 'none';
    document.getElementById('appRoot').style.display = 'block';
  }, persona);

  for(const view of VIEWS){
    await page.evaluate((v) => { try { showView(v); } catch(e) { window.__lastShowViewError = `${v}: ${e.message}`; } }, view);
    await page.waitForTimeout(40);
  }
  const showViewError = await page.evaluate(() => window.__lastShowViewError || null);
  page.off('pageerror', onError);
  return { pageErrors, showViewError };
}

async function main(){
  const server = await serveIndexHtml(PORT);
  const browser = await launchBrowser();
  try {
    const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
    await page.goto(`http://127.0.0.1:${PORT}/`);
    // El mock de sb tiene que vivir DENTRO del navegador (page.exposeFunction
    // cruza a Node en cada llamada, no sirve para un objeto encadenable
    // sincrónico como `sb.from(...).eq(...)`) — se inyecta como función
    // global, mismo código que buildSupabaseMock() de harness.js.
    await page.addScriptTag({ content: `window.__buildMock = ${buildSupabaseMockFn.toString()};` });

    const personas = [
      { label: 'coach', userId: 'coach-1', role: 'coach', fullName: 'Luis', plan: null, coachId: null },
      { label: 'alumno-coacheado', userId: 'ath-1', role: 'athlete', fullName: 'Ana', plan: 'coached', coachId: 'coach-1' },
      { label: 'alumno-solo-seguimiento', userId: 'ath-2', role: 'athlete', fullName: 'Pedro', plan: 'tracking', coachId: 'coach-1' },
    ];

    let allErrors = [];
    let allShowViewErrors = [];
    for(const persona of personas){
      const { pageErrors, showViewError } = await runForPersona(page, persona);
      allErrors = allErrors.concat(pageErrors);
      if(showViewError) allShowViewErrors.push(`[${persona.label}] ${showViewError}`);
      console.log(`${persona.label}: ${VIEWS.length} vistas recorridas, ${pageErrors.length} error(es) de página`);
    }

    assert.strictEqual(allErrors.length, 0, `Errores de página encontrados:\n${allErrors.join('\n')}`);
    assert.strictEqual(allShowViewErrors.length, 0, `showView() tiró excepción:\n${allShowViewErrors.join('\n')}`);
    console.log('OK — smoke-views: todas las vistas cargan sin error para las 3 personas.');
  } finally {
    await browser.close();
    server.close();
  }
}

// Misma lógica que buildSupabaseMock() de harness.js, pero declarada acá
// para poder inyectarla en el contexto del navegador vía toString() (el
// mock tiene que vivir ahí, no en Node, para que `sb.from(...)` funcione
// dentro de la página).
function buildSupabaseMockFn(){
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
      then(resolve){ resolve({ data: [], error: null }); },
    };
    return api;
  }
  return { from: (t) => chain(t) };
}

main().catch(e => { console.error(e); process.exit(1); });
