/* Riskly News: mostra la notifica quando esce un articolo (anche a sito chiuso; su iPhone dalla schermata Home).
   Non salva niente in cache: il sito si carica sempre dalla rete. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('push', e => {
  let d = {}; try { d = e.data.json(); } catch(err) { d = { titolo: 'Riskly News', testo: e.data ? e.data.text() : '' }; }
  e.waitUntil(self.registration.showNotification(d.titolo || 'Riskly News', {
    body: d.testo || '', tag: d.tag, icon: '/icon-192.png', badge: '/icon-192.png', data: { url: d.url || '/' } }));
});
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || '/';
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(l => {
    for(const c of l) if('focus' in c){ c.navigate && c.navigate(url); return c.focus(); }
    return self.clients.openWindow(url);
  }));
});
