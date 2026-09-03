/* LeakExpert · sukayipkacaklari.com — minimal, no dependencies */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* header shadow on scroll */
  var hdr = document.querySelector('.hdr');
  if (hdr) {
    var onScroll = function () {
      hdr.setAttribute('data-scrolled', String(window.scrollY > 8));
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* mobile nav */
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('.nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('nav--open');
      burger.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('nav--open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* language switcher: explicit choice is stored by the inline <head> script,
     which is attached before this deferred file loads — see OPEN_SCRIPT. */

  /* reveal on scroll */
  var items = document.querySelectorAll('.rv');
  if (!items.length) return;
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  items.forEach(function (el) { io.observe(el); });

  /* hero telemetry path draw */
  var flow = document.getElementById('flowline');
  if (flow && !reduce) {
    try {
      var len = flow.getTotalLength();
      flow.style.strokeDasharray = len;
      flow.style.strokeDashoffset = len;
      flow.getBoundingClientRect();
      flow.style.transition = 'stroke-dashoffset 1.9s ease-out .2s';
      requestAnimationFrame(function () { flow.style.strokeDashoffset = '0'; });
    } catch (e) { /* noop */ }
  }
})();
