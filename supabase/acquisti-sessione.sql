-- Riskly · ogni acquisto attivato da Stripe ricorda la sessione di pagamento:
-- lo stesso evento ricevuto due volte non attiva due acquisti.
alter table public.acquisti add column if not exists stripe_sessione text;
create unique index if not exists acquisti_stripe_sessione on public.acquisti (stripe_sessione) where stripe_sessione is not null;
