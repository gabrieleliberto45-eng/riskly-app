-- Riskly: da eseguire UNA volta nel SQL Editor di Supabase (tutto insieme).
-- 1) pannello Gestione dell'admin  2) collegamento tra bot e journal.
-- Si può rieseguire senza danni.

create or replace function public.e_admin() returns boolean
  language sql stable security definer set search_path = public
as $$
  select lower(coalesce(auth.jwt() ->> 'email', '')) = 'gabrieleliberto1212@gmail.com'
$$;

-- l'admin vede e modifica tutti i profili
drop policy if exists "profili: admin legge tutti" on public.profili;
create policy "profili: admin legge tutti" on public.profili
  for select to authenticated
  using (public.e_admin());

drop policy if exists "profili: admin modifica tutti" on public.profili;
create policy "profili: admin modifica tutti" on public.profili
  for update to authenticated
  using (public.e_admin())
  with check (public.e_admin());

-- il permesso di modifica torna com'era; piano e scadenza li protegge il controllo qui sotto
grant update on public.profili to authenticated;

create or replace function public.proteggi_piano() returns trigger
  language plpgsql security definer set search_path = public
as $$
begin
  if (new.piano is distinct from old.piano or new.scadenza is distinct from old.scadenza)
     and auth.role() = 'authenticated' and not public.e_admin() then
    raise exception 'Solo l''amministratore può cambiare piano e scadenza';
  end if;
  return new;
end
$$;

drop trigger if exists proteggi_piano on public.profili;
create trigger proteggi_piano before update on public.profili
  for each row execute function public.proteggi_piano();


-- 1. Operazioni: da dove arrivano ---------------------------------------------------

alter table public.operazioni add column if not exists fonte text not null default 'manuale';
alter table public.operazioni add column if not exists bot_dettagli jsonb;


-- 2. Chiave del bot e impostazioni scelte nel journal --------------------------------

create table if not exists public.bot_chiavi (
  utente       uuid primary key references auth.users(id) on delete cascade,
  chiave       text not null unique,
  impostazioni jsonb not null default '{}'::jsonb,
  creata       timestamptz not null default now()
);

alter table public.bot_chiavi enable row level security;

drop policy if exists "bot_chiavi: lettura propria" on public.bot_chiavi;
create policy "bot_chiavi: lettura propria" on public.bot_chiavi
  for select to authenticated
  using (auth.uid() = utente);

drop policy if exists "bot_chiavi: modifica propria" on public.bot_chiavi;
create policy "bot_chiavi: modifica propria" on public.bot_chiavi
  for update to authenticated
  using (auth.uid() = utente)
  with check (auth.uid() = utente);

drop policy if exists "bot_chiavi: cancellazione propria" on public.bot_chiavi;
create policy "bot_chiavi: cancellazione propria" on public.bot_chiavi
  for delete to authenticated
  using (auth.uid() = utente);

-- dal browser si cambiano solo le impostazioni; la chiave la genera bot_nuova_chiave()
revoke insert, update on public.bot_chiavi from authenticated, anon;
grant select, delete on public.bot_chiavi to authenticated;
grant update (impostazioni) on public.bot_chiavi to authenticated;


-- 3. Operazioni già ricevute: non si importano due volte ----------------------------

create table if not exists public.bot_ricevute (
  utente   uuid not null references auth.users(id) on delete cascade,
  conto    bigint not null,
  ticket   bigint not null,
  ricevuta timestamptz not null default now(),
  primary key (utente, conto, ticket)
);

alter table public.bot_ricevute enable row level security;
-- nessuna policy: ci scrivono solo le funzioni qui sotto
revoke all on public.bot_ricevute from authenticated, anon;


-- 4. Stato dei bot, per vederlo dal telefono ----------------------------------------

create table if not exists public.bot_stato (
  utente     uuid not null references auth.users(id) on delete cascade,
  conto      bigint not null,
  bot        text not null,
  dati       jsonb not null,
  aggiornato timestamptz not null default now(),
  primary key (utente, conto, bot)
);

alter table public.bot_stato enable row level security;

drop policy if exists "bot_stato: lettura propria" on public.bot_stato;
create policy "bot_stato: lettura propria" on public.bot_stato
  for select to authenticated
  using (auth.uid() = utente);

drop policy if exists "bot_stato: cancellazione propria" on public.bot_stato;
create policy "bot_stato: cancellazione propria" on public.bot_stato
  for delete to authenticated
  using (auth.uid() = utente);

revoke insert, update on public.bot_stato from authenticated, anon;
grant select, delete on public.bot_stato to authenticated;


-- 5. Funzioni ------------------------------------------------------------------------

-- a chi appartiene una chiave (null se non esiste)
create or replace function public.bot_proprietario(p_chiave text)
returns uuid
language sql stable security definer set search_path = public
as $$
  select utente from public.bot_chiavi
  where p_chiave is not null and length(p_chiave) >= 32 and chiave = p_chiave;
$$;

revoke all on function public.bot_proprietario(text) from public, anon, authenticated;


-- dal journal: crea o rigenera la chiave dell'utente connesso
create or replace function public.bot_nuova_chiave()
returns text
language plpgsql volatile security definer set search_path = public
as $$
declare
  nuova text := replace(gen_random_uuid()::text, '-', '') || replace(gen_random_uuid()::text, '-', '');
begin
  if auth.uid() is null then
    raise exception 'accesso richiesto' using errcode = '28000';
  end if;

  insert into public.bot_chiavi (utente, chiave)
  values (auth.uid(), nuova)
  on conflict (utente) do update set chiave = excluded.chiave, creata = now();

  return nuova;
