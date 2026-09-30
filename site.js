/* Shadab Ali — site interactions (one deferred script for every page).
   Header · mobile menu · reveals · section index · cursor · project overlay · contact email */
(() => {
  window.__site = 1;
  const root = document.documentElement;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const motionOK = () => !reduceMotion.matches;

  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ---------- Header: stays put and gets slimmer once the page scrolls ---------- */
  const header = document.querySelector('[data-header]');
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    header.classList.toggle('is-scrolled', scrollY > 24);
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  const toggle = document.querySelector('[data-menu-toggle]');
  const nav = document.getElementById('site-nav');
  const setMenu = open => {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
    root.classList.toggle('menu-open', open);
    document.querySelectorAll('main, .site-footer').forEach(el => { el.inert = open; });
  };
  toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); }
  });
  matchMedia('(min-width: 768px)').addEventListener('change', event => { if (event.matches) setMenu(false); });

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
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 })
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

  /* ---------- Section index: "02 / Selected work" along the left edge (wide screens) ---------- */
  const rail = document.querySelector('[data-index-rail]');
  const indexed = [...document.querySelectorAll('[data-index]')];
  if (rail && indexed.length && 'IntersectionObserver' in window) {
    const text = rail.querySelector('.index-rail-text');
    const visible = new Map();
    const hero = document.querySelector('.hero');
    const update = () => {
      let current = null;
      indexed.forEach(section => { if (visible.get(section)) current = section; });
      const heroInView = hero && hero.getBoundingClientRect().bottom > innerHeight * 0.5;
      const label = heroInView ? 'Scroll' : current?.dataset.index;
      if (label) { text.textContent = label; rail.classList.add('is-visible'); }
      else rail.classList.remove('is-visible');
    };
    // A section counts as current while it crosses the middle of the screen.
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => visible.set(entry.target, entry.isIntersecting));
      update();
    }, { rootMargin: '-50% 0px -50% 0px' });
    indexed.forEach(section => observer.observe(section));
    addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
    update();
  }

  /* ---------- "View project" cursor over project images (mouse only) ---------- */
  if (finePointer.matches && motionOK()) {
    const cursor = document.createElement('div');
    cursor.className = 'cursor';
    cursor.setAttribute('aria-hidden', 'true');
    cursor.innerHTML = '<span>View</span><span>Project ↗</span>';
    document.body.append(cursor);
    let x = -300, y = -300, scale = 0, targetX = x, targetY = y, targetScale = 0, running = false;
    const loop = () => {
      x += (targetX - x) * 0.24;
      y += (targetY - y) * 0.24;
      scale += (targetScale - scale) * 0.22;
      cursor.style.transform = `translate3d(${(x + 18).toFixed(1)}px, ${(y + 18).toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;
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
     Project links point at real project pages. With JS, the page's project
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
      note.className = 'dialog-status meta';
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
      if (from) returnFocus = from.closest('.exhibit')?.querySelector('[data-case-link]') || from;
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

  /* ---------- Contact: "Start a project" on a service fills in the project type ---------- */
  const briefLink = document.querySelector('[data-brief-mail]');
  const requested = new URLSearchParams(location.search).get('service');
  if (briefLink && requested) {
    const type = briefLink.dataset.types.split('|').find(item => item.toLowerCase() === requested.toLowerCase());
    const query = briefLink.getAttribute('href').split('?')[1] || '';
    const params = Object.fromEntries(query.split('&').map(pair => pair.split('=').map(decodeURIComponent)));
    if (type && params.body) {
      params.body = params.body.replace(/^Project type.*$/m, `Project type: ${type}`);
      params.subject = `Project enquiry — ${type}`;
      briefLink.href = `mailto:${briefLink.getAttribute('href').slice(7).split('?')[0]}?subject=${encodeURIComponent(params.subject)}&body=${encodeURIComponent(params.body)}`;
    }
  }
})();
