-- Riskly: licenze dei bot venduti sul sito.
-- Da eseguire una volta nel SQL Editor di Supabase (Dashboard → SQL Editor → New query).
-- Si può rieseguire senza danni.
--
-- Come funziona
--   · Ogni cliente è una riga della tabella "licenze": numero di conto MetaTrader, quale
--     bot (o "tutti"), scadenza (vuota = per sempre), attiva sì/no.
--     La gestisci dal Table Editor di Supabase: aggiungi, modifica, disattiva.
--   · All'avvio e poi una volta al giorno il bot chiama licenza_verifica() con il suo
--     numero di conto. La risposta "OK:<firma>" è firmata con la chiave segreta, che
--     conoscono solo questo server e i bot: nessuno può falsificarla.
--   · La tabella e la chiave non si leggono dall'esterno: ci accede solo la funzione.
--
-- IMPORTANTE: la chiave segreta va scritta alla fine di questo file (punto 4), uguale a
-- LIC_SEGRETO in Riskly_Licenza.mqh. Non pubblicarla e non metterla su GitHub.


create extension if not exists pgcrypto with schema extensions;


-- 1. Clienti -------------------------------------------------------------------------

create table if not exists public.licenze (
  id               bigint generated always as identity primary key,
  conto            bigint  not null,                  -- numero del conto MetaTrader
  prodotto         text    not null default 'tutti',  -- tutti | risklypro | riskguard | trademanager | scalein | risklycopy
  cliente          text,
  email            text,
  scade            date,                              -- vuoto = licenza a vita
  attiva           boolean not null default true,     -- false = revocata
  nota             text,
  creata           timestamptz not null default now(),
  ultimo_controllo timestamptz,                       -- compilati dal bot
  broker           text,
  versione         text,
  controlli        integer not null default 0,
  constraint licenze_prodotto check (prodotto in
    ('tutti','risklypro','riskguard','trademanager','scalein','risklycopy'))
);

create index if not exists licenze_conto on public.licenze (conto);

alter table public.licenze enable row level security;
-- nessuna policy: dal sito e dai bot non si legge né si scrive, solo dalla Dashboard
revoke all on public.licenze from anon, authenticated;


-- 2. Chiave segreta (una riga sola, mai leggibile dall'esterno) ------------------------

create table if not exists public.licenze_segreto (
  id      integer primary key default 1 check (id = 1),
  segreto text not null
);

alter table public.licenze_segreto enable row level security;
revoke all on public.licenze_segreto from anon, authenticated;


-- 3. Verifica chiamata dai bot --------------------------------------------------------
-- Risposta: 'OK:' || sha256(prodotto|conto|AAAA.MM.GG|segreto)   (data in ora UTC)
--           'NO:motivo'

create or replace function public.licenza_verifica(p_prodotto text, p_conto bigint,
                                                   p_broker text default '', p_versione text default '')
returns text
language plpgsql volatile security definer set search_path = public, extensions
as $$
declare
  prod text := lower(coalesce(p_prodotto, ''));
  seg  text;
  l    public.licenze;
begin
  if p_conto is null or p_conto <= 0 or prod !~ '^[a-z]{3,20}$' then
    return 'NO:richiesta non valida';
  end if;

  select segreto into seg from public.licenze_segreto where id = 1;
  if seg is null or length(seg) < 20 or seg = 'METTI-QUI-LA-CHIAVE' then
    return 'NO:server licenze non configurato';
  end if;

  -- prima le licenze a vita, poi quella che scade più tardi
  select * into l from public.licenze
  where conto = p_conto and attiva and (prodotto = prod or prodotto = 'tutti')
  order by scade desc nulls first
  limit 1;

  if not found then
    return 'NO:nessuna licenza per il conto ' || p_conto;
  end if;

  if l.scade is not null and l.scade < (now() at time zone 'utc')::date then
    return 'NO:licenza scaduta il ' || to_char(l.scade, 'DD/MM/YYYY');
  end if;

  update public.licenze
  set ultimo_controllo = now(), broker = left(coalesce(p_broker, ''), 80),
      versione = left(coalesce(p_versione, ''), 40), controlli = controlli + 1
  where id = l.id;

  return 'OK:' || encode(digest(prod || '|' || p_conto::text || '|'
                                || to_char(now() at time zone 'utc', 'YYYY.MM.DD') || '|' || seg,
                                'sha256'), 'hex');
end;
$$;

revoke all on function public.licenza_verifica(text, bigint, text, text) from public;
grant execute on function public.licenza_verifica(text, bigint, text, text) to anon, authenticated;


-- 4. La tua chiave segreta ------------------------------------------------------------
-- Sostituisci METTI-QUI-LA-CHIAVE con la stessa chiave di LIC_SEGRETO, poi esegui.

-- (se la lasci così com'è non cambia nulla: la chiave già salvata resta)

insert into public.licenze_segreto (id, segreto)
select 1, v from (values ('METTI-QUI-LA-CHIAVE')) as t(v)
where v <> 'METTI-QUI-LA-CHIAVE'
on conflict (id) do update set segreto = excluded.segreto;
