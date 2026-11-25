'use strict';
// Test de regresión del registro con nombre — cubre el bug real encontrado
// en producción: los 8 alumnos de Luis aparecían como "Alumno" genérico en
// Mensajes porque el formulario de registro nunca pedía el nombre
// (profiles.full_name quedaba null para siempre). El fix (ver index.html,
// signUpWithCode) tiene DOS caminos que tienen que funcionar los dos:
//   1. El nombre viaja en options.data.full_name del signUp — necesario
//      para el caso en que el alta requiere confirmar email por correo (sin
//      sesión activa todavía, no se puede escribir en profiles por RLS).
//   2. Si YA hay sesión activa tras el signUp, se escribe el nombre directo
//      en profiles — red de respaldo que no depende de que exista (o
//      funcione) un trigger del lado de Supabase que lea los metadatos.
// Este test verifica ambos caminos por separado, más la validación de
// campo vacío.

const assert = require('assert');
const { launchBrowser, serveIndexHtml } = require('./lib/harness');

const PORT = 8141;

function buildSignupMockFn(withSession){
  function chain(table){
    const api = {
      select(){ return api; }, eq(){ return api; }, neq(){ return api; },
      is(){ return api; }, order(){ return api; }, in(){ return api; },
      limit(){ return api; }, gte(){ return api; }, lte(){ return api; },
      async single(){ return { data: null, error: { message: 'n/a' } }; },
      async maybeSingle(){
        if(table === 'profiles') return { data: { id: 'user-1', role: 'athlete', plan: 'tracking', full_name: null }, error: null };
        return { data: null, error: null };
      },
      async insert(row){ return { data: [{ id: 'mock-id', ...row }], error: null }; },
      update(row){
        if(table === 'profiles') window.__calls.profileUpdates.push(row);
        return api;
      },
      async upsert(row){ return { data: [row], error: null }; },
      async delete(){ return { data: null, error: null }; },
      then(resolve){ resolve({ data: [], error: null }); },
    };
    return api;
  }
  window.__calls = { signUpArgs: null, profileUpdates: [] };
  return {
    auth: {
      signUp: async (args) => {
        window.__calls.signUpArgs = args;
        return {
          data: { user: { id: 'user-1' }, session: withSession ? { user: { id: 'user-1' }, access_token: 'tok' } : null },
          error: null,
        };
      },
    },
    rpc: async (fn) => {
      if(fn === 'validate_invite_code') return { data: true, error: null };
      if(fn === 'consume_invite_code') return { data: null, error: null };
      return { data: null, error: null };
    },
    from: (t) => chain(t),
  };
}

async function fillAndSubmit(page, { code, name, email, password }){
  await page.evaluate(({ code, name, email, password }) => {
    document.getElementById('signupCode').value = code;
    document.getElementById('signupName').value = name;
    document.getElementById('signupEmail').value = email;
    document.getElementById('signupPassword').value = password;
  }, { code, name, email, password });
  // signUpWithCode() es async — hay que esperar la promesa real, no un timeout a ciegas.
  await page.evaluate(() => signUpWithCode());
}

async function main(){
  const server = await serveIndexHtml(PORT);
  const browser = await launchBrowser();
  try {
    const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push(e.message));
    await page.goto(`http://127.0.0.1:${PORT}/`);
    await page.evaluate(() => {
      document.getElementById('authSignup').style.display = 'block';
      document.getElementById('authStep1').style.display = 'none';
    });

    // Caso 1: alta requiere confirmar email (sin sesión activa todavía) —
    // el nombre tiene que viajar en los metadatos del signUp.
    await page.addScriptTag({ content: `window.__buildSignupMock = ${buildSignupMockFn.toString()};` });
    await page.evaluate(() => { sb = window.__buildSignupMock(false); });
    await fillAndSubmit(page, { code: 'LUIS-ABCD', name: 'Ana Pérez', email: 'ana@test.com', password: '123456' });
    const case1 = await page.evaluate(() => ({
      fullNameEnMetadatos: window.__calls.signUpArgs && window.__calls.signUpArgs.options && window.__calls.signUpArgs.options.data && window.__calls.signUpArgs.options.data.full_name,
      profileUpdates: window.__calls.profileUpdates,
      msg: document.getElementById('signupMsg').textContent,
    }));
    console.log('Caso 1 (sin sesión, requiere confirmar email):', JSON.stringify(case1));
    assert.strictEqual(case1.fullNameEnMetadatos, 'Ana Pérez', 'El nombre no viajó en options.data.full_name del signUp');
    assert.strictEqual(case1.profileUpdates.length, 0, 'No debería intentar un update directo sin sesión activa (RLS lo rechazaría)');

    // Caso 2: alta con sesión activa inmediata — además de los metadatos,
    // tiene que escribir el nombre directo en profiles (red de respaldo).
    await page.evaluate(() => { sb = window.__buildSignupMock(true); });
    await fillAndSubmit(page, { code: 'LUIS-EFGH', name: 'Pedro Gómez', email: 'pedro@test.com', password: '123456' });
    const case2 = await page.evaluate(() => ({
      fullNameEnMetadatos: window.__calls.signUpArgs.options.data.full_name,
      profileUpdates: window.__calls.profileUpdates,
    }));
    console.log('Caso 2 (con sesión activa):', JSON.stringify(case2));
    assert.strictEqual(case2.fullNameEnMetadatos, 'Pedro Gómez', 'El nombre no viajó en options.data.full_name del signUp');
    assert.strictEqual(case2.profileUpdates.length, 1, 'Con sesión activa, debería escribir profiles.full_name directo como red de respaldo');
    assert.strictEqual(case2.profileUpdates[0].full_name, 'Pedro Gómez', 'El update directo no llevó el nombre correcto');

    // Caso 3: validación de campo vacío — sin nombre, no debe ni intentar el signUp.
    await page.evaluate(() => { sb = window.__buildSignupMock(false); window.__calls.signUpArgs = null; });
    await fillAndSubmit(page, { code: 'LUIS-IJKL', name: '', email: 'sin-nombre@test.com', password: '123456' });
    const case3 = await page.evaluate(() => ({
      signUpLlamado: window.__calls.signUpArgs !== null,
      msg: document.getElementById('signupMsg').textContent,
    }));
    console.log('Caso 3 (nombre vacío):', JSON.stringify(case3));
    assert.strictEqual(case3.signUpLlamado, false, 'No debería llamar a signUp si falta el nombre');

    assert.strictEqual(pageErrors.length, 0, `Errores de página:\n${pageErrors.join('\n')}`);
    console.log('OK — signup-flow: el nombre viaja en metadatos, se escribe directo con sesión activa, y se valida como campo obligatorio.');
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch(e => { console.error(e); process.exit(1); });
