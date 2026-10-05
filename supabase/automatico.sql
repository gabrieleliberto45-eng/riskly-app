-- Riskly · pagamenti automatici e codice sconto del corso. Si può rieseguire.

-- il cliente Stripe di chi ha un abbonamento al journal (per toglierlo quando finisce)
alter table public.profili add column if not exists stripe_cliente text;

-- codice sconto del 50% sul videocorso, solo per chi ha comprato un software
create or replace function public.codice_sconto_corso()
returns text
language sql stable
security definer
set search_path = public
as $$
  select valore from public.impostazioni_private
  where chiave = 'codice_corso'
    and exists (
      select 1 from public.acquisti
      where utente = auth.uid() and stato = 'attivo'
        and prodotto !~* 'corso' and prodotto !~* '^journal'
    )
$$;

revoke all on function public.codice_sconto_corso() from public, anon;
grant execute on function public.codice_sconto_corso() to authenticated;

insert into public.impostazioni_private (chiave, valore)
values ('codice_corso', 'SOFTWARE50')
on conflict (chiave) do update set valore = excluded.valore;

-- quando il cliente ha accettato termini e rinuncia al recesso (prima del pagamento)
alter table public.acquisti add column if not exists termini_accettati timestamptz;
