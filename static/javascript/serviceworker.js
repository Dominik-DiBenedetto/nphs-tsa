// serviceworker.js
const STATIC_CACHE = 'djangopwa-static-v3';

self.addEventListener('install', (event) => {
  // Take over immediately on next navigation
  self.skipWaiting();
  // (Optional) Precache a few critical static files. Leave empty if you want purely runtime caching.
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll([
      // '/static/css/styles.css',
      // '/static/js/app.js',
      // '/static/images/logo.png',
    ]))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    // Claim control right away so the new fetch rules apply without a manual refresh
    await self.clients.claim();
    // Delete any old runtime caches created by previous versions
    const names = await caches.keys();
    await Promise.all(
      names.map((name) => {
        // keep only the current static cache; remove everything else
        if (name !== STATIC_CACHE) {
          return caches.delete(name);
        }
      })
    );
  })());
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Don’t touch non-GET requests or the SW file itself
  if (req.method !== 'GET' || url.pathname === '/serviceworker.js') return;

  // 1) **Network-only for HTML / navigations** to keep CSRF fresh
  const accept = req.headers.get('accept') || '';
  if (req.mode === 'navigate' || accept.includes('text/html')) {
    event.respondWith(fetch(req, { cache: 'no-store' })
      .catch(() => caches.match('/offline.html')) // optional offline fallback if you add one
    );
    return;
  }

  // 2) **Cache static assets only**
  const isStaticPath =
    url.pathname.startsWith('/static/') ||
    url.pathname.startsWith('/staticfiles/'); // include your prod path if different

  const isStaticByType = [
    'style', 'script', 'image', 'font', 'audio', 'video', 'worker'
  ].includes(req.destination);

  if (isStaticPath || isStaticByType) {
    // Cache-first, then update in background (stale-while-revalidate-ish)
    event.respondWith((async () => {
      const cached = await caches.match(req);
      const fetchPromise = fetch(req).then(async (res) => {
        if (res && res.ok) {
          const cache = await caches.open(STATIC_CACHE);
          cache.put(req, res.clone());
        }
        return res;
      });
      return cached || fetchPromise;
    })());
    return;
  }

  // 3) Everything else → pass-through network (and don't cache)
  event.respondWith(fetch(req, { cache: 'no-store' }));
});

/*
var staticCacheName = "djangopwa-v1";

self.addEventListener("install", function (event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            return cache.addAll([
                "/", // pre-cache homepage
                // you can also add critical assets like CSS/JS/icons here if you want
            ]);
        })
    );
});

// cleanup old caches on activate
self.addEventListener("activate", function (event) {
    event.waitUntil(
        caches.keys().then(function (cacheNames) {
            return Promise.all(
                cacheNames
                    .filter(function (cacheName) {
                        return (
                            cacheName.startsWith("djangopwa-") &&
                            cacheName !== staticCacheName
                        );
                    })
                    .map(function (cacheName) {
                        return caches.delete(cacheName);
                    })
            );
        })
    );
});

self.addEventListener("fetch", function (event) {
    var requestUrl = new URL(event.request.url);

    // Don’t intercept service worker file itself
    if (requestUrl.pathname === "/serviceworker.js") {
        return;
    }

    // skip caching for login/register/logout (always fetch from network)
    if (
        requestUrl.pathname.startsWith("/login") ||
        requestUrl.pathname.startsWith("/register") ||
        requestUrl.pathname.startsWith("/logout")
    ) {
        return event.respondWith(fetch(event.request));
    }

    event.respondWith(
        caches.match(event.request).then(function (response) {
            if (response) {
                // return cached response immediately
                return response;
            }
            // otherwise fetch from network and cache it for future
            return fetch(event.request)
                .then(function (networkResponse) {
                    return caches.open(staticCacheName).then(function (cache) {
                        // only cache successful GET requests (skip errors, POST, etc.)
                        if (
                            event.request.method === "GET" &&
                            networkResponse.ok
                        ) {
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    });
                })
                .catch(function () {
                    // optional: fallback offline page
                    if (requestUrl.pathname === "/") {
                        return caches.match("/"); // serve cached homepage if offline
                    }
                });
        })
    );
});
*/