/* BikeShop – Main JS */

document.addEventListener('DOMContentLoaded', () => {

  // ── Cart AJAX ────────────────────────────────────────────
  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = form.querySelector('[type=submit]');
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      try {
        const res = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        const data = await res.json();
        if (data.success) {
          updateCartCount(data.cart_count);
          showToast(data.message, 'success');
        } else {
          showToast(data.error || 'Error adding to cart', 'danger');
        }
      } catch {
        showToast('Network error. Please try again.', 'danger');
      } finally {
        btn.disabled = false;
        btn.innerHTML = btn.dataset.label || 'Add to Cart';
      }
    });
  });

  // ── Cart Quantity Controls ───────────────────────────────
  document.querySelectorAll('.qty-control').forEach(ctrl => {
    const input = ctrl.querySelector('input');
    ctrl.querySelector('.qty-minus')?.addEventListener('click', () => {
      const v = parseInt(input.value) - 1;
      if (v >= 1) { input.value = v; triggerQtyUpdate(input); }
    });
    ctrl.querySelector('.qty-plus')?.addEventListener('click', () => {
      const max = parseInt(input.max || 9999);
      const v = parseInt(input.value) + 1;
      if (v <= max) { input.value = v; triggerQtyUpdate(input); }
    });
    input.addEventListener('change', () => triggerQtyUpdate(input));
  });

  function triggerQtyUpdate(input) {
    const form = input.closest('form');
    if (form) form.submit();
  }

  // ── Wishlist Toggle ──────────────────────────────────────
  document.querySelectorAll('.btn-wishlist').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const url = btn.dataset.url;
      if (!url) { window.location = '/login/'; return; }
      try {
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', getCsrf());
        const res = await fetch(url, { method: 'POST', body: fd, headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        const data = await res.json();
        btn.classList.toggle('active', data.in_wishlist);
        btn.querySelector('i').className = data.in_wishlist ? 'bi bi-heart-fill' : 'bi bi-heart';
        updateWishlistCount(data.wishlist_count);
        showToast(data.message, 'success');
      } catch { showToast('Please log in to use wishlist.', 'info'); }
    });
  });

  // ── Product Image Gallery ────────────────────────────────
  const mainImg = document.getElementById('mainProductImage');
  document.querySelectorAll('.thumb-gallery img').forEach(thumb => {
    thumb.addEventListener('click', () => {
      if (mainImg) {
        mainImg.src = thumb.dataset.full || thumb.src;
        document.querySelectorAll('.thumb-gallery img').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
      }
    });
  });

  // ── Toast ────────────────────────────────────────────────
  function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
      document.body.appendChild(container);
    }
    const id = 'toast_' + Date.now();
    const iconMap = { success: 'bi-check-circle-fill', danger: 'bi-exclamation-circle-fill', info: 'bi-info-circle-fill', warning: 'bi-exclamation-triangle-fill' };
    const icon = iconMap[type] || 'bi-info-circle-fill';
    container.insertAdjacentHTML('beforeend', `
      <div id="${id}" class="toast align-items-center text-bg-${type} border-0" role="alert">
        <div class="d-flex">
          <div class="toast-body"><i class="bi ${icon} me-2"></i>${message}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      </div>`);
    const el = document.getElementById(id);
    const toast = new bootstrap.Toast(el, { delay: 3500 });
    toast.show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
  }

  function getCsrf() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  }

  function updateCartCount(count) {
    document.querySelectorAll('.cart-count-badge').forEach(el => { el.textContent = count; el.style.display = count ? '' : 'none'; });
  }
  function updateWishlistCount(count) {
    document.querySelectorAll('.wishlist-count-badge').forEach(el => { el.textContent = count; el.style.display = count ? '' : 'none'; });
  }

  // ── Django messages → toasts ─────────────────────────────
  document.querySelectorAll('.django-message').forEach(el => {
    const type = el.dataset.type === 'error' ? 'danger' : (el.dataset.type || 'info');
    showToast(el.dataset.message, type);
  });

  // ── Sticky header shadow ──────────────────────────────────
  const navbar = document.querySelector('.navbar-main');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.style.boxShadow = window.scrollY > 10 ? '0 4px 20px rgba(0,0,0,.25)' : '';
    });
  }

  // ── Back to top ───────────────────────────────────────────
  const btt = document.getElementById('backToTop');
  if (btt) {
    window.addEventListener('scroll', () => { btt.style.display = window.scrollY > 300 ? 'flex' : 'none'; });
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }
});