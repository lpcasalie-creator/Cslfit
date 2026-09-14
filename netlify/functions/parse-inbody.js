// Recibe una foto de un reporte InBody (base64) y devuelve los 8 campos de
// Composición Corporal ya estructurados, usando la API de Claude con visión.
// La API key vive SOLO acá (variable de entorno de Netlify) — nunca llega al
// cliente, que sólo ve el JSON de resultado.
const FIELDS = ['weight', 'pgc', 'smm', 'fatMass', 'bmi', 'visceral', 'water', 'bmr'];

const PROMPT = `Esta es una foto de un reporte de composición corporal (InBody u otra báscula de bioimpedancia). Extrae EXACTAMENTE estos 8 valores si están visibles y legibles en la imagen:

- weight: peso corporal en kg
- pgc: porcentaje de grasa corporal (PBF / % Body Fat)
- smm: masa muscular esquelética en kg (SMM / Skeletal Muscle Mass)
- fatMass: masa grasa corporal en kg (Body Fat Mass)
- bmi: índice de masa corporal (BMI/IMC)
- visceral: nivel de grasa visceral (Visceral Fat Level, número entero sin unidad)
- water: agua corporal total, como porcentaje (%). Si el reporte sólo trae el agua corporal en litros y no hay forma de saber el porcentaje, deja este campo en null.
- bmr: tasa metabólica basal en kcal (BMR/TMB)

Responde ÚNICAMENTE con un objeto JSON plano con exactamente esas 8 claves. Cada valor debe ser un número (usa punto decimal, no coma) o null si ese dato no aparece en la imagen o no se alcanza a leer con certeza. No inventes ni redondees agresivamente un número que no se lee bien — en ese caso usa null. No agregues texto antes ni después del JSON, ni uses bloques de código.`;

function extractJson(text) {
  const cleaned = text.replace(/```json|```/g, '').trim();
  const match = cleaned.match(/\{[\s\S]*\}/);
  if (!match) return null;
  try { return JSON.parse(match[0]); } catch { return null; }
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: JSON.stringify({ ok: false, error: 'Método no permitido' }) };
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, body: JSON.stringify({ ok: false, error: 'Falta configurar ANTHROPIC_API_KEY en Netlify (Site settings → Environment variables).' }) };
  }

  let payload;
  try { payload = JSON.parse(event.body || '{}'); } catch {
    return { statusCode: 400, body: JSON.stringify({ ok: false, error: 'Body inválido' }) };
  }

  const { image, mediaType } = payload;
  if (!image || typeof image !== 'string') {
    return { statusCode: 400, body: JSON.stringify({ ok: false, error: 'Falta la imagen' }) };
  }
  // Base64 crece ~33% sobre el binario; 8MB de base64 ≈ 6MB de imagen real,
  // ya bastante holgado para una foto de celular comprimida en el cliente.
  if (image.length > 8 * 1024 * 1024) {
    return { statusCode: 413, body: JSON.stringify({ ok: false, error: 'La imagen es demasiado grande' }) };
  }
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  const type = allowedTypes.includes(mediaType) ? mediaType : 'image/jpeg';

  let anthropicRes;
  try {
    anthropicRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-5',
        max_tokens: 500,
        messages: [{
          role: 'user',
          content: [
            { type: 'image', source: { type: 'base64', media_type: type, data: image } },
            { type: 'text', text: PROMPT },
          ],
        }],
      }),
    });
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ ok: false, error: 'No se pudo contactar al servicio de lectura de fotos' }) };
  }

  if (!anthropicRes.ok) {
    const errText = await anthropicRes.text().catch(() => '');
    return { statusCode: 502, body: JSON.stringify({ ok: false, error: 'Error del servicio de lectura de fotos: ' + errText.slice(0, 200) }) };
  }

  const data = await anthropicRes.json();
  const text = (data.content || []).map(b => b.text || '').join('');
  const parsed = extractJson(text);
  if (!parsed) {
    return { statusCode: 502, body: JSON.stringify({ ok: false, error: 'No se pudo interpretar la respuesta del lector de fotos' }) };
  }

  // Sólo se devuelven las 8 claves esperadas, y sólo si son número o null —
  // nunca se reenvía texto libre del modelo hacia el cliente.
  const clean = {};
  FIELDS.forEach(k => {
    const v = parsed[k];
    clean[k] = (typeof v === 'number' && isFinite(v)) ? v : null;
  });

  return { statusCode: 200, body: JSON.stringify({ ok: true, data: clean }) };
};
