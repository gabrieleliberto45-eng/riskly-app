-- Rinforzi dal controllo del 19 ottobre 2026 (avvisi di sicurezza di Supabase). Si può rieseguire.
-- 1) funzioni dei trigger: girano da sole, non devono essere chiamabili dall'esterno
revoke execute on function public.crea_profilo() from public, anon, authenticated;
revoke execute on function public.proteggi_piano() from public, anon, authenticated;
-- 2) percorso di ricerca fisso per le funzioni dei controlli admin e licenze
alter function public.e_admin() set search_path = public;
alter function public.licenza_admin() set search_path = public;
do $$ declare f regprocedure; begin
  for f in select p.oid::regprocedure from pg_proc p join pg_namespace n on n.oid = p.pronamespace
           where n.nspname = 'public' and p.proname in ('licenza_codice', 'licenza_max_conti') loop
    execute format('alter function %s set search_path = public', f);
  end loop;
end $$;
