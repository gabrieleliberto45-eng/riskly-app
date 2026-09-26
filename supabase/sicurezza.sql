-- ═══════════════════════════════════════════════════════════════════
--  Riskly · correzioni di sicurezza del database (Supabase)
--
--  Il database ha già la RLS attiva su tutte le tabelle e le policy
--  admin. Qui si chiudono solo le due falle trovate e si aggiunge la
--  consegna protetta del link Telegram. Si può rieseguire.
-- ═══════════════════════════════════════════════════════════════════


-- ─── 1. Acquisti: il cliente può creare solo ordini "in_attesa" ────
-- Prima bastava che l'ordine fosse suo: poteva crearlo già "attivo"
-- e sbloccare l'area clienti senza pagare.
drop policy if exists "crea i propri ordini" on public.acquisti;
create policy "crea i propri ordini" on public.acquisti
  for insert to authenticated
  with check (auth.uid() = utente and stato = 'in_attesa');


-- ─── 2. Profili: il cliente li legge ma non li modifica ────────────
-- Prima poteva cambiarsi piano e scadenza da solo (es. "premium").
-- Il profilo lo crea il trigger al_nuovo_utente → crea_profilo(),
-- il piano lo cambia solo l'admin ("admin aggiorna profili").
drop policy if exists "ognuno modifica il proprio profilo" on public.profili;
drop policy if exists "inserimento del proprio profilo" on public.profili;


-- ─── 3. Link del gruppo Telegram clienti ──────────────────────────
-- download.html lo chiede con sb.rpc('link_gruppo_clienti') e lo
-- riceve solo chi ha un acquisto attivo.
create table if not exists public.impostazioni_private (
  chiave text primary key,
  valore text not null
);
alter table public.impostazioni_private enable row level security;
-- nessuna policy: dal browser non si legge, solo tramite la funzione sotto

create or replace function public.link_gruppo_clienti()
returns text
language sql stable
security definer
set search_path = public
as $$
  select valore from public.impostazioni_private
  where chiave = 'telegram_clienti'
    and exists (
      select 1 from public.acquisti
      where utente = auth.uid() and stato = 'attivo'
    )
$$;

revoke all on function public.link_gruppo_clienti() from public, anon;
grant execute on function public.link_gruppo_clienti() to authenticated;

-- Il link (nuovo, con "richiesta di accesso" attiva) si inserisce così,
-- oppure dal Table Editor → impostazioni_private:
-- insert into public.impostazioni_private (chiave, valore)
-- values ('telegram_clienti', 'https://t.me/+NUOVO_LINK')
-- on conflict (chiave) do update set valore = excluded.valore;
