// Rafael landing page: small, dependency-free enhancements.
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('open', !open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) { toggle.setAttribute('aria-expanded', 'false'); links.classList.remove('open'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) { toggle.click(); toggle.focus(); }
    });
  }

  // Header background on scroll
  var header = document.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 20); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Reveal on scroll + pause hero animations when hidden
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { reduce ? el.classList.add('in') : io.observe(el); });
    var hero = document.querySelector('.hero');
    if (hero) new IntersectionObserver(function (e) { hero.classList.toggle('paused', !e[0].isIntersecting); }).observe(hero);
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
  document.addEventListener('visibilitychange', function () { doc.classList.toggle('paused', document.hidden); });

  // Gallery arrows
  var gallery = document.querySelector('.gallery');
  document.querySelectorAll('.gallery-ctrl .round').forEach(function (b) {
    b.addEventListener('click', function () {
      gallery.scrollBy({ left: Number(b.dataset.dir) * Math.min(600, gallery.clientWidth * 0.8), behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  // Point download buttons at the newest release APK (all releases are pre-releases,
  // so /releases/latest doesn't resolve). Falls back to the hard-coded link.
  fetch('https://api.github.com/repos/OriginalSolution/rafael-android/releases?per_page=5', { headers: { Accept: 'application/vnd.github+json' } })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (list) {
      for (var i = 0; i < list.length; i++) {
        var rel = list[i];
        if (rel.draft) continue;
        var apk = (rel.assets || []).filter(function (a) { return /\.apk$/i.test(a.name); })[0];
        if (!apk) continue;
        document.querySelectorAll('.js-apk').forEach(function (a) { a.href = apk.browser_download_url; });
        document.querySelectorAll('.js-apk-version').forEach(function (s) { s.textContent = rel.tag_name.replace(/^v/, 'Version ') + ' · APK'; });
        return;
      }
    }).catch(function () {});

  // Testimonials: rendered from testimonials.json. Empty list keeps the invitation card.
  var list = document.getElementById('stories-list');
  if (list) {
    fetch('testimonials.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (items) {
        items = (Array.isArray(items) ? items : []).filter(function (t) { return t && t.quote; });
        if (!items.length) return;
        var invite = list.querySelector('.story-empty');
        var frag = document.createDocumentFragment();
        items.forEach(function (t) {
          var card = document.createElement('article');
          card.className = 'glass story reveal in';
          var q = document.createElement('blockquote'); q.textContent = t.quote;
          var who = document.createElement('p'); who.className = 'who';
          who.textContent = (t.anonymous || !t.name) ? 'Anonymous' : t.name;
          if (t.detail) { var d = document.createElement('span'); d.textContent = t.detail; who.appendChild(d); }
          card.appendChild(q); card.appendChild(who); frag.appendChild(card);
        });
        list.insertBefore(frag, invite);
        if (invite) {
          invite.classList.remove('story-empty');
          invite.querySelector('h3').textContent = 'Share your story';
        }
      }).catch(function () {});
  }

  var y = document.querySelector('.js-year'); if (y) y.textContent = new Date().getFullYear();
})();
