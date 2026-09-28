-- ═══════════════════════════════════════════════════════════════════
--  Riskly · conteggio automatico dei posti al prezzo di lancio
--
--  Il sito chiede sb.rpc('posti_venduti') e mostra "N posti disponibili su 10".
--  La funzione restituisce SOLO un numero (quanti ordini confermati ci sono):
--  nessun dato dei clienti esce dal database. Si può rieseguire.
-- ═══════════════════════════════════════════════════════════════════
create or replace function public.posti_venduti()
returns integer
language sql stable
security definer
set search_path = public
as $$
  select count(*)::integer from public.acquisti where stato = 'attivo'
$$;

revoke all on function public.posti_venduti() from public;
grant execute on function public.posti_venduti() to anon, authenticated;
