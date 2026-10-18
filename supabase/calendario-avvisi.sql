-- Riskly · avvisi push del calendario economico (strumenti.riskly.trade)
-- Ogni telefono/browser che attiva gli avvisi ha una riga: l'indirizzo push e i dati preferiti.
-- La tabella la leggono e scrivono solo le funzioni cal-iscrivi e cal-avvisi (chiave di servizio):
-- nessuna regola RLS per il pubblico.

create table if not exists public.cal_iscrizioni (
  endpoint   text primary key,
  p256dh     text not null,
  auth       text not null,
  preferiti  jsonb not null default '{}'::jsonb,   -- { id_evento: { d: data ISO, t: titolo, c: paese } }
  inviati    jsonb not null default '{}'::jsonb,   -- { "id:p" | "id:u": ms }  avvisi già mandati
  creato     timestamptz not null default now(),
  aggiornato timestamptz not null default now()
);
alter table public.cal_iscrizioni enable row level security;

-- controllo ogni minuto: chiama la funzione cal-avvisi
create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.unschedule('cal-avvisi') where exists (select 1 from cron.job where jobname = 'cal-avvisi');
select cron.schedule('cal-avvisi', '* * * * *', $$
  select net.http_post(
    url := 'https://swlztverwfgdgchgpudt.supabase.co/functions/v1/cal-avvisi',
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-cron', '<<CRON_SECRET>>'),
    body := '{}'::jsonb)
$$);
