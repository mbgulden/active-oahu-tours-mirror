/**
 * Gallery Lightbox Modal
 * - Click thumbnail to open full-size image in overlay
 * - Desktop: keyboard nav (←/→/ESC), click outside to close
 * - Mobile: touch swipe (left/right) between images, tap to close
 * - Accessible: role="dialog", aria-modal, focus management, aria-label
 * - Groups images by data-lightbox attribute
 */
(function () {
  'use strict';

  // Wait for DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Find all lightbox triggers
    const triggers = document.querySelectorAll('[data-lightbox]');
    if (!triggers.length) return;

    let currentGroup = null;
    let currentIndex = 0;
    let touchStartX = 0;
    let touchEndX = 0;
    let lastFocused = null;

    // Inject lightbox DOM
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
    const lightboxTitle = overlay.querySelector('.aot-lightbox-title');
    const lightboxCounter = overlay.querySelector('.aot-lightbox-counter');
    const closeBtn = overlay.querySelector('.aot-lightbox-close');
    const prevBtn = overlay.querySelector('.aot-lightbox-prev');
    const nextBtn = overlay.querySelector('.aot-lightbox-next');

    function getGroup(groupName) {
      return Array.from(document.querySelectorAll(`[data-lightbox="${groupName}"]`));
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
      // Focus close button for keyboard users
      setTimeout(() => closeBtn.focus(), 50);
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
      const fullSrc = trigger.getAttribute('data-full') || img.src;
      const title = trigger.getAttribute('data-title') || img.alt || '';
      lightboxImg.src = fullSrc;
      lightboxImg.alt = title;
      lightboxTitle.textContent = title;
      lightboxCounter.textContent = `Image ${currentIndex + 1} of ${currentGroup.length}`;
      // Hide nav buttons if only one image
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

    // Attach click handlers to all triggers
    triggers.forEach((trigger, idx) => {
      const groupName = trigger.getAttribute('data-lightbox');
      // Find this trigger's index within its group
      const group = getGroup(groupName);
      const groupIndex = group.indexOf(trigger);
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        open(groupName, groupIndex);
      });
    });

    // Close button
    closeBtn.addEventListener('click', close);

    // Nav buttons
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      prev();
    });
    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      next();
    });

    // Click outside image to close
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) close();
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') next();
      else if (e.key === 'ArrowLeft') prev();
      else if (e.key === 'Tab') {
        // Simple focus trap: keep tab within the dialog
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

    // Touch swipe support for mobile
    overlay.addEventListener(
      'touchstart',
      (e) => {
        touchStartX = e.changedTouches[0].screenX;
      },
      { passive: true }
    );
    overlay.addEventListener(
      'touchend',
      (e) => {
        touchEndX = e.changedTouches[0].screenX;
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
