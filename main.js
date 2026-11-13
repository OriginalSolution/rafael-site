// Rafael landing page: minimal JS (mobile nav + placeholder waitlist form).
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      links.classList.toggle('open', !open);
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { toggle.setAttribute('aria-expanded', 'false'); links.classList.remove('open'); }
    });
  }

  // TODO(backend): replace this handler with a real submission (fetch POST to your waitlist endpoint).
  var form = document.getElementById('waitlist-form');
  var status = document.getElementById('form-status');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = form.elements.email;
      if (!email.value || !email.checkValidity()) {
        status.textContent = 'Please enter a valid email address.';
        email.focus();
        return;
      }
      status.textContent = 'Thanks! This is a preview, so sign-up isn\u2019t connected yet and nothing was sent or saved.';
    });
  }
})();
