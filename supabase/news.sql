-- Riskly News (news.riskly.trade), abbonamento a parte (Gabriele, 1° novembre 2026).
-- Titolo e sommario sono pubblici; l'articolo intero lo leggono solo gli abbonati a Riskly News
-- e chi ha il piano Premium del journal. Da eseguire una volta nell'editor SQL di Supabase.

-- ─── 1. Articoli ───────────────────────────────────────────────────
create table if not exists public.notizie (
  id          text primary key,                 -- AAAA-MM-GG-slug
  data        date not null,
  categoria   text not null check (categoria in ('oro', 'dollaro', 'fed', 'tassi', 'straordinarie', 'settimana')),
  titolo      text not null,
  sommario    text not null,
  corpo       jsonb not null default '[]'::jsonb,  -- paragrafi
  da_guardare jsonb not null default '[]'::jsonb,
  fonti       jsonb not null default '[]'::jsonb,  -- [{nome, url}]
  pubblicato  boolean not null default true,
  creato      timestamptz not null default now()
);
create index if not exists notizie_data on public.notizie (data desc);
alter table public.notizie enable row level security;

-- ─── 2. Chi può leggere l'articolo intero ──────────────────────────
-- abbonamento Riskly News attivo, oppure piano Premium del journal
-- senza argomenti: dice solo se chi è collegato ha accesso (nessuno può chiederlo per un altro utente)
create or replace function public.ha_news()
returns boolean
language sql stable
security definer
set search_path = public
as $$
  select auth.uid() is not null and (
    exists (select 1 from public.acquisti a
            where a.utente = auth.uid() and a.stato = 'attivo' and a.prodotto ilike 'Riskly News%')
    or exists (select 1 from public.profili p where p.id = auth.uid() and p.piano = 'premium')
  );
$$;
revoke all on function public.ha_news() from public;
grant execute on function public.ha_news() to authenticated;

drop policy if exists notizie_abbonati on public.notizie;
create policy notizie_abbonati on public.notizie
  for select to authenticated
  using (pubblicato and public.ha_news());
-- scrivono solo la service role (la routine degli articoli) e l'admin dalla dashboard: nessuna policy di scrittura

-- ─── 3. Anteprima pubblica: titolo e sommario per tutti ────────────
create or replace view public.notizie_anteprima as
  select id, data, categoria, titolo, sommario
  from public.notizie
  where pubblicato;
grant select on public.notizie_anteprima to anon, authenticated;

-- ─── 4. Abbonamenti: quale abbonamento Stripe è di quale acquisto ──
-- serve quando un abbonamento finisce: si chiude solo quello (News o journal), non l'altro
alter table public.acquisti add column if not exists stripe_abbonamento text;
create index if not exists acquisti_stripe_abbonamento on public.acquisti (stripe_abbonamento) where stripe_abbonamento is not null;
do $$
declare c record;
begin
  for c in
    select con.conname from pg_constraint con
    join pg_class rel on rel.oid = con.conrelid
    join pg_namespace ns on ns.oid = rel.relnamespace
    where ns.nspname = 'public' and rel.relname = 'acquisti'
      and con.contype = 'c' and pg_get_constraintdef(con.oid) ilike '%stato%'
  loop
    execute format('alter table public.acquisti drop constraint %I', c.conname);
  end loop;
end $$;
alter table public.acquisti add constraint acquisti_stato_check
  check (stato in ('in_attesa', 'attivo', 'rifiutato', 'scaduto')) not valid;
