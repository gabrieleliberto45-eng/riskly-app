-- 16/11/2026 · controllo sicurezza (approvato da Gabriele: "approvo: metti online correzione sicurezza news")
-- 1) La vista notizie_anteprima gira come postgres (scavalca la RLS): solo lettura per il pubblico.
revoke insert, update, delete, truncate, references, trigger on public.notizie_anteprima from anon, authenticated, public;
grant select on public.notizie_anteprima to anon, authenticated;
-- 2) Gli utenti non possono cambiare da soli piano, scadenza e codice cliente Stripe.
create or replace function public.proteggi_piano() returns trigger
language plpgsql security definer set search_path to 'public' as $$
begin
  if (new.piano is distinct from old.piano or new.scadenza is distinct from old.scadenza
      or new.stripe_cliente is distinct from old.stripe_cliente)
     and auth.role() = 'authenticated' and not public.e_admin() then
    raise exception 'Solo l''amministratore può cambiare piano, scadenza e cliente Stripe';
  end if;
  return new;
end $$;
