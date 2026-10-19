-- Riskly: licenze collegate agli ordini del sito (da eseguire DOPO licenze.sql).
-- Da eseguire nel SQL Editor di Supabase. Si può rieseguire senza danni.
-- Non contiene la chiave segreta: quella resta quella salvata da licenze.sql.
--
-- Come funziona
--   · Il cliente compra dal sito: l'ordine entra in "acquisti" come in_attesa.
--   · Tu confermi il pagamento dalla pagina Gestione (stato = attivo).
--   · Il conto scritto dal cliente nell'ordine vale subito; altri conti li aggiunge lui
--     dal suo account (in tutto 2 per RiskGuard, TradeManager, ScaleIn; 3 per Riskly Pro e RisklyCopy).
--   · Il bot su quei conti si attiva da solo. Se rimetti l'ordine in attesa (rimborso),
--     la licenza sparisce da sola al controllo successivo.
--   · La tabella "licenze" (righe scritte a mano) continua a valere: per i tuoi conti,
--     per RisklyCopy, per prove a scadenza o casi particolari.


-- 1. Conti collegati a un acquisto ---------------------------------------------------

create table if not exists public.licenze_conti (
  id       bigint generated always as identity primary key,
  utente   uuid   not null references auth.users(id) on delete cascade,
  prodotto text   not null,          -- risklypro | riskguard | trademanager | scalein
  conto    bigint not null check (conto > 0),
  creato   timestamptz not null default now(),
  unique (prodotto, conto)           -- un conto non si registra due volte per lo stesso bot
);

alter table public.licenze_conti enable row level security;
revoke all on public.licenze_conti from anon, authenticated;   -- solo dalle funzioni qui sotto


-- 2. Funzioni di supporto -----------------------------------------------------------

-- "Riskly Pro" -> "risklypro", "RiskGuard" -> "riskguard"
create or replace function public.licenza_codice(nome text)
returns text language sql immutable
as $$ select lower(regexp_replace(coalesce(nome, ''), '[^A-Za-z]', '', 'g')) $$;

-- quanti conti per acquisto
create or replace function public.licenza_max_conti(prod text)
returns integer language sql immutable
as $$ select case when prod in ('risklypro', 'risklycopy') then 3 else 2 end $$;   -- RisklyCopy: 1 principale + 2 copie

-- l'admin del sito (stessa email di ADMIN in index.html)
create or replace function public.licenza_admin()
returns boolean language sql stable
as $$ select lower(coalesce(auth.jwt() ->> 'email', '')) in ('gabrieleliberto1212@gmail.com') $$;


-- 3. Per il cliente: i suoi conti, aggiungere un conto --------------------------------

-- i conti scritti negli ordini confermati del cliente (campo "conto" di acquisti)
create or replace function public.licenza_conti_ordini(p_utente uuid)
returns table (prodotto text, conto bigint, creato timestamptz)
language sql stable security definer set search_path = public
as $$
  select distinct on (public.licenza_codice(a.prodotto), d.n)
         public.licenza_codice(a.prodotto), d.n::bigint, a.creato
  from public.acquisti a
  cross join lateral (select regexp_replace(coalesce(a.conto::text, ''), '[^0-9]', '', 'g') as n) d
  where a.utente = p_utente and a.stato = 'attivo' and d.n <> '' and length(d.n) <= 11
$$;

revoke all on function public.licenza_conti_ordini(uuid) from public, anon, authenticated;

create or replace function public.licenza_miei_conti()
returns table (prodotto text, conto bigint, creato timestamptz)
language sql stable security definer set search_path = public
as $$
  select x.prodotto, x.conto, min(x.creato) from (
    select c.prodotto, c.conto, c.creato from public.licenze_conti c where c.utente = auth.uid()
    union all
    select o.prodotto, o.conto, o.creato from public.licenza_conti_ordini(auth.uid()) o
  ) x
  group by x.prodotto, x.conto
  order by 3
$$;

create or replace function public.licenza_aggiungi_conto(p_prodotto text, p_conto bigint)
returns text
language plpgsql volatile security definer set search_path = public
as $$
declare
  prod text := public.licenza_codice(p_prodotto);
  n    integer;
begin
  if auth.uid() is null then
    raise exception 'accesso richiesto' using errcode = '28000';
  end if;
  if p_conto is null or p_conto <= 0 or p_conto > 99999999999 then
    return 'Numero di conto non valido';
  end if;
  if not exists (select 1 from public.acquisti a
                 where a.utente = auth.uid() and a.stato = 'attivo'
                   and public.licenza_codice(a.prodotto) = prod) then
    return 'Nessun acquisto confermato per questo bot';
  end if;
  if exists (select 1 from public.licenza_conti_ordini(auth.uid()) o where o.prodotto = prod and o.conto = p_conto) then
    return 'Conto già collegato';
  end if;
  if exists (select 1 from public.licenze_conti where prodotto = prod and conto = p_conto) then
    return case when exists (select 1 from public.licenze_conti
                             where prodotto = prod and conto = p_conto and utente = auth.uid())
                then 'Conto già collegato'
                else 'Questo conto è già collegato a un altro account: scrivi al supporto' end;
  end if;
  select count(*) into n from public.licenza_miei_conti() m where m.prodotto = prod;
  if n >= public.licenza_max_conti(prod) then
    return 'Hai già collegato ' || n || ' conti: per cambiarne uno scrivi al supporto';
  end if;

  insert into public.licenze_conti (utente, prodotto, conto) values (auth.uid(), prod, p_conto);
  return 'OK';
