-- ═══════════════════════════════════════════════════════════════════
--  Riskly · regole di sicurezza del database (Supabase)
--
--  Il sito controlla chi è admin solo nel browser: la protezione vera
--  dei dati sono queste regole (Row Level Security). Senza, chiunque
--  apra la console del browser può leggere la lista d'attesa o
--  segnare come "attivo" un ordine mai pagato.
--
--  Come si usa: Supabase → SQL Editor → incolla tutto → Run.
--  Si può rieseguire: ogni volta riparte da zero sulle tabelle sotto.
--
--  ATTENZIONE: cancella TUTTE le policy già presenti su queste tabelle
--  e le sostituisce con quelle qui sotto.
-- ═══════════════════════════════════════════════════════════════════


-- ─── 1. Chi è admin ───────────────────────────────────────────────
-- Stessa email della costante ADMIN in index.html.
-- Funziona solo se su Supabase è attiva la conferma dell'email
-- (Authentication → Providers → Email → "Confirm email").
create or replace function public.is_admin()
returns boolean
language sql stable
as $$
  select lower(coalesce(auth.jwt() ->> 'email', '')) in ('gabrieleliberto1212@gmail.com')
$$;


-- ─── 2. Via le policy vecchie ─────────────────────────────────────
do $$
declare r record;
begin
  for r in
    select policyname, tablename from pg_policies
    where schemaname = 'public'
      and tablename in ('lista_attesa','visite','acquisti','profili','operazioni')
  loop
    execute format('drop policy %I on public.%I', r.policyname, r.tablename);
  end loop;
end $$;

alter table public.lista_attesa enable row level security;
alter table public.visite       enable row level security;
alter table public.acquisti     enable row level security;
alter table public.profili      enable row level security;
alter table public.operazioni   enable row level security;


-- ─── 3. Lista d'attesa: tutti si iscrivono, solo l'admin legge ─────
create policy "iscrizione aperta" on public.lista_attesa
  for insert to anon, authenticated with check (true);
create policy "admin legge" on public.lista_attesa
  for select to authenticated using (public.is_admin());
create policy "admin cancella" on public.lista_attesa
  for delete to authenticated using (public.is_admin());


-- ─── 4. Visite: tutti le registrano, solo l'admin le vede ─────────
create policy "visita aperta" on public.visite
  for insert to anon, authenticated with check (true);
create policy "admin legge" on public.visite
  for select to authenticated using (public.is_admin());


-- ─── 5. Acquisti ──────────────────────────────────────────────────
-- Il cliente vede i suoi e può solo crearne di nuovi "in_attesa".
-- Solo l'admin li conferma (stato = 'attivo').
create policy "cliente legge i suoi" on public.acquisti
  for select to authenticated using (utente = auth.uid() or public.is_admin());
create policy "cliente crea in attesa" on public.acquisti
  for insert to authenticated with check (utente = auth.uid() and stato = 'in_attesa');
create policy "admin aggiorna" on public.acquisti
  for update to authenticated using (public.is_admin()) with check (public.is_admin());


-- ─── 6. Profili ───────────────────────────────────────────────────
-- Il cliente legge il suo profilo ma non lo modifica:
-- altrimenti potrebbe cambiarsi il piano da "prova" a "premium" da solo.
create policy "cliente legge il suo" on public.profili
  for select to authenticated using (id = auth.uid() or public.is_admin());
create policy "admin aggiorna" on public.profili
  for update to authenticated using (public.is_admin()) with check (public.is_admin());


-- ─── 7. Operazioni del journal: ognuno solo le sue ────────────────
create policy "proprie operazioni" on public.operazioni
  for all to authenticated
  using (utente = auth.uid()) with check (utente = auth.uid());


-- ─── 8. Link del gruppo Telegram clienti ──────────────────────────
-- Il link sta qui, non nel codice del sito: download.html lo chiede
-- con sb.rpc('link_gruppo_clienti') e lo riceve solo chi ha un
-- acquisto attivo.
create table if not exists public.impostazioni_private (
  chiave text primary key,
  valore text not null
);
alter table public.impostazioni_private enable row level security;
-- nessuna policy: dal browser non si legge, solo tramite la funzione sotto

-- Incolla qui il link di invito (meglio un link NUOVO, con "richiesta di accesso"
-- attiva, e revoca quello vecchio che è stato pubblico nel codice del sito).
insert into public.impostazioni_private (chiave, valore)
values ('telegram_clienti', 'https://t.me/+INCOLLA_QUI_IL_NUOVO_LINK')
on conflict (chiave) do update set valore = excluded.valore;

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
