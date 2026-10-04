-- ═══════════════════════════════════════════════════════════════════
--  Riskly · gestione ordini dall'area "Gestione" (solo admin)
--  - l'admin vede nome ed email di chi ha fatto l'ordine
--  - l'admin può rifiutare un ordine (stato "rifiutato") o eliminarlo
--  Si può rieseguire.
-- ═══════════════════════════════════════════════════════════════════

-- chi è admin (stessa email del sito)
create or replace function public.e_admin()
returns boolean
language sql stable
as $$
  select lower(coalesce(auth.jwt() ->> 'email', '')) in ('gabrieleliberto1212@gmail.com')
$$;

-- ─── 1. L'admin può eliminare gli ordini ──────────────────────────
drop policy if exists "admin elimina ordini" on public.acquisti;
create policy "admin elimina ordini" on public.acquisti
  for delete to authenticated
  using (public.e_admin());

-- ─── 2. Stato "rifiutato" ammesso ─────────────────────────────────
-- se la colonna stato ha un vincolo sui valori, lo sostituisce con
-- uno che accetta anche "rifiutato"
do $$
declare c record;
begin
  for c in
    select con.conname
    from pg_constraint con
    join pg_class rel on rel.oid = con.conrelid
    join pg_namespace ns on ns.oid = rel.relnamespace
    where ns.nspname = 'public' and rel.relname = 'acquisti'
      and con.contype = 'c' and pg_get_constraintdef(con.oid) ilike '%stato%'
  loop
    execute format('alter table public.acquisti drop constraint %I', c.conname);
  end loop;
end $$;
alter table public.acquisti add constraint acquisti_stato_check
  check (stato in ('in_attesa', 'attivo', 'rifiutato')) not valid;

-- ─── 3. Nome ed email del cliente per ogni ordine ─────────────────
create or replace function public.ordini_clienti()
returns table (id text, email text, nome text)
language sql stable
security definer
set search_path = public
as $$
  select a.id::text, u.email::text, p.nome
  from public.acquisti a
  left join auth.users u on u.id = a.utente
  left join public.profili p on p.id = a.utente
  where public.e_admin()
$$;

revoke all on function public.ordini_clienti() from public, anon;
grant execute on function public.ordini_clienti() to authenticated;
