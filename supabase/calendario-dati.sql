-- Riskly · calendario economico sul database (15 novembre 2026, Gabriele: "approvo: metti online il calendario sul database")
-- Il calendario diventa una parte centrale dell'ecosistema: la funzione cal-aggiorna scarica i dati ogni minuto
-- e li salva qui; sito (Strumenti), Riskly News e i moduli futuri leggono da questa tabella, non dalla fonte.
-- Fonte principale: TradingView (lo stesso calendario di prima). Riserva automatica: biquote.io, se TradingView
-- non risponde per più di 30 minuti. In tabella c'è sempre UNA sola fonte alla volta (colonna fonte).
-- Le colonne hanno gli stessi nomi dei campi di TradingView, così il sito le usa senza conversioni.

create table if not exists public.cal_eventi (
  id          text primary key,
  date        timestamptz not null,
  country     text not null,          -- codice paese in minuscolo: us, eu, gb…
  currency    text,
  title       text not null,
  indicator   text,
  ticker      text,
  period      text,
  importance  smallint not null default 0,   -- 1 alta · 0 media · -1 bassa
  actual      double precision,
  forecast    double precision,
  previous    double precision,
  unit        text,
  scale       text,
  comment     text,
  source      text,
  source_url  text,
  fonte       text not null default 'tradingview',
  aggiornato  timestamptz not null default now()
);
create index if not exists cal_eventi_date on public.cal_eventi (date);
create index if not exists cal_eventi_country_date on public.cal_eventi (country, date);

alter table public.cal_eventi enable row level security;
drop policy if exists cal_eventi_leggi on public.cal_eventi;
create policy cal_eventi_leggi on public.cal_eventi for select to anon, authenticated using (true);
grant select on public.cal_eventi to anon, authenticated;

-- stato della copia: quale fonte è attiva, errori di fila, ultimo aggiornamento riuscito
create table if not exists public.cal_stato (
  id               smallint primary key default 1 check (id = 1),
  fonte            text not null default 'tradingview',
  errori_tv        int not null default 0,
  ultimo_ok        timestamptz,
  ultimo_largo     timestamptz,
  ultimo_errore    text,
  aggiornato       timestamptz not null default now()
);
insert into public.cal_stato (id) values (1) on conflict do nothing;
alter table public.cal_stato enable row level security;
drop policy if exists cal_stato_leggi on public.cal_stato;
create policy cal_stato_leggi on public.cal_stato for select to anon, authenticated using (true);
grant select on public.cal_stato to anon, authenticated;

-- ogni minuto: stessa intestazione segreta del job cal-avvisi, copiata dal job esistente
select cron.unschedule('cal-aggiorna') where exists (select 1 from cron.job where jobname = 'cal-aggiorna');
select cron.schedule('cal-aggiorna', '* * * * *', replace(command, '/functions/v1/cal-avvisi', '/functions/v1/cal-aggiorna'))
  from cron.job where jobname = 'cal-avvisi';
