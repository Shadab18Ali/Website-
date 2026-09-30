/* Shadab Ali — site interactions (one deferred script for every page).
   Header · mobile menu · reveals · parallax · cursor · project overlay · contact form */
(() => {
  window.__site = 1;
  const root = document.documentElement;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const motionOK = () => !reduceMotion.matches;

  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ---------- Header: tucks away on scroll down, returns on scroll up ---------- */
  const header = document.querySelector('[data-header]');
  let lastY = scrollY;
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    const y = scrollY;
    header.classList.toggle('is-scrolled', y > 8);
    if (root.classList.contains('menu-open')) return;
    if (y > 320 && y > lastY + 6) header.classList.add('is-hidden');
    else if (y < lastY - 6 || y <= 320) header.classList.remove('is-hidden');
    lastY = y;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  header.addEventListener('focusin', () => header.classList.remove('is-hidden'));

  /* ---------- Mobile menu ---------- */
  const toggle = document.querySelector('[data-menu-toggle]');
  const nav = document.getElementById('site-nav');
  const setMenu = open => {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
    root.classList.toggle('menu-open', open);
    document.querySelectorAll('main, .site-footer').forEach(el => { el.inert = open; });
    if (open) header.classList.remove('is-hidden');
  };
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
  });
  matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) setMenu(false); });

  /* ---------- Reveals: fade, image clip and word-by-word text ---------- */
  const splitWords = element => {
    if (element.dataset.split) return;
    element.dataset.split = 'done';
    let index = 0;
    const walk = node => {
      [...node.childNodes].forEach(child => {
        if (child.nodeType === Node.TEXT_NODE) {
          const fragment = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { fragment.append(document.createTextNode(part)); return; }
            const word = document.createElement('span');
            const inner = document.createElement('span');
            word.className = 'w';
            inner.textContent = part;
            inner.style.setProperty('--i', index++);
            word.append(inner);
            fragment.append(word);
          });
          child.replaceWith(fragment);
        } else if (child.nodeType === Node.ELEMENT_NODE && !child.classList.contains('visually-hidden')) {
          walk(child);
        }
      });
    };
    walk(element);
  };
  const revealObserver = 'IntersectionObserver' in window
    ? new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          revealObserver.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -6% 0px', threshold: 0.1 })
    : null;
  const reveal = scope => {
    const targets = [...scope.querySelectorAll('[data-reveal]')];
    if (!motionOK() || !revealObserver) { targets.forEach(el => el.classList.add('is-in')); return; }
    targets.forEach(el => {
      if (el.classList.contains('split')) splitWords(el);
      revealObserver.observe(el);
    });
  };
  reveal(document);
  reduceMotion.addEventListener?.('change', () => document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-in')));

  /* ---------- Parallax on the editorial image sequence ---------- */
  const parallaxItems = [...document.querySelectorAll('[data-parallax]')];
  if (parallaxItems.length && motionOK() && 'IntersectionObserver' in window) {
    const active = new Set();
    let frame = 0;
    const update = () => {
      frame = 0;
      const vh = innerHeight;
      active.forEach(item => {
        const box = item.getBoundingClientRect();
        const progress = (box.top + box.height / 2 - vh / 2) / vh;
        const limit = box.height * 0.05;
        const shift = Math.max(-limit, Math.min(limit, -progress * parseFloat(item.dataset.parallax) * vh));
        item.style.setProperty('--py', `${shift.toFixed(1)}px`);
      });
    };
    const request = () => { if (!frame) frame = requestAnimationFrame(update); };
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { entry.isIntersecting ? active.add(entry.target) : active.delete(entry.target); });
      request();
    }, { rootMargin: '15% 0px' });
    parallaxItems.forEach(item => observer.observe(item));
    addEventListener('scroll', request, { passive: true });
    addEventListener('resize', request, { passive: true });
  }

  /* ---------- "View" cursor over project images (mouse only) ---------- */
  if (finePointer.matches && motionOK()) {
    const cursor = document.createElement('div');
    cursor.className = 'cursor';
    cursor.setAttribute('aria-hidden', 'true');
    cursor.textContent = 'View';
    document.body.append(cursor);
    let x = -200, y = -200, scale = 0, targetX = x, targetY = y, targetScale = 0, running = false;
    const loop = () => {
      x += (targetX - x) * 0.22;
      y += (targetY - y) * 0.22;
      scale += (targetScale - scale) * 0.2;
      cursor.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;
      if (Math.abs(targetX - x) + Math.abs(targetY - y) + Math.abs(targetScale - scale) > 0.05) requestAnimationFrame(loop);
      else running = false;
    };
    const kick = () => { if (!running) { running = true; requestAnimationFrame(loop); } };
    document.addEventListener('pointermove', event => {
      if (event.pointerType !== 'mouse') return;
      targetX = event.clientX;
      targetY = event.clientY;
      targetScale = event.target.closest('[data-cursor="view"]') ? 1 : 0;
      if (scale < 0.02 && targetScale === 1) { x = targetX; y = targetY; }
      kick();
    }, { passive: true });
    document.documentElement.addEventListener('pointerleave', () => { targetScale = 0; kick(); });
  }

  /* ---------- Project overlay ----------
     "View project" links point at real project pages. With JS, the page's project
     article is fetched and shown in a modal dialog; the URL updates so the back
     button closes it and the address can be shared. */
  const canDialog = typeof HTMLDialogElement === 'function' && 'showModal' in HTMLDialogElement.prototype;
  if (canDialog && !document.body.classList.contains('page-case') && document.querySelector('[data-open-project]')) {
    const cache = new Map();
    const pageTitle = document.title;
    const dialog = document.createElement('dialog');
    dialog.className = 'project-dialog';
    dialog.setAttribute('aria-label', 'Project');
    document.body.append(dialog);
    let returnFocus = null;
    let pushed = false;
    let closing = false;

    const load = href => {
      const path = new URL(href, location.href).pathname;
      if (!cache.has(path)) {
        cache.set(path, fetch(path, { credentials: 'same-origin' })
          .then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.text(); })
          .catch(error => { cache.delete(path); throw error; }));
      }
      return cache.get(path);
    };
    const status = text => {
      const note = document.createElement('p');
      note.className = 'dialog-status label';
      note.setAttribute('role', 'status');
      note.textContent = text;
      dialog.replaceChildren(note);
    };
    const render = markup => {
      const doc = new DOMParser().parseFromString(markup, 'text/html');
      const article = doc.querySelector('[data-case]');
      if (!article) throw new Error('Project content not found');
      // The underlying page already has an h1, so the project's headings move down a level.
      article.querySelectorAll('h1, h2, h3').forEach(heading => {
        const replacement = doc.createElement(`h${Number(heading.tagName[1]) + 1}`);
        [...heading.attributes].forEach(attribute => replacement.setAttribute(attribute.name, attribute.value));
        replacement.innerHTML = heading.innerHTML;
        heading.replaceWith(replacement);
      });
      dialog.replaceChildren(document.importNode(article, true));
      dialog.removeAttribute('aria-label');
      dialog.setAttribute('aria-labelledby', 'case-title');
      dialog.scrollTop = 0;
      document.title = doc.title;
      reveal(dialog);
      dialog.querySelector('[data-case-close]')?.focus({ preventScroll: true });
    };
    const open = async (href, { from = null, mode = 'push' } = {}) => {
      const url = new URL(href, location.href);
      if (from) returnFocus = from.closest('.project')?.querySelector('.view-link') || from;
      if (!dialog.open) {
        status('Loading project…');
        dialog.classList.remove('is-closing');
        dialog.showModal();
        root.classList.add('has-dialog');
      }
      try {
        render(await load(url.href));
        if (mode === 'push') { history.pushState({ project: url.pathname }, '', url.pathname); pushed = true; }
        else if (mode === 'replace') history.replaceState({ project: url.pathname }, '', url.pathname);
      } catch (error) {
        location.href = url.href; // fall back to the full project page
      }
    };
    const finishClose = () => {
      closing = false;
      dialog.classList.remove('is-closing');
      if (dialog.open) dialog.close();
      root.classList.remove('has-dialog');
      document.title = pageTitle;
      if (returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
    };
    const close = () => {
      if (!dialog.open || closing) return;
      closing = true;
      if (!motionOK()) { finishClose(); return; }
      dialog.classList.add('is-closing');
      setTimeout(finishClose, 430);
    };
    const requestClose = () => {
      if (pushed && history.state?.project) history.back(); // popstate closes the dialog
      else close();
    };

    document.addEventListener('click', event => {
      const link = event.target.closest('[data-open-project]');
      if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const inside = dialog.contains(link);
      open(link.href, { from: inside ? null : link, mode: inside || dialog.open ? 'replace' : 'push' });
    });
    dialog.addEventListener('click', event => {
      if (event.target.closest('[data-case-close]')) { event.preventDefault(); requestClose(); }
    });
    dialog.addEventListener('cancel', event => { event.preventDefault(); requestClose(); });
    // Keep Tab and Shift+Tab cycling inside the open project.
    dialog.addEventListener('keydown', event => {
      if (event.key !== 'Tab') return;
      const focusable = [...dialog.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')]
        .filter(el => el.getClientRects().length && !el.closest('[aria-hidden="true"]'));
      if (!focusable.length) { event.preventDefault(); return; }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && (document.activeElement === first || document.activeElement === dialog)) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
    addEventListener('popstate', event => {
      if (event.state?.project) open(event.state.project, { mode: 'none' });
      else { pushed = false; close(); }
    });
    const prefetch = event => {
      const link = event.target.closest?.('[data-open-project]');
      if (link) load(link.href).catch(() => {});
    };
    document.addEventListener('pointerover', prefetch, { passive: true });
    document.addEventListener('focusin', prefetch);
  }

  /* ---------- Services: pre-select the service on the contact form ---------- */
  document.querySelectorAll('[data-service]').forEach(link => {
    link.href = `contact.html?service=${encodeURIComponent(link.dataset.service)}#brief`;
  });
  const serviceSelect = document.querySelector('[name="service"]');
  const requested = new URLSearchParams(location.search).get('service');
  if (serviceSelect && requested) {
    const option = [...serviceSelect.options].find(item => item.value && item.textContent.toLowerCase() === requested.toLowerCase());
    if (option) serviceSelect.value = option.value;
  }

  /* ---------- Contact form ---------- */
  const form = document.getElementById('inquiryForm');
  const formStatus = document.getElementById('formStatus');
  if (form && formStatus) {
    const submit = form.querySelector('[type="submit"]');
    const submitLabel = submit.innerHTML;
    const localPreview = ['localhost', '127.0.0.1'].includes(location.hostname);
    if (localPreview) {
      submit.innerHTML = 'Prepare inquiry email <span aria-hidden="true">→</span>';
      formStatus.textContent = 'Local preview: the live form sends through Vercel once the email settings are added. Here, the button prepares an email instead.';
    }
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      formStatus.classList.remove('is-success', 'is-error');
      const values = new FormData(form);
      if (localPreview) {
        const get = name => String(values.get(name) || '').trim();
        const subject = `Website inquiry — ${get('service')} — ${get('name')}`;
        const body = `Hi Shadab,\n\nI'd like to discuss a website project.\n\nName: ${get('name')}\nEmail: ${get('email')}\nProject type: ${get('service')}\nCurrent website: ${get('website') || 'Not provided'}\nBudget: ${get('budget') || 'Not specified'}\nTimeline: ${get('timeline') || 'Not specified'}\n\nProject details:\n${get('details')}\n\nThanks,\n${get('name')}`;
        formStatus.textContent = 'Your email app should open now. Review the message and press Send there.';
        location.href = `mailto:shadab18ali@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        return;
      }
      submit.disabled = true;
      submit.textContent = 'Sending…';
      formStatus.textContent = 'Sending your project request…';
      try {
        const response = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams(values).toString(),
        });
        if (!response.ok) throw new Error(`Form submission failed (${response.status})`);
        form.reset();
        formStatus.textContent = 'Your request was sent. Thank you — I’ll reply by email.';
        formStatus.classList.add('is-success');
        location.href = 'thanks.html';
      } catch (error) {
        formStatus.textContent = 'The form could not send your request. Please email or message me on WhatsApp instead.';
        formStatus.classList.add('is-error');
        formStatus.focus();
        console.error('Inquiry form submission failed:', error);
      } finally {
        submit.disabled = false;
        submit.innerHTML = submitLabel;
      }
    });
  }
})();
