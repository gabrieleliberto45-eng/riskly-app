-- Riskly: scollegare un conto MetaTrader dal journal.
-- Da eseguire UNA volta nel SQL Editor di Supabase (Dashboard -> SQL Editor -> New query), dopo bot.sql.
-- Si puo' rieseguire senza danni.
--
-- Nel journal ogni riquadro "I tuoi bot" ha il pulsante "Scollega": il conto finisce in bot_scollegati,
-- il suo stato sparisce e da quel momento il bot di quel conto non manda piu' ne' stato ne' operazioni,
-- anche se resta acceso con la stessa chiave. Gli altri conti restano collegati.
-- Per ricollegarlo: "Collega i tuoi bot" -> "Conti scollegati" -> "Ricollega".

create table if not exists public.bot_scollegati (
  utente     uuid not null references auth.users(id) on delete cascade,
  conto      bigint not null,
  scollegato timestamptz not null default now(),
  primary key (utente, conto)
);

alter table public.bot_scollegati enable row level security;

drop policy if exists "bot_scollegati: lettura propria" on public.bot_scollegati;
create policy "bot_scollegati: lettura propria" on public.bot_scollegati
  for select to authenticated
  using (auth.uid() = utente);

revoke all on public.bot_scollegati from authenticated, anon;
grant select on public.bot_scollegati to authenticated;


-- dal journal: scollega un conto (e toglie il suo stato)
create or replace function public.bot_scollega(p_conto bigint)
returns void
language plpgsql volatile security definer set search_path = public
as $$
begin
  if auth.uid() is null then
    raise exception 'accesso richiesto' using errcode = '28000';
  end if;
  if p_conto is null then
    raise exception 'dati non validi' using errcode = '22023';
  end if;
  insert into public.bot_scollegati (utente, conto) values (auth.uid(), p_conto)
  on conflict (utente, conto) do update set scollegato = now();
  delete from public.bot_stato where utente = auth.uid() and conto = p_conto;
end;
$$;

revoke all on function public.bot_scollega(bigint) from public, anon;
grant execute on function public.bot_scollega(bigint) to authenticated;


-- dal journal: ricollega un conto scollegato
create or replace function public.bot_ricollega(p_conto bigint)
returns void
language plpgsql volatile security definer set search_path = public
as $$
begin
  if auth.uid() is null then
    raise exception 'accesso richiesto' using errcode = '28000';
  end if;
  delete from public.bot_scollegati where utente = auth.uid() and conto = p_conto;
end;
$$;

revoke all on function public.bot_ricollega(bigint) from public, anon;
grant execute on function public.bot_ricollega(bigint) to authenticated;


-- le due funzioni del bot, uguali a bot.sql piu' il controllo del conto scollegato

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

  -- conto scollegato dal journal: le operazioni non arrivano piu'
  if exists (select 1 from public.bot_scollegati where utente = u and conto = p_conto) then
    return 0;
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

  -- conto scollegato dal journal: lo stato non viene piu' mostrato
  if exists (select 1 from public.bot_scollegati where utente = u and conto = p_conto) then
    return;
  end if;

  insert into public.bot_stato (utente, conto, bot, dati, aggiornato)
  values (u, p_conto, p_bot, p_dati, now())
  on conflict (utente, conto, bot) do update set dati = excluded.dati, aggiornato = now();
end;
$$;

revoke all on function public.bot_aggiorna_stato(text, bigint, text, jsonb) from public;
grant execute on function public.bot_aggiorna_stato(text, bigint, text, jsonb) to anon, authenticated;
