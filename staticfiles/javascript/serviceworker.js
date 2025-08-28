var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/',  // pre-cache homepage
        // you can also add critical assets like CSS/JS/icons here if you want
      ]);
    })
  );
});

// cleanup old caches on activate
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          return cacheName.startsWith('djangopwa-') && cacheName !== staticCacheName;
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);

  // Don’t intercept service worker file itself
  if (requestUrl.pathname === '/serviceworker.js') {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(function(response) {
      if (response) {
        // return cached response immediately
        return response;
      }
      // otherwise fetch from network and cache it for future
      return fetch(event.request).then(function(networkResponse) {
        return caches.open(staticCacheName).then(function(cache) {
          // only cache successful GET requests (skip errors, POST, etc.)
          if (event.request.method === 'GET' && networkResponse.ok) {
            cache.put(event.request, networkResponse.clone());
          }
          return networkResponse;
        });
      }).catch(function() {
        // optional: fallback offline page
        if (requestUrl.pathname === '/') {
          return caches.match('/'); // serve cached homepage if offline
        }
      });
    })
  );
});
