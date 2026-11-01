-- Riskly News solo con l'abbonamento a parte (Gabriele, 1° novembre 2026: "escludilo" dal Premium).
-- L'articolo intero lo legge solo chi ha un acquisto "Riskly News…" attivo; il piano Premium del journal non basta più.
create or replace function public.ha_news()
returns boolean
language sql stable
security definer
set search_path = public
as $$
  select auth.uid() is not null and exists (
    select 1 from public.acquisti a
    where a.utente = auth.uid() and a.stato = 'attivo' and a.prodotto ilike 'Riskly News%'
  );
$$;
