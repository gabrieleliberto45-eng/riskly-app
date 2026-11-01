-- Riskly News · notifiche quando esce un articolo (Gabriele, 1° novembre 2026)
-- Ogni browser/telefono che attiva le notifiche su news.riskly.trade ha una riga.
-- La tabella la usano solo le funzioni news-iscrivi e news-avvisi (chiave di servizio): nessuna regola per il pubblico.
create table if not exists public.news_iscrizioni (
  endpoint text primary key,
  p256dh   text not null,
  auth     text not null,
  creato   timestamptz not null default now()
);
alter table public.news_iscrizioni enable row level security;

-- quando un articolo ha già mandato la notifica (così non la manda due volte, nemmeno dopo un aggiornamento)
alter table public.notizie add column if not exists avvisato timestamptz;
update public.notizie set avvisato = coalesce(avvisato, creato);   -- gli articoli già usciti non avvisano

create extension if not exists pg_net;
create or replace function public.notizie_avvisa()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if new.pubblicato and new.avvisato is null then
    perform net.http_post(
      url := 'https://swlztverwfgdgchgpudt.supabase.co/functions/v1/news-avvisi',
      body := jsonb_build_object('id', new.id),
      headers := jsonb_build_object('Content-Type', 'application/json'));
  end if;
  return new;
end $$;
drop trigger if exists notizie_avvisa on public.notizie;
create trigger notizie_avvisa after insert or update of pubblicato on public.notizie
  for each row execute function public.notizie_avvisa();
