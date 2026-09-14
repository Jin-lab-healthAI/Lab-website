/* Jin Lab — ~3 KB of vanilla JS. No frameworks, no build step. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- theme toggle (persisted) ---- */
  var root = document.documentElement;
  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('jinlab-theme', next); } catch (e) {}
    });
  }

  /* ---- sticky nav state + scroll progress ---- */
  var nav = document.getElementById('nav');
  var bar = document.getElementById('nav-progress');
  function onScroll() {
    var y = window.scrollY || 0;
    if (nav) nav.classList.toggle('is-stuck', y > 8);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- mobile menu ---- */
  var burger = document.getElementById('burger');
  var menu = document.getElementById('mobile-menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      menu.hidden = open;
    });
  }

  /* ---- reveal on scroll ---- */
  var items = document.querySelectorAll('.reveal');
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---- pointer-tracked glow on research cards ---- */
  if (!reduced) {
    document.querySelectorAll('.prog').forEach(function (card) {
      card.addEventListener('pointermove', function (ev) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', ((ev.clientX - r.left) / r.width) * 100 + '%');
        card.style.setProperty('--my', ((ev.clientY - r.top) / r.height) * 100 + '%');
      });
    });
  }

  /* ---- publications: type filter + text search ---- */
  var chips = document.querySelectorAll('.chip[data-filter]');
  var search = document.getElementById('pub-search');
  var empty = document.getElementById('pub-empty');
  if (chips.length || search) {
    var state = { type: 'all', q: '' };

    function apply() {
      var shown = 0;
      document.querySelectorAll('.pub[data-type]').forEach(function (li) {
        var okType = state.type === 'all' || li.dataset.type === state.type;
        var okText = !state.q || (li.dataset.search || '').indexOf(state.q) !== -1;
        var show = okType && okText;
        li.style.display = show ? '' : 'none';
        if (show) shown++;
      });
      // hide year headings whose entries are all filtered out
      document.querySelectorAll('.pubyear').forEach(function (group) {
        var any = Array.prototype.some.call(group.querySelectorAll('.pub'), function (li) {
          return li.style.display !== 'none';
        });
        group.style.display = any ? '' : 'none';
      });
      if (empty) empty.hidden = shown !== 0;
    }

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        chips.forEach(function (c) { c.classList.remove('is-active'); });
        chip.classList.add('is-active');
        state.type = chip.dataset.filter;
        apply();
      });
    });
    if (search) {
      search.addEventListener('input', function () {
        state.q = search.value.trim().toLowerCase();
        apply();
      });
    }
  }
})();
