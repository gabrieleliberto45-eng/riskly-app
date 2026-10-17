-- ═══════════════════════════════════════════════════════════════════
--  Riskly · consegna dei due corsi e del pacchetto. Si può rieseguire.
--
--  Prodotti (colonna acquisti.prodotto):
--    'Videocorso'                  → gruppo Telegram del corso di rischio
--    'Corso Analisi fondamentale'  → gruppo Telegram dell'analisi fondamentale
--    'Pacchetto corsi'             → tutti e due i gruppi
--  download.html chiede i link con sb.rpc(...): arrivano solo a chi ha l'acquisto attivo.
-- ═══════════════════════════════════════════════════════════════════

-- corso di rischio: Videocorso o Pacchetto (non più "qualsiasi prodotto con corso nel nome")
create or replace function public.link_gruppo_corso()
returns text language sql stable security definer set search_path = public as $$
  select valore from public.impostazioni_private
  where chiave = 'telegram_corso'
    and exists (select 1 from public.acquisti where utente = auth.uid() and stato = 'attivo'
                and (prodotto = 'Videocorso' or prodotto = 'Pacchetto corsi'))
$$;
revoke all on function public.link_gruppo_corso() from public, anon;
grant execute on function public.link_gruppo_corso() to authenticated;

-- analisi fondamentale: corso singolo o Pacchetto
create or replace function public.link_gruppo_fondamentale()
returns text language sql stable security definer set search_path = public as $$
  select valore from public.impostazioni_private
  where chiave = 'telegram_fondamentale'
    and exists (select 1 from public.acquisti where utente = auth.uid() and stato = 'attivo'
                and (prodotto = 'Corso Analisi fondamentale' or prodotto = 'Pacchetto corsi'))
$$;
revoke all on function public.link_gruppo_fondamentale() from public, anon;
grant execute on function public.link_gruppo_fondamentale() to authenticated;

-- il codice sconto del videocorso resta solo per chi ha comprato un software (non per corsi o pacchetto)
create or replace function public.codice_sconto_corso()
returns text language sql stable security definer set search_path = public as $$
  select valore from public.impostazioni_private
  where chiave = 'codice_corso'
    and exists (select 1 from public.acquisti where utente = auth.uid() and stato = 'attivo'
                and prodotto !~* 'corso' and prodotto !~* 'pacchetto' and prodotto !~* '^journal')
$$;
revoke all on function public.codice_sconto_corso() from public, anon;
grant execute on function public.codice_sconto_corso() to authenticated;

-- il link d'invito del gruppo "Riskly · Analisi fondamentale" (con approvazione dell'amministratore):
-- NON scriverlo qui nel repository. Si esegue a parte nel SQL Editor:
-- insert into public.impostazioni_private (chiave, valore)
-- values ('telegram_fondamentale', 'https://t.me/+LINK')
-- on conflict (chiave) do update set valore = excluded.valore;
