/**
 * Gallery Lightbox Modal
 * - Click thumbnail to open full-size image in overlay
 * - Desktop: keyboard nav (←/→/ESC), click outside to close
 * - Mobile: touch swipe (left/right) between images, tap to close
 * - Accessible: role="dialog", aria-modal, focus management, aria-label
 * - Groups images by data-lightbox attribute
 * - Loads full-size image from /wp-content/uploads/_lightbox/ (falls back to thumbnail)
 */
(function () {
  'use strict';

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    const triggers = document.querySelectorAll('[data-lightbox]');
    if (!triggers.length) return;

    let currentGroup = null;
    let currentIndex = 0;
    let touchStartX = 0;
    let lastFocused = null;

    const overlay = document.createElement('div');
    overlay.id = 'aot-lightbox';
    overlay.className = 'aot-lightbox';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Image gallery viewer');
    overlay.setAttribute('hidden', '');
    overlay.innerHTML = `
      <button class="aot-lightbox-close" type="button" aria-label="Close gallery">&times;</button>
      <button class="aot-lightbox-prev" type="button" aria-label="Previous image">&#10094;</button>
      <button class="aot-lightbox-next" type="button" aria-label="Next image">&#10095;</button>
      <div class="aot-lightbox-content">
        <img class="aot-lightbox-img" alt="" />
        <div class="aot-lightbox-caption">
          <span class="aot-lightbox-title"></span>
          <span class="aot-lightbox-counter"></span>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    const lightboxImg = overlay.querySelector('.aot-lightbox-img');
    lightboxImg.addEventListener('error', function handleImgError() {
      const trigger = currentGroup && currentGroup[currentIndex];
      if (trigger) {
        const img = trigger.querySelector('img');
        if (img && img.src && lightboxImg.src !== img.src) {
          lightboxImg.src = img.src;
        }
      }
    });
    const lightboxTitle = overlay.querySelector('.aot-lightbox-title');
    const lightboxCounter = overlay.querySelector('.aot-lightbox-counter');
    const closeBtn = overlay.querySelector('.aot-lightbox-close');
    const prevBtn = overlay.querySelector('.aot-lightbox-prev');
    const nextBtn = overlay.querySelector('.aot-lightbox-next');

    function getGroup(groupName) {
      return Array.from(document.querySelectorAll('[data-lightbox="' + groupName + '"]'));
    }

    function open(groupName, index) {
      const group = getGroup(groupName);
      if (!group.length) return;
      currentGroup = group;
      currentIndex = index;
      lastFocused = document.activeElement;
      show();
      overlay.removeAttribute('hidden');
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      setTimeout(function () { closeBtn.focus(); }, 50);
    }

    function close() {
      overlay.classList.remove('open');
      overlay.setAttribute('hidden', '');
      document.body.style.overflow = '';
      if (lastFocused && typeof lastFocused.focus === 'function') {
        lastFocused.focus();
      }
    }

    function show() {
      const trigger = currentGroup[currentIndex];
      const img = trigger.querySelector('img');
      let fullSrc = trigger.getAttribute('data-full');
      if (!fullSrc) {
        const thumbSrc = img.getAttribute('src') || img.src;
        // Strip dimensions suffix (e.g. -115x115)
        const noDims = thumbSrc.replace(/-\d+x\d+(?=\.\w+$)/, '');
        // Use just the filename to avoid per-year/month duplicate dirs
        const filename = noDims.split('/').pop();
        fullSrc = '/wp-content/uploads/_lightbox/' + filename;
      }
      const title = trigger.getAttribute('data-title') || img.alt || '';
      lightboxImg.src = fullSrc;
      lightboxImg.alt = title;
      lightboxTitle.textContent = title;
      lightboxCounter.textContent = 'Image ' + (currentIndex + 1) + ' of ' + currentGroup.length;
      const single = currentGroup.length <= 1;
      prevBtn.style.display = single ? 'none' : '';
      nextBtn.style.display = single ? 'none' : '';
    }

    function next() {
      if (!currentGroup) return;
      currentIndex = (currentIndex + 1) % currentGroup.length;
      show();
    }

    function prev() {
      if (!currentGroup) return;
      currentIndex = (currentIndex - 1 + currentGroup.length) % currentGroup.length;
      show();
    }

    triggers.forEach(function (trigger) {
      const groupName = trigger.getAttribute('data-lightbox');
      const group = getGroup(groupName);
      const groupIndex = group.indexOf(trigger);
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        open(groupName, groupIndex);
      });
    });

    closeBtn.addEventListener('click', close);

    prevBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      prev();
    });
    nextBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      next();
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });

    document.addEventListener('keydown', function (e) {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') next();
      else if (e.key === 'ArrowLeft') prev();
      else if (e.key === 'Tab') {
        const focusable = [closeBtn, prevBtn, nextBtn];
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    overlay.addEventListener(
      'touchstart',
      function (e) {
        touchStartX = e.changedTouches[0].screenX;
      },
      { passive: true }
    );
    overlay.addEventListener(
      'touchend',
      function (e) {
        const touchEndX = e.changedTouches[0].screenX;
        const dx = touchEndX - touchStartX;
        const threshold = 50;
        if (Math.abs(dx) > threshold) {
          if (dx < 0) next();
          else prev();
        }
      },
      { passive: true }
    );
  }
})();