end;
$$;

revoke all on function public.bot_nuova_chiave() from public, anon;
grant execute on function public.bot_nuova_chiave() to authenticated;


-- dal bot: le impostazioni scelte nel journal
create or replace function public.bot_impostazioni(p_chiave text)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  u   uuid := public.bot_proprietario(p_chiave);
  imp jsonb;
begin
  if u is null then
    raise exception 'chiave non valida' using errcode = '28000';
  end if;
  select impostazioni into imp from public.bot_chiavi where utente = u;
  return coalesce(imp, '{}'::jsonb);
end;
$$;

revoke all on function public.bot_impostazioni(text) from public;
grant execute on function public.bot_impostazioni(text) to anon, authenticated;


-- dal bot: registra le operazioni chiuse. Restituisce quante sono state aggiunte.
-- Ogni elemento: {ticket, data "AAAA-MM-GG", ora "HH:MM", simbolo, direzione "long"|"short",
--                 pnl, rischio, nota, dettagli {...}}
create or replace function public.bot_invia_operazioni(p_chiave text, p_conto bigint, p_operazioni jsonb)
returns integer
language plpgsql volatile security definer set search_path = public
as $$
declare
  u         uuid := public.bot_proprietario(p_chiave);
  imp       jsonb;
  o         jsonb;
  aggiunte  integer := 0;
  strategia text;
  emozione  text;
  conNota   boolean;
  simboli   text;
begin
  if u is null then
    raise exception 'chiave non valida' using errcode = '28000';
  end if;
  if p_conto is null or p_operazioni is null or jsonb_typeof(p_operazioni) <> 'array' then
    raise exception 'dati non validi' using errcode = '22023';
  end if;
  if jsonb_array_length(p_operazioni) > 200 then
    raise exception 'troppe operazioni in un solo invio' using errcode = '22023';
  end if;

  select impostazioni into imp from public.bot_chiavi where utente = u;
  imp       := coalesce(imp, '{}'::jsonb);
  strategia := left(coalesce(imp->>'strategia', ''), 60);
  emozione  := coalesce(nullif(imp->>'emozione', ''), 'lucido');
  conNota   := coalesce((imp->>'nota_auto')::boolean, true);
  simboli   := upper(coalesce(imp->>'simboli', ''));   -- vuoto = tutti

  for o in select * from jsonb_array_elements(p_operazioni)
  loop
    continue when (o->>'ticket') is null or (o->>'data') is null;

    -- importazione sospesa dal journal
    continue when coalesce((imp->>'importa')::boolean, true) = false;

    -- solo i simboli scelti nel journal (lista separata da virgole)
    continue when simboli <> '' and not (upper(o->>'simbolo') = any (
      select trim(s) from unnest(string_to_array(simboli, ',')) as s));

    insert into public.bot_ricevute (utente, conto, ticket)
    values (u, p_conto, (o->>'ticket')::bigint)
    on conflict do nothing;

    continue when not found;     -- già arrivata in passato (anche se poi cancellata)

    -- jsonb_populate_record converte ogni valore nel tipo della colonna
    insert into public.operazioni
      (utente, data, ora, simbolo, direzione, pnl, rischio, strategia, emozione, nota, fonte, bot_dettagli)
    select r.utente, r.data, r.ora, r.simbolo, r.direzione, r.pnl, r.rischio,
           r.strategia, r.emozione, r.nota, r.fonte, r.bot_dettagli
    from jsonb_populate_record(null::public.operazioni, jsonb_build_object(
      'utente',       u,
      'data',         o->>'data',
      'ora',          coalesce(nullif(o->>'ora', ''), '00:00'),
      'simbolo',      upper(left(coalesce(o->>'simbolo', ''), 30)),
      'direzione',    case when o->>'direzione' = 'short' then 'short' else 'long' end,
      'pnl',          coalesce((o->>'pnl')::numeric, 0),
      'rischio',      greatest(coalesce((o->>'rischio')::numeric, 0), 0),
      'strategia',    strategia,
      'emozione',     emozione,
      'nota',         case when conNota then left(coalesce(o->>'nota', ''), 500) else '' end,
      'fonte',        'bot',
      'bot_dettagli', coalesce(o->'dettagli', '{}'::jsonb) || jsonb_build_object('conto', p_conto)
    )) as r;

    aggiunte := aggiunte + 1;
  end loop;

  return aggiunte;
end;
$$;

revoke all on function public.bot_invia_operazioni(text, bigint, jsonb) from public;
grant execute on function public.bot_invia_operazioni(text, bigint, jsonb) to anon, authenticated;


-- dal bot: aggiorna il proprio stato
create or replace function public.bot_aggiorna_stato(p_chiave text, p_conto bigint, p_bot text, p_dati jsonb)
returns void
language plpgsql volatile security definer set search_path = public
as $$
declare
  u uuid := public.bot_proprietario(p_chiave);
begin
  if u is null then
    raise exception 'chiave non valida' using errcode = '28000';
  end if;
  if p_conto is null or p_bot is null or length(p_bot) > 40
     or p_dati is null or pg_column_size(p_dati) > 8000 then
    raise exception 'dati non validi' using errcode = '22023';
  end if;

  insert into public.bot_stato (utente, conto, bot, dati, aggiornato)
  values (u, p_conto, p_bot, p_dati, now())
  on conflict (utente, conto, bot) do update set dati = excluded.dati, aggiornato = now();
end;
$$;

revoke all on function public.bot_aggiorna_stato(text, bigint, text, jsonb) from public;
grant execute on function public.bot_aggiorna_stato(text, bigint, text, jsonb) to anon, authenticated;
