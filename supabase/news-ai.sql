-- Riskly News · assistente AI (Gabriele, 3 novembre 2026): contatore delle domande al giorno per utente.
-- La tabella non è leggibile dal sito (RLS senza policy): la usa solo la funzione news-ai con la chiave di servizio.
create table if not exists public.news_ai_uso (
  utente uuid not null,
  giorno date not null default (now() at time zone 'Europe/Rome')::date,
  n int not null default 0,
  primary key (utente, giorno)
);
alter table public.news_ai_uso enable row level security;

create or replace function public.news_ai_conta(u uuid)
returns int
language sql
security definer
set search_path = public
as $$
  insert into public.news_ai_uso (utente, giorno, n) values (u, (now() at time zone 'Europe/Rome')::date, 1)
  on conflict (utente, giorno) do update set n = news_ai_uso.n + 1
  returning n;
$$;
revoke all on function public.news_ai_conta(uuid) from public, anon, authenticated;
grant execute on function public.news_ai_conta(uuid) to service_role;
