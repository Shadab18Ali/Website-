const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');

function closeMenu() {
  nav.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open menu');
  document.body.classList.remove('menu-open');
}

menuButton.addEventListener('click', () => {
  const open = !nav.classList.contains('open');
  nav.classList.toggle('open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  document.body.classList.toggle('menu-open', open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && nav.classList.contains('open')) {
    closeMenu();
    menuButton.focus();
  }
});

document.querySelectorAll('[data-service]').forEach(link => {
  link.href = `contact.html?service=${encodeURIComponent(link.dataset.service)}#inquiry`;
});

const serviceSelect = document.querySelector('[name="service"]');
if (serviceSelect) {
  const requestedService = new URLSearchParams(window.location.search).get('service');
  if (requestedService) {
    const wanted = requestedService.toLowerCase();
    const option = [...serviceSelect.options].find(item => item.textContent.toLowerCase() === wanted)
      || [...serviceSelect.options].find(item => item.value && item.textContent.toLowerCase().includes(wanted.split(' ')[0]));
    if (option) serviceSelect.value = option.value;
  }
}

const inquiryForm = document.querySelector('#inquiryForm');
const formStatus = document.querySelector('#formStatus');
if (inquiryForm) {
  const submitButton = inquiryForm.querySelector('[type="submit"]');
  const originalButton = submitButton.innerHTML;
  const localPreview = ['localhost', '127.0.0.1'].includes(window.location.hostname);
  if (localPreview) {
    submitButton.innerHTML = 'Prepare inquiry email <span aria-hidden="true">↗</span>';
    formStatus.textContent = 'Local preview: the live form activates on Vercel after email settings are added. Here, the button prepares an email for you to send.';
  }
  inquiryForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (!inquiryForm.reportValidity()) return;
    formStatus.classList.remove('is-success', 'is-error');
    const values = new FormData(inquiryForm);
    if (localPreview) {
      const name = String(values.get('name')).trim();
      const email = String(values.get('email')).trim();
      const service = String(values.get('service')).trim();
      const website = String(values.get('website')).trim();
      const details = String(values.get('details')).trim();
      const budget = String(values.get('budget') || '').trim() || 'Not specified';
      const timeline = String(values.get('timeline') || '').trim() || 'Not specified';
      const subject = `Website inquiry — ${service} — ${name}`;
      const body = `Hi Shadab,\n\nI'd like to discuss a website project.\n\nName: ${name}\nEmail: ${email}\nService: ${service}\nCurrent website: ${website || 'Not provided'}\nEstimated budget: ${budget}\nDesired timeline: ${timeline}\n\nProject details:\n${details}\n\nThanks,\n${name}`;
      formStatus.textContent = 'Your email app should open now. Review the message and press Send there.';
      window.location.href = `mailto:shadab18ali@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      return;
    }
    submitButton.disabled = true;
    submitButton.textContent = 'Sending request…';
    formStatus.textContent = 'Sending your project request…';
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(values).toString(),
      });
      if (!response.ok) throw new Error(`Form submission failed (${response.status})`);
      inquiryForm.reset();
      formStatus.textContent = 'Your request was sent. Thank you — I’ll reply by email.';
      formStatus.classList.add('is-success');
      window.location.href = 'thanks.html';
    } catch (error) {
      formStatus.textContent = 'The form could not send your request. Please use the direct email or WhatsApp link on this page.';
      formStatus.classList.add('is-error');
      formStatus.focus();
      console.error('Inquiry form submission failed:', error);
    } finally {
      submitButton.disabled = false;
      submitButton.innerHTML = originalButton;
    }
  });
}

// Testimonials ship as hidden placeholders; ?preview shows them, and placeholder cards never render otherwise.
const testimonials = document.querySelector('[data-testimonials]');
if (testimonials) {
  if (new URLSearchParams(window.location.search).has('preview')) {
    testimonials.hidden = false;
    testimonials.classList.add('is-preview');
  } else {
    testimonials.querySelectorAll('[data-placeholder]').forEach(card => card.remove());
    if (!testimonials.querySelector('.testimonial')) testimonials.hidden = true;
  }
}

document.querySelector('#year').textContent = new Date().getFullYear();
