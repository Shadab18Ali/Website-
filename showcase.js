(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

  if (finePointer && !reduceMotion) {
    const ring = document.createElement('div');
    ring.className = 'site-mouse-ring';
    ring.setAttribute('aria-hidden', 'true');
    document.body.append(ring);
    let targetX = -100;
    let targetY = -100;
    let currentX = -100;
    let currentY = -100;
    let running = false;
    const animate = () => {
      currentX += (targetX - currentX) * .28;
      currentY += (targetY - currentY) * .28;
      ring.style.left = `${currentX}px`;
      ring.style.top = `${currentY}px`;
      if (Math.abs(targetX - currentX) + Math.abs(targetY - currentY) > .3) requestAnimationFrame(animate);
      else running = false;
    };
    document.addEventListener('pointermove', event => {
      if (event.pointerType !== 'mouse') return;
      targetX = event.clientX;
      targetY = event.clientY;
      ring.classList.add('is-visible');
      ring.classList.toggle('is-hovering', !!event.target.closest('a,button,input,select,textarea'));
      ring.classList.toggle('is-over-showcase', !!event.target.closest('.showcase-stage'));
      if (!running) { running = true; requestAnimationFrame(animate); }
    }, { passive: true });
    document.addEventListener('pointerleave', () => ring.classList.remove('is-visible'));
  }

  document.querySelectorAll('[data-project-showcase]').forEach(gallery => {
    const stage = gallery.querySelector('.showcase-stage');
    const slides = [...gallery.querySelectorAll('.showcase-slide')];
    const thumbnails = [...gallery.querySelectorAll('.showcase-thumbnail')];
    const count = gallery.querySelector('[data-project-count]');
    const kind = gallery.querySelector('[data-project-kind]');
    const title = gallery.querySelector('[data-project-title]');
    const description = gallery.querySelector('[data-project-description]');
    const tags = gallery.querySelector('[data-project-tags]');
    const result = gallery.querySelector('[data-project-result]');
    const link = gallery.querySelector('[data-project-link]');
    const linkLabel = gallery.querySelector('[data-project-link-label]');
    const previous = gallery.querySelectorAll('[data-project-prev]');
    const next = gallery.querySelectorAll('[data-project-next]');
    let index = 0;
    let dragStart = null;
    const hydrate = slide => slide.querySelectorAll('img[data-src]').forEach(img => {
      if (img.dataset.srcset) img.srcset = img.dataset.srcset;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      img.removeAttribute('data-srcset');
    });
    const setProject = target => {
      index = (target + slides.length) % slides.length;
      const slide = slides[index];
      slides.forEach((item, position) => {
        item.classList.toggle('is-active', position === index);
        item.setAttribute('aria-hidden', String(position !== index));
        if (position === index) hydrate(item);
      });
      thumbnails.forEach((button, position) => button.setAttribute('aria-pressed', String(position === index)));
      stage.style.setProperty('--stage-color', slide.dataset.color);
      count.textContent = `${String(index + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      kind.textContent = slide.dataset.kind;
      title.textContent = slide.dataset.title;
      description.textContent = slide.dataset.description;
      if (result) result.textContent = slide.dataset.result || '';
      tags.replaceChildren(...slide.dataset.tags.split('|').map(label => {
        const chip = document.createElement('span');
        chip.textContent = label;
        return chip;
      }));
      link.href = slide.dataset.link;
      if (linkLabel) linkLabel.textContent = slide.dataset.linkLabel || 'Explore this project';
      link.setAttribute('aria-label', `${linkLabel ? linkLabel.textContent : 'Explore'}: ${slide.dataset.title}`);
    };
    previous.forEach(button => button.addEventListener('click', () => setProject(index - 1)));
    next.forEach(button => button.addEventListener('click', () => setProject(index + 1)));
    thumbnails.forEach((button, position) => button.addEventListener('click', () => setProject(position)));
    gallery.addEventListener('keydown', event => {
      if (!event.target.closest('.showcase-navigation,.showcase-thumbnails,.showcase-stage-controls')) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        setProject(index + (event.key === 'ArrowRight' ? 1 : -1));
        thumbnails[index]?.focus();
      }
    });
    stage.addEventListener('pointerdown', event => {
      if (event.target.closest('a,button')) return;
      dragStart = { x: event.clientX, y: event.clientY };
    });
    stage.addEventListener('pointerup', event => {
      if (!dragStart) return;
      const dx = event.clientX - dragStart.x;
      const dy = event.clientY - dragStart.y;
      if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy)) setProject(index + (dx < 0 ? 1 : -1));
      dragStart = null;
    });
    stage.addEventListener('pointercancel', () => { dragStart = null; });
    if (finePointer && !reduceMotion) {
      const cursor = document.createElement('div');
      cursor.className = 'showcase-cursor';
      cursor.textContent = 'DRAG ↔';
      cursor.setAttribute('aria-hidden', 'true');
      document.body.append(cursor);
      stage.addEventListener('pointerenter', () => cursor.classList.add('is-visible'));
      stage.addEventListener('pointerleave', () => {
        cursor.classList.remove('is-visible');
        stage.style.removeProperty('--tilt-x');
        stage.style.removeProperty('--tilt-y');
        stage.style.removeProperty('--spot-x');
        stage.style.removeProperty('--spot-y');
        dragStart = null;
      });
      stage.addEventListener('pointermove', event => {
        if (event.pointerType !== 'mouse') return;
        cursor.style.left = `${event.clientX}px`;
        cursor.style.top = `${event.clientY}px`;
        const bounds = stage.getBoundingClientRect();
        const x = (event.clientX - bounds.left) / bounds.width;
        const y = (event.clientY - bounds.top) / bounds.height;
        stage.style.setProperty('--tilt-x', `${((x - .5) * 8).toFixed(2)}deg`);
        stage.style.setProperty('--tilt-y', `${((.5 - y) * 6).toFixed(2)}deg`);
        stage.style.setProperty('--spot-x', `${(x * 100).toFixed(1)}%`);
        stage.style.setProperty('--spot-y', `${(y * 100).toFixed(1)}%`);
      }, { passive: true });
    }
    setProject(0);
    if (document.readyState === 'complete') slides.forEach(hydrate);
    else addEventListener('load', () => slides.forEach(hydrate), { once: true });
  });
})();
