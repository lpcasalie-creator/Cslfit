'use strict';
// Test de regresión del generador automático de CrossFit — cubre
// exactamente los 2 bugs reales encontrados y arreglados en una sesión de
// trabajo anterior (ver comentarios "Fix (auditoría de variabilidad...)" en
// index.html, función autoGenerateProgram y _crossfitPickMovement):
//
// 1. El movimiento de Fuerza/Skills del último día de una semana se repetía
//    textual en el primer día de la semana siguiente — opts._used se
//    reiniciaba vacío al empezar cada semana y nunca se sembraba con lo que
//    pasó el último día de la semana anterior (solo con el WOD, nunca con
//    Fuerza/Skills).
// 2. La ponderación por nivel (Fase 15B) duplicaba cada nombre de
//    movimiento x4/x6 ANTES de la comparación que decide si hay que
//    reintentar sobre el pool completo cuando el filtro de familia de
//    equipamiento deja pocos candidatos — así que un pool genuinamente
//    agotado (todos los candidatos libres ya usados) parecía "más grande
//    que el original" después de ponderar, y la red de respaldo (Fase 26)
//    nunca se activaba aunque hubiera alternativas reales disponibles.
//
// Esta clase de bug es sutil y ya pasó una vez sin que nadie lo notara
// durante meses — correr esto después de tocar CUALQUIER cosa en el
// generador de CrossFit (opts._used, _recentWodMovs, el filtro de familia,
// la ponderación por nivel, la inserción de benchmarks, las semanas de
// descarga/test) es más barato que volver a encontrarlo a mano.

const assert = require('assert');
const { launchBrowser, serveIndexHtml } = require('./lib/harness');

const PORT = 8140;

