-- Riskly: ripristina il pannello "Gestione" dell'amministratore.
-- Da eseguire nel SQL Editor di Supabase DOPO sicurezza.sql.
-- sicurezza.sql limita ogni utente al proprio profilo: questo file riconsente
-- all'admin di vedere tutti i profili e cambiare il piano, mentre gli altri
-- utenti continuano a non poter toccare piano e scadenza.

-- chi è l'amministratore (stessa email della lista ADMIN nel sito)
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
