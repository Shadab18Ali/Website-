(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const clamp = (value, low, high) => Math.min(high, Math.max(low, value));

  const progress = document.createElement('div');
  progress.className = 'motion-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.append(progress);
  const topButton = document.createElement('button');
  topButton.className = 'motion-top';
  topButton.type = 'button';
  topButton.textContent = '↑';
  topButton.setAttribute('aria-label', 'Back to top');
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduced.matches ? 'instant' : 'smooth' }));
  document.body.append(topButton);
  let scrollFrame = 0;
  const updateScroll = () => {
    scrollFrame = 0;
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${max > 0 ? clamp(scrollY / max, 0, 1) : 0})`;
    topButton.classList.toggle('is-visible', scrollY > 780);
  };
  addEventListener('scroll', () => { if (!scrollFrame) scrollFrame = requestAnimationFrame(updateScroll); }, { passive: true });
  addEventListener('resize', updateScroll, { passive: true });
  updateScroll();

  if (!reduced.matches && 'IntersectionObserver' in window) {
    const revealTargets = [...document.querySelectorAll('main > section:not(.hero), .service-card, .project')];
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: .08, rootMargin: '0px 0px 35px 0px' });
    revealTargets.forEach(element => { element.dataset.reveal = ''; revealObserver.observe(element); });
    document.documentElement.classList.add('motion-ready');
  }

  const hero = document.querySelector('[data-motion-slider]');
  if (hero) {
    const media = hero.querySelector('.motion-hero-media');
    const images = [...media.querySelectorAll('img')];
    const count = hero.querySelector('[data-slide-count]');
    const caption = hero.querySelector('[data-slide-caption]');
    const prev = hero.querySelector('[data-slide-prev]');
    const next = hero.querySelector('[data-slide-next]');
    const controls = hero.querySelector('.motion-hero-controls');
    let index = 0;
    let timer = 0;
    let pointerStart = null;
    let paused = false;
    let visible = true;
    // Only the first image is in the markup's src; the rest load after the page (or when shown first).
    const hydrate = img => { if (img.dataset.src && !img.getAttribute('src')) img.src = img.dataset.src; };
    const setSlide = (target) => {
      index = (target + images.length) % images.length;
      images.forEach((img, position) => {
        img.classList.toggle('is-active', position === index);
        img.setAttribute('aria-hidden', String(position !== index));
        if (position === index) hydrate(img);
      });
      count.textContent = `${String(index + 1).padStart(2, '0')} / ${String(images.length).padStart(2, '0')}`;
      caption.textContent = images[index].dataset.caption || '';
    };
    const stop = () => { clearInterval(timer); timer = 0; };
    const start = () => {
      stop();
      if (!reduced.matches && !paused && visible && !document.hidden) timer = setInterval(() => setSlide(index + 1), 7500);
    };
    prev.addEventListener('click', () => { setSlide(index - 1); start(); });
    next.addEventListener('click', () => { setSlide(index + 1); start(); });
    controls.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        setSlide(index + (event.key === 'ArrowRight' ? 1 : -1));
        start();
      }
    });
    hero.addEventListener('pointerdown', event => {
      if (event.target.closest('a,button')) return;
      pointerStart = { x: event.clientX, y: event.clientY };
      hero.dataset.dragging = '';
    });
    hero.addEventListener('pointerup', event => {
      if (!pointerStart) return;
      const dx = event.clientX - pointerStart.x;
      const dy = event.clientY - pointerStart.y;
      if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy)) { setSlide(index + (dx < 0 ? 1 : -1)); start(); }
      pointerStart = null;
      delete hero.dataset.dragging;
    });
    hero.addEventListener('pointercancel', () => { pointerStart = null; delete hero.dataset.dragging; });
    hero.addEventListener('mouseenter', () => { paused = true; stop(); });
    hero.addEventListener('mouseleave', () => { paused = false; pointerStart = null; delete hero.dataset.dragging; start(); media.style.removeProperty('--hero-x'); media.style.removeProperty('--hero-y'); });
    hero.addEventListener('focusin', () => { paused = true; stop(); });
    hero.addEventListener('focusout', event => {
      if (hero.contains(event.relatedTarget)) return;
      paused = false;
      start();
    });
    if (finePointer.matches && !reduced.matches) {
      let pointerFrame = 0;
      hero.addEventListener('pointermove', event => {
        if (pointerFrame) return;
        pointerFrame = requestAnimationFrame(() => {
          pointerFrame = 0;
          const bounds = hero.getBoundingClientRect();
          const x = (event.clientX - bounds.left) / bounds.width - .5;
          const y = (event.clientY - bounds.top) / bounds.height - .5;
          media.style.setProperty('--hero-x', `${(-x * 13).toFixed(1)}px`);
          media.style.setProperty('--hero-y', `${(-y * 9).toFixed(1)}px`);
        });
      }, { passive: true });
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => { visible = entries[0]?.isIntersecting || false; start(); }, { threshold: .12 }).observe(hero);
    }
    if (document.readyState === 'complete') images.forEach(hydrate);
    else addEventListener('load', () => images.forEach(hydrate), { once: true });
    document.addEventListener('visibilitychange', start);
    reduced.addEventListener?.('change', start);
    setSlide(0);
    start();
  }

  if (finePointer.matches && !reduced.matches) {
    document.querySelectorAll('.button, .nav-cta').forEach(element => {
      element.addEventListener('pointermove', event => {
        const rect = element.getBoundingClientRect();
        const x = (event.clientX - rect.left - rect.width / 2) * .09;
        const y = (event.clientY - rect.top - rect.height / 2) * .09;
        element.style.transform = `translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0)`;
      });
      element.addEventListener('pointerleave', () => { element.style.transform = ''; });
    });
  }
})();
