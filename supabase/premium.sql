-- Riskly · codice sconto del 30% sui bot, solo per chi ha il journal Premium attivo. Si può rieseguire.

create or replace function public.codice_sconto_premium()
returns text
language sql stable
security definer
set search_path = public
as $$
  select valore from public.impostazioni_private
  where chiave = 'codice_premium'
    and exists (
      select 1 from public.profili
      where id = auth.uid() and piano = 'premium'
        and (scadenza is null or scadenza > now())
    )
$$;

revoke all on function public.codice_sconto_premium() from public, anon;
grant execute on function public.codice_sconto_premium() to authenticated;

insert into public.impostazioni_private (chiave, valore)
values ('codice_premium', 'PREMIUM30')
on conflict (chiave) do update set valore = excluded.valore;
