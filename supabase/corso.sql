-- ═══════════════════════════════════════════════════════════════════
--  Riskly · consegna del videocorso (gruppo Telegram del corso)
--
--  download.html chiede sb.rpc('link_gruppo_corso'): il link arriva solo
--  a chi ha un acquisto "Videocorso" confermato (stato = 'attivo').
--  Usa la tabella impostazioni_private creata da sicurezza.sql.
--  Si può rieseguire.
-- ═══════════════════════════════════════════════════════════════════

create or replace function public.link_gruppo_corso()
returns text
language sql stable
security definer
set search_path = public
as $$
  select valore from public.impostazioni_private
  where chiave = 'telegram_corso'
    and exists (
      select 1 from public.acquisti
      where utente = auth.uid() and stato = 'attivo' and prodotto ilike '%corso%'
    )
$$;

revoke all on function public.link_gruppo_corso() from public, anon;
grant execute on function public.link_gruppo_corso() to authenticated;

-- Il link d'invito del gruppo "Riskly corso", creato su Telegram con
-- "Richiedi l'approvazione dell'amministratore" attivo:
-- insert into public.impostazioni_private (chiave, valore)
-- values ('telegram_corso', 'https://t.me/+LINK_DEL_CORSO')
-- on conflict (chiave) do update set valore = excluded.valore;
