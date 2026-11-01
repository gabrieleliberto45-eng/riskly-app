-- Riskly News, 1° novembre 2026 (Gabriele): copertina per ogni articolo e sezione "Setup XAU" (comportamento dell'oro, zone, trend).
alter table public.notizie add column if not exists copertina text;                       -- es. /copertine/ID.jpg sul sito news
alter table public.notizie add column if not exists tabella jsonb not null default '[]'::jsonb;   -- righe [etichetta, valore] (Setup XAU)
alter table public.notizie drop constraint if exists notizie_categoria_check;
alter table public.notizie add constraint notizie_categoria_check
  check (categoria in ('oro', 'dollaro', 'fed', 'tassi', 'straordinarie', 'settimana', 'setup'));
drop view if exists public.notizie_anteprima;
create view public.notizie_anteprima as
  select id, data, categoria, titolo, sommario, copertina
  from public.notizie
  where pubblicato;
grant select on public.notizie_anteprima to anon, authenticated;
update public.notizie set copertina = '/copertine/' || id || '.jpg' where copertina is null;
-- 1° novembre 2026: categoria "dati" (analisi del report subito dopo l'uscita di un dato importante)
alter table public.notizie drop constraint if exists notizie_categoria_check;
alter table public.notizie add constraint notizie_categoria_check
  check (categoria in ('oro', 'dollaro', 'fed', 'tassi', 'straordinarie', 'settimana', 'setup', 'dati'));
