-- Bot di supporto Telegram: quale messaggio inoltrato a Gabriele appartiene a quale cliente.
-- Le scrive e le legge solo la funzione tg-supporto (chiave di servizio): nessuna policy pubblica.
create table if not exists public.tg_supporto_msg (
  admin_msg bigint primary key,
  utente_chat bigint not null,
  creato timestamptz not null default now()
);
create table if not exists public.tg_supporto_utenti (
  chat bigint primary key,
  ultima_conferma timestamptz not null default now()
);
alter table public.tg_supporto_msg enable row level security;
alter table public.tg_supporto_utenti enable row level security;
