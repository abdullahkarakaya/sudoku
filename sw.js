// Çevrimdışı çalışma: önce ağ (güncel sürüm), ağ yoksa önbellek.
const CACHE = "sudoku:" + new URL(self.registration.scope).pathname + ":v1";
const CORE = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png",
  "icons/favicon.png", "icons/apple-touch-icon.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE && k.startsWith("sudoku:")) await caches.delete(k);
    await self.clients.claim();
  })());
});
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  e.respondWith((async () => {
    const key = req.mode === "navigate" ? "index.html" : req;
    try {
      const res = await fetch(req, { cache: "no-store" });
      if (res.ok) (await caches.open(CACHE)).put(key, res.clone());
      return res;
    } catch {
      return (await caches.match(key, { ignoreSearch: true })) || Response.error();
    }
  })());
});
