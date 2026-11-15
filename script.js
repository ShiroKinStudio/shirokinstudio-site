'use strict';

// Lightweight enhancement only: the page and Play Store links work without JS.
const year = document.getElementById('copyright-year');
if (year) year.textContent = String(new Date().getFullYear());

// GA4 outbound events are sent only if the site owner configures GA4 later.
// Never delay navigation or fire an analytics request by ourselves.
document.querySelectorAll('a[data-game]').forEach(link => {
  link.addEventListener('click', () => {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'select_content', {
        content_type: 'mobile_game',
        item_id: link.dataset.game,
        outbound: true
      });
    }
  });
});