function buildSupabaseMockFn(){
  function chain(){
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
  return { from: () => chain() };
}

async function setup(page){
  await page.evaluate(() => {
    sb = window.__buildMock();
    currentUser = { id: 'coach-1' };
    currentProfile = { role: 'coach', full_name: 'Luis' };
    document.getElementById('authGate').style.display = 'none';
    document.getElementById('appRoot').style.display = 'block';
    showView('prog');
  });
}

function movName(txt){
  return (txt.split('\n')[0] || '').replace(/\s+\d+x.*$/, '').trim();
}

// Toma solo la primera línea real del WOD (saltando el warm-up, que es
// genérico y se repite siempre a propósito) — mismo criterio que se usó
// para verificar este fix manualmente en su momento.
function wodMainLine(txt){
  const paras = (txt || '').split('\n\n').filter(p => p.trim());
  const wodPara = paras.find(p => !/^warm-up/i.test(p.trim())) || '';
  return wodPara.split('\n')[0].trim();
}

async function checkNoWeekBoundaryRepeat(page){
  const results = await page.evaluate(({ movName, wodMainLine }) => {
    // eslint-disable-next-line no-eval
    const movNameFn = eval(`(${movName})`);
    const wodMainLineFn = eval(`(${wodMainLine})`);
    const out = [];
    for(const daysPerWeek of [4, 5]){
      const dayIndices = DAY_INDEX_MAP[daysPerWeek];
      const lastDayIdx = dayIndices[dayIndices.length - 1];
      const firstDayIdx = dayIndices[0];
      for(const weeks of [8, 12]){
        document.getElementById('genFocus').value = 'crossfit';
        document.getElementById('genWeeks').value = String(weeks);
        document.getElementById('genDays').value = String(daysPerWeek);
        document.getElementById('genDays').dispatchEvent(new Event('change'));
        document.getElementById('genLevel').value = 'intermedio';
        document.getElementById('genEquipment').value = 'completo';
        autoGenerateProgram();
        for(let w = 1; w < weeks; w++){
          const lastFuerza = document.getElementById(`day_w${w}_d${lastDayIdx}_fuerza`);
          const firstFuerza = document.getElementById(`day_w${w + 1}_d${firstDayIdx}_fuerza`);
          const lastWod = document.getElementById(`day_w${w}_d${lastDayIdx}_wod`);
          const firstWod = document.getElementById(`day_w${w + 1}_d${firstDayIdx}_wod`);
          if(!lastFuerza || !firstFuerza) continue;
          const m1 = movNameFn(lastFuerza.value), m2 = movNameFn(firstFuerza.value);
          if(m1 && m2 && m1 === m2) out.push({ daysPerWeek, weeks, semana: w, tipo: 'fuerza', movimiento: m1 });
          if(lastWod && firstWod){
            const w1 = wodMainLineFn(lastWod.value), w2 = wodMainLineFn(firstWod.value);
            if(w1 && w2 && w1 === w2) out.push({ daysPerWeek, weeks, semana: w, tipo: 'wod', valor: w1 });
          }
        }
      }
    }
    return out;
  }, { movName: movName.toString(), wodMainLine: wodMainLine.toString() });
  return results;
}

async function checkLevelWeightingFallback(page){
  // Reproduce el escenario exacto del bug #2: 5 días/semana, 12 semanas,
  // intermedio, completo — semana 6 (wi=5), patrón 'lunge', donde
  // "Bulgarian Split Squat" quedaba forzado a repetir a pesar de haber
  // "Reverse Lunge"/"Overhead Lunge" libres en el pool completo.
  return page.evaluate(() => {
    document.getElementById('genFocus').value = 'crossfit';
    document.getElementById('genWeeks').value = '12';
    document.getElementById('genDays').value = '5';
    document.getElementById('genDays').dispatchEvent(new Event('change'));
    document.getElementById('genLevel').value = 'intermedio';
    document.getElementById('genEquipment').value = 'completo';
    autoGenerateProgram();
    const dayIndices = DAY_INDEX_MAP[5];
    const lastDayIdx = dayIndices[dayIndices.length - 1];
    const firstDayIdx = dayIndices[0];
    const w5wod = document.getElementById(`day_w5_d${lastDayIdx}_wod`).value;
    const w6wod = document.getElementById(`day_w6_d${firstDayIdx}_wod`).value;
    return { w5wod, w6wod, repiteBulgarian: /bulgarian split squat/i.test(w5wod) && /bulgarian split squat/i.test(w6wod) };
  });
}

async function main(){
  const server = await serveIndexHtml(PORT);
  const browser = await launchBrowser();
  try {
    const page = await (await browser.newContext({ viewport: { width: 390, height: 844 } })).newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push(e.message));
    await page.goto(`http://127.0.0.1:${PORT}/`);
    await page.addScriptTag({ content: `window.__buildMock = ${buildSupabaseMockFn.toString()};` });
    await setup(page);

    const repeats = await checkNoWeekBoundaryRepeat(page);
    console.log(`Barrido de borde entre semanas (4/5 días × 8/12 semanas): ${repeats.length} repetición(es) encontrada(s)`);
    assert.strictEqual(repeats.length, 0, `Repeticiones en el borde entre semanas:\n${JSON.stringify(repeats, null, 2)}`);

    const levelWeighting = await checkLevelWeightingFallback(page);
    console.log(`Caso ponderación por nivel (5 días, 12 semanas, semana 5→6): ¿repite Bulgarian Split Squat? ${levelWeighting.repiteBulgarian}`);
    assert.strictEqual(levelWeighting.repiteBulgarian, false,
      `El movimiento se repitió a pesar de haber alternativas libres.\nSemana 5: ${levelWeighting.w5wod}\nSemana 6: ${levelWeighting.w6wod}`);

    assert.strictEqual(pageErrors.length, 0, `Errores de página durante la generación:\n${pageErrors.join('\n')}`);
    console.log('OK — crossfit-generator: sin repeticiones en el borde entre semanas, sin errores.');
  } finally {
    await browser.close();
    server.close();
  }
}

main().catch(e => { console.error(e); process.exit(1); });