end;
$$;

revoke all on function public.licenza_miei_conti() from public, anon;
revoke all on function public.licenza_aggiungi_conto(text, bigint) from public, anon;
grant execute on function public.licenza_miei_conti() to authenticated;
grant execute on function public.licenza_aggiungi_conto(text, bigint) to authenticated;


-- 4. Per te (pagina Gestione): vedere e togliere i conti dei clienti -------------------

create or replace function public.licenza_admin_conti()
returns table (id bigint, utente uuid, prodotto text, conto bigint, creato timestamptz)
language plpgsql stable security definer set search_path = public
as $$
begin
  if not public.licenza_admin() then
    raise exception 'solo admin' using errcode = '42501';
  end if;
  return query select c.id, c.utente, c.prodotto, c.conto, c.creato
               from public.licenze_conti c order by c.creato desc;
end;
$$;

create or replace function public.licenza_admin_rimuovi(p_id bigint)
returns void
language plpgsql volatile security definer set search_path = public
as $$
begin
  if not public.licenza_admin() then
    raise exception 'solo admin' using errcode = '42501';
  end if;
  delete from public.licenze_conti where id = p_id;
end;
$$;

revoke all on function public.licenza_admin_conti() from public, anon;
revoke all on function public.licenza_admin_rimuovi(bigint) from public, anon;
grant execute on function public.licenza_admin_conti() to authenticated;
grant execute on function public.licenza_admin_rimuovi(bigint) to authenticated;


-- 5. Verifica chiamata dai bot (sostituisce quella di licenze.sql) ---------------------
-- Valida se: c'è una riga attiva in "licenze" (a mano), oppure il conto è collegato a un
-- acquisto confermato di quel bot. Risposta firmata come prima.

create or replace function public.licenza_verifica(p_prodotto text, p_conto bigint,
                                                   p_broker text default '', p_versione text default '')
returns text
language plpgsql volatile security definer set search_path = public, extensions
as $$
declare
  prod text := lower(coalesce(p_prodotto, ''));
  seg  text;
  l    public.licenze;
  ok   boolean := false;
begin
  if p_conto is null or p_conto <= 0 or prod !~ '^[a-z]{3,20}$' then
    return 'NO:richiesta non valida';
  end if;

  select segreto into seg from public.licenze_segreto where id = 1;
  if seg is null or length(seg) < 20 or seg = 'METTI-QUI-LA-CHIAVE' then
    return 'NO:server licenze non configurato';
  end if;

  -- a) licenza scritta a mano
  select * into l from public.licenze
  where conto = p_conto and attiva and (prodotto = prod or prodotto = 'tutti')
  order by scade desc nulls first
  limit 1;

  if found then
    if l.scade is not null and l.scade < (now() at time zone 'utc')::date then
      if not exists (select 1 from public.licenze_conti c where c.conto = p_conto and c.prodotto = prod) then
        return 'NO:licenza scaduta il ' || to_char(l.scade, 'DD/MM/YYYY');
      end if;
    else
      ok := true;
      update public.licenze
      set ultimo_controllo = now(), broker = left(coalesce(p_broker, ''), 80),
          versione = left(coalesce(p_versione, ''), 40), controlli = controlli + 1
      where id = l.id;
    end if;
  end if;

  -- b) conto collegato a un acquisto confermato
  if not ok then
    ok := exists (
      select 1 from public.licenze_conti c
      join public.acquisti a on a.utente = c.utente
      where c.conto = p_conto and c.prodotto = prod
        and a.stato = 'attivo' and public.licenza_codice(a.prodotto) = prod);
  end if;

  -- c) conto scritto dal cliente nell'ordine stesso (campo "conto" di acquisti)
  if not ok then
    ok := exists (
      select 1 from public.acquisti a
      where a.stato = 'attivo' and public.licenza_codice(a.prodotto) = prod
        and regexp_replace(coalesce(a.conto::text, ''), '[^0-9]', '', 'g') = p_conto::text);
  end if;

  if not ok then
    return 'NO:nessuna licenza per il conto ' || p_conto;
  end if;

  return 'OK:' || encode(digest(prod || '|' || p_conto::text || '|'
                                || to_char(now() at time zone 'utc', 'YYYY.MM.DD') || '|' || seg,
                                'sha256'), 'hex');
end;
$$;

revoke all on function public.licenza_verifica(text, bigint, text, text) from public;
grant execute on function public.licenza_verifica(text, bigint, text, text) to anon, authenticated;
