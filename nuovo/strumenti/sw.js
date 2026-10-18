/* Riskly Strumenti: serve solo per mostrare gli avvisi del calendario (anche su iPhone, dalla schermata Home).
   Non salva niente in cache: il sito si carica sempre dalla rete. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(l => {
    for(const c of l) if('focus' in c){ c.navigate && c.navigate('/#calendario'); return c.focus(); }
    return self.clients.openWindow('/#calendario');
  }));
});
