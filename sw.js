const CACHE_NAME = 'experfrut-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css', // Cambia estas rutas por las reales de tu proyecto
  '/static/js/funciones.js',
  '/static/img/logo.png'
];

// Instalar el Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Responder con la caché cuando no haya internet
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});