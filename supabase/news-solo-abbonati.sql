-- Riskly News solo con l'abbonamento a parte (Gabriele, 1° novembre 2026: "escludilo" dal Premium).
-- L'articolo intero lo legge chi ha un acquisto "Riskly News…" attivo; il piano Premium del journal non basta più.
-- Unica eccezione: l'account di Gabriele (gabrieleliberto1212@gmail.com) per controllare gli articoli.
create or replace function public.ha_news()
returns boolean
language sql stable
security definer
set search_path = public
as $$
  select auth.uid() is not null and (
    auth.uid() = '2aa363d7-b519-42e2-8daf-acd0b509865a'::uuid
    or exists (
      select 1 from public.acquisti a
      where a.utente = auth.uid() and a.stato = 'attivo' and a.prodotto ilike 'Riskly News%'
    )
  );
$$;
