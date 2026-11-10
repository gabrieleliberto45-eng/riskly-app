// Carica una copertina di Riskly News nell'archivio pubblico "copertine" (così non serve un deploy Netlify per ogni articolo).
// Chiamata: POST {id, jpg: <base64>} con header x-token = valore di config_interna.token_copertine (tabella senza accesso pubblico).
import { createClient } from 'npm:@supabase/supabase-js@2';
Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('POST', { status: 405 });
  const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  const { data } = await sb.from('config_interna').select('valore').eq('chiave', 'token_copertine').maybeSingle();
  if (!data || (req.headers.get('x-token') ?? '') !== data.valore) return new Response('non autorizzato', { status: 403 });
  let b: { id?: string; jpg?: string };
  try { b = await req.json(); } catch { return new Response('json', { status: 400 }); }
  if (!b.id || !/^[a-z0-9-]{3,80}$/.test(b.id) || !b.jpg) return new Response('dati', { status: 400 });
  const bytes = Uint8Array.from(atob(b.jpg), (c) => c.charCodeAt(0));
  if (bytes.length > 3_000_000 || bytes[0] !== 0xff || bytes[1] !== 0xd8) return new Response('non è un jpg valido', { status: 400 });
  const { error } = await sb.storage.from('copertine').upload(`${b.id}.jpg`, bytes, { contentType: 'image/jpeg', upsert: true });
  if (error) return new Response(error.message, { status: 500 });
  return Response.json({ url: `${Deno.env.get('SUPABASE_URL')}/storage/v1/object/public/copertine/${b.id}.jpg` });
});
