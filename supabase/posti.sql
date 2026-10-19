-- ═══════════════════════════════════════════════════════════════════
--  Riskly · conteggio automatico dei posti al prezzo di lancio dei bot
--
--  Il sito chiede sb.rpc('posti_venduti') e mostra "N posti disponibili su 10".
--  Conta solo gli acquisti di bot confermati da Stripe, esclusi gli acquisti di prova
--  di Gabriele. Restituisce SOLO un numero: nessun dato dei clienti esce dal database.
--  Si può rieseguire.
-- ═══════════════════════════════════════════════════════════════════
create or replace function public.posti_venduti()
returns integer
language sql stable
security definer
set search_path = public
as $$
  select count(*)::integer
  from public.acquisti a
  left join auth.users u on u.id = a.utente
  where a.stato = 'attivo'
    and a.prodotto in ('RiskGuard', 'TradeManager', 'ScaleIn', 'Riskly Pro', 'RisklyCopy')
    and lower(coalesce(u.email, '')) not in ('gabrieleliberto1212@gmail.com', 'gabrieleliberto45@gmail.com')
$$;

revoke all on function public.posti_venduti() from public;
grant execute on function public.posti_venduti() to anon, authenticated;
