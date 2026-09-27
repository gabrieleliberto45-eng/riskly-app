-- Riskly: regole di sicurezza lato server.
-- Da eseguire una volta nel SQL Editor di Supabase (Dashboard → SQL Editor → New query).
-- Il sito controlla già piani e permessi nel browser, ma chiunque può aggirarli dalla
-- console: queste regole fanno sì che il database stesso li faccia rispettare.
-- Prima di eseguirlo, controlla che i nomi (operazioni.utente, profili.id, bucket
-- "screenshot") corrispondano ai tuoi.


-- 1. Operazioni: ognuno legge e modifica solo le proprie ---------------------------

alter table public.operazioni enable row level security;

drop policy if exists "operazioni: solo le proprie" on public.operazioni;
create policy "operazioni: solo le proprie" on public.operazioni
  for all to authenticated
  using (auth.uid() = utente)
  with check (auth.uid() = utente);


-- 2. Profili: si legge il proprio, ma piano e scadenza non si toccano dal browser ----

alter table public.profili enable row level security;

drop policy if exists "profili: lettura del proprio" on public.profili;
create policy "profili: lettura del proprio" on public.profili
  for select to authenticated
  using (auth.uid() = id);

drop policy if exists "profili: modifica del proprio" on public.profili;
create policy "profili: modifica del proprio" on public.profili
  for update to authenticated
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- l'amministratore (pannello "Gestione" del sito) vede e modifica tutti i profili;
-- piano e scadenza li può cambiare solo lui (o il pagamento, con la service role)
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



-- 3. Screenshot: bucket privato, ognuno vede solo la propria cartella --------------
-- Il journal ora usa link temporanei firmati, quindi funziona anche col bucket privato.

update storage.buckets set public = false where id = 'screenshot';

drop policy if exists "screenshot: lettura propria" on storage.objects;
create policy "screenshot: lettura propria" on storage.objects
  for select to authenticated
  using (bucket_id = 'screenshot' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "screenshot: caricamento proprio" on storage.objects;
create policy "screenshot: caricamento proprio" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'screenshot' and (storage.foldername(name))[1] = auth.uid()::text);

drop policy if exists "screenshot: cancellazione propria" on storage.objects;
create policy "screenshot: cancellazione propria" on storage.objects
  for delete to authenticated
  using (bucket_id = 'screenshot' and (storage.foldername(name))[1] = auth.uid()::text);

-- limite di 5 MB e solo immagini, anche se qualcuno aggira il controllo nel browser
update storage.buckets
  set file_size_limit = 5242880,
      allowed_mime_types = array['image/png','image/jpeg','image/webp','image/gif']
  where id = 'screenshot';
