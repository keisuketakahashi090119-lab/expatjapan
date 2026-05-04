// Affiliate link click tracking for GA4
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('a[href]').forEach(function(link) {
    link.addEventListener('click', function() {
      var href = this.href || '';
      var affiliates = [
        { domain: 'wise.com', name: 'Wise' },
        { domain: 'safetywing.com', name: 'SafetyWing' }
      ];
      affiliates.forEach(function(affiliate) {
        if (href.indexOf(affiliate.domain) !== -1) {
          if (typeof gtag === 'function') {
            gtag('event', 'affiliate_click', {
              'affiliate_name': affiliate.name,
              'link_url': href,
              'page_location': window.location.href
            });
          }
        }
      });
    });
  });
});
