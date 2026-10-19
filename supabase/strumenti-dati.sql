-- Dati salvati di strumenti.riskly.trade (preferiti del calendario, filtri, valori dei calcolatori).
-- Una riga per utente; ognuno legge e scrive solo la sua.
create table if not exists public.strumenti_dati (
  utente uuid primary key references auth.users(id) on delete cascade,
  dati jsonb not null default '{}'::jsonb,
  aggiornato timestamptz not null default now()
);
alter table public.strumenti_dati enable row level security;
drop policy if exists "strumenti_dati_leggi" on public.strumenti_dati;
drop policy if exists "strumenti_dati_crea" on public.strumenti_dati;
drop policy if exists "strumenti_dati_modifica" on public.strumenti_dati;
create policy "strumenti_dati_leggi" on public.strumenti_dati for select to authenticated using (auth.uid() = utente);
create policy "strumenti_dati_crea" on public.strumenti_dati for insert to authenticated with check (auth.uid() = utente and pg_column_size(dati) < 200000);
create policy "strumenti_dati_modifica" on public.strumenti_dati for update to authenticated using (auth.uid() = utente) with check (auth.uid() = utente and pg_column_size(dati) < 200000);
grant select, insert, update on public.strumenti_dati to authenticated;
