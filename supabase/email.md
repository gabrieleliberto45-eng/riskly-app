# Email degli account (dal 19 ottobre 2026)
- Invio tramite **Resend** (account di Gabriele), dominio riskly.trade verificato, regione eu-west-1.
- Supabase → Auth → SMTP: smtp.resend.com, porta 465, utente `resend`, password = chiave API di Resend (non nel repository).
  Mittente: Riskly <noreply@riskly.trade>. Limite: 100 email all'ora.
- Record DNS su Netlify (zona riskly.trade): TXT resend._domainkey, MX e TXT su send, CNAME rsend, TXT _dmarc (p=none).
  I record MX/SPF di ImprovMX sulla radice (inoltro della posta in arrivo) restano invariati.
- Modelli in italiano: conferma account, recupero password, link di accesso, cambio email.
