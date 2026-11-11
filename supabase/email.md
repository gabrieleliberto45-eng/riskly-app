# Email degli account (dal 19 ottobre 2026)
- Invio tramite **Resend** (account di Gabriele), dominio riskly.trade verificato, regione eu-west-1.
- Supabase → Auth → SMTP: smtp.resend.com, porta 465, utente `resend`, password = chiave API di Resend (non nel repository).
  Mittente: Riskly <noreply@riskly.trade>. Limite: 100 email all'ora.
- Record DNS su Netlify (zona riskly.trade): TXT resend._domainkey, MX e TXT su send, CNAME rsend, TXT _dmarc (p=none).
  I record MX/SPF di ImprovMX sulla radice (inoltro della posta in arrivo) restano invariati.
- Modelli in italiano: conferma account, recupero password, link di accesso, cambio email.

## Email promozionali (regola dall'11 novembre 2026)
Oggi dal sistema partono solo email di servizio (conferma account, recupero password). Se si inviano email promozionali o newsletter, ognuna deve avere in fondo:
- il link per disiscriversi (un clic, che funziona davvero e toglie l'indirizzo dalla lista);
- l'indirizzo postale dell'azienda (CAN-SPAM, USA) e i dati del titolare: Gabriele Liberto · Ditta individuale · P. IVA 04948840162 · [INDIRIZZO POSTALE DA INSERIRE: Gabriele deve darlo];
- il mittente chiaro (Riskly <noreply@riskly.trade>) e un oggetto non ingannevole.
Si scrive solo a chi ha spuntato il consenso facoltativo ("novità di Riskly").
