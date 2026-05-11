/* ============================================================
   GaonKaam – Village Labour Connect
   Main JavaScript
   ============================================================ */

'use strict';

/* ── DOM Ready ───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initAlertDismiss();
  initToasts();
  initJobCardLinks();
  initFormEnhancements();
  initChatScroll();
  initConfirmActions();
  initProgressBars();
});

/* ── Navbar (mobile hamburger) ───────────────────────────── */
function initNavbar() {
  const ham  = document.querySelector('.hamburger');
  const nav  = document.querySelector('.navbar-links');
  if (!ham || !nav) return;

  ham.addEventListener('click', () => {
    nav.classList.toggle('open');
    ham.classList.toggle('open');
  });

  // Close when a link is clicked
  nav.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => nav.classList.remove('open'))
  );
}

/* ── Auto-dismiss alerts after 5s ───────────────────────── */
function initAlertDismiss() {
  document.querySelectorAll('.alert').forEach(el => {
    // Add close button
    const btn = document.createElement('button');
    btn.innerHTML = '×';
    btn.style.cssText = 'margin-left:auto;background:none;border:none;font-size:18px;cursor:pointer;opacity:0.6;line-height:1;';
    btn.addEventListener('click', () => fadeOut(el));
    el.style.cssText += ';display:flex;align-items:center;';
    el.appendChild(btn);

    // Auto dismiss
    setTimeout(() => fadeOut(el), 5000);
  });
}

function fadeOut(el) {
  el.style.transition = 'opacity 0.4s, max-height 0.4s, padding 0.4s, margin 0.4s';
  el.style.opacity = '0';
  el.style.maxHeight = '0';
  el.style.padding   = '0';
  el.style.margin    = '0';
  setTimeout(() => el.remove(), 450);
}

/* ── Toast notifications ─────────────────────────────────── */
function initToasts() {
  // Create container
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
}

window.showToast = function(message, type = '', duration = 3500) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast' + (type ? ' ' + type : '');
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.35s';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 380);
  }, duration);
};

/* ── Job cards – entire card is clickable ────────────────── */
function initJobCardLinks() {
  document.querySelectorAll('.job-card[data-href]').forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('click', e => {
      if (e.target.closest('a, button')) return; // don't override inner links/buttons
      window.location.href = card.dataset.href;
    });
  });
}

/* ── Form enhancements ───────────────────────────────────── */
function initFormEnhancements() {
  // Character counters for textareas
  document.querySelectorAll('textarea[maxlength]').forEach(ta => {
    const max = parseInt(ta.getAttribute('maxlength'));
    const counter = document.createElement('div');
    counter.style.cssText = 'font-size:11px;color:#8A7060;text-align:right;margin-top:3px;';
    ta.parentNode.insertBefore(counter, ta.nextSibling);
    const update = () => { counter.textContent = `${ta.value.length} / ${max}`; };
    ta.addEventListener('input', update);
    update();
  });

  // Auto-resize textareas
  document.querySelectorAll('textarea.form-input').forEach(ta => {
    ta.addEventListener('input', () => {
      ta.style.height = 'auto';
      ta.style.height = ta.scrollHeight + 'px';
    });
  });

  // Live wage calculator on job form
  const wage  = document.getElementById('id_daily_wage');
  const days  = document.getElementById('daysPreview');
  const total = document.getElementById('totalWagePreview');
  if (wage && total) {
    const daysInput = document.getElementById('id_workers_needed');
    const recalc = () => {
      const w = parseFloat(wage.value) || 0;
      if (days) days.textContent = daysInput ? daysInput.value : '?';
      total.textContent = 'Rs. ' + (w).toLocaleString('en-NP');
    };
    wage.addEventListener('input', recalc);
    if (daysInput) daysInput.addEventListener('input', recalc);
  }

  // Submit button loading state
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn && !btn.dataset.noLoad) {
        btn.disabled = true;
        const orig = btn.innerHTML;
        btn.innerHTML = '<span class="spinner"></span> ' + (btn.dataset.loadText || 'Please wait…');
        // Restore after 8s in case of server error
        setTimeout(() => { btn.disabled = false; btn.innerHTML = orig; }, 8000);
      }
    });
  });
}

/* ── Auto scroll chat to bottom ─────────────────────────── */
function initChatScroll() {
  const area = document.getElementById('messagesArea');
  if (area) {
    area.scrollTop = area.scrollHeight;
    // Keep scrolled to bottom as new messages appear
    const observer = new MutationObserver(() => {
      area.scrollTop = area.scrollHeight;
    });
    observer.observe(area, { childList: true });
  }
}

/* ── Confirm dangerous actions ───────────────────────────── */
function initConfirmActions() {
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm)) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  });
}

/* ── Animate progress bars on scroll ────────────────────── */
function initProgressBars() {
  const fills = document.querySelectorAll('.progress-fill[data-width]');
  if (!fills.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.width = entry.target.dataset.width + '%';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  fills.forEach(fill => {
    const w = fill.style.width;
    fill.dataset.width = parseInt(w);
    fill.style.width = '0';
    observer.observe(fill);
  });
}

/* ── Voice message recording ─────────────────────────────── */
let mediaRecorder = null;
let audioChunks   = [];
let recordingTimer = null;

window.startVoiceRecording = async function(btn) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks   = [];

    mediaRecorder.addEventListener('dataavailable', e => {
      if (e.data.size > 0) audioChunks.push(e.data);
    });

    mediaRecorder.start();
    btn.style.background = '#C1440E';
    btn.style.color = 'white';
    btn.title = 'Release to send';

    // Max 60 sec
    recordingTimer = setTimeout(() => stopVoiceRecording(btn), 60000);
  } catch (err) {
    showToast('Microphone access denied. Please allow microphone permission.', 'error');
  }
};

window.stopVoiceRecording = function(btn) {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') return;
  clearTimeout(recordingTimer);

  mediaRecorder.addEventListener('stop', () => {
    const blob = new Blob(audioChunks, { type: 'audio/webm' });
    const convId = document.getElementById('convId')?.value;
    if (!convId) return;

    const formData = new FormData();
    formData.append('voice_file', blob, 'voice.webm');
    formData.append('msg_type', 'voice');
    formData.append('content', '');
    formData.append('csrfmiddlewaretoken', getCsrf());

    fetch(`/messages/${convId}/send/`, { method: 'POST', body: formData })
      .then(r => r.json())
      .then(() => { window.location.reload(); })
      .catch(() => showToast('Voice send failed.', 'error'));
  });

  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach(t => t.stop());
  btn.style.background = '';
  btn.style.color = '';
  btn.title = 'Hold to record voice message';
  showToast('🎤 Voice message sent!', 'success');
};

/* ── AJAX send message (chat) ────────────────────────────── */
window.sendMessageAjax = function(e) {
  e.preventDefault();
  const form   = e.target;
  const input  = form.querySelector('#msgInput');
  const text   = input?.value.trim();
  const convId = document.getElementById('convId')?.value;
  if (!text || !convId) return;

  const data = new FormData();
  data.append('content', text);
  data.append('msg_type', 'text');
  data.append('csrfmiddlewaretoken', getCsrf());

  input.value = '';
  input.style.height = '';

  fetch(`/messages/${convId}/send/`, {
    method: 'POST',
    body: data,
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(r => r.json())
  .then(msg => appendMessage(msg, true))
  .catch(() => showToast('Message failed to send.', 'error'));
};

function appendMessage(msg, isSent) {
  const area = document.getElementById('messagesArea');
  if (!area) return;

  const wrapper = document.createElement('div');
  wrapper.style.cssText = `display:flex;gap:8px;max-width:70%;${isSent ? 'flex-direction:row-reverse;align-self:flex-end;' : 'align-self:flex-start;'}`;
  wrapper.className = 'fade-in';

  if (isSent) {
    wrapper.innerHTML = `
      <div>
        <div class="chat-bubble-sent">${escapeHtml(msg.content)}</div>
        <div class="chat-time" style="text-align:right;">${msg.time} ✓</div>
      </div>`;
  } else {
    const initials = msg.sender.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
    wrapper.innerHTML = `
      <div class="avatar avatar-sm">${initials}</div>
      <div>
        <div class="chat-bubble-recv">${escapeHtml(msg.content)}</div>
        <div class="chat-time">${msg.time}</div>
      </div>`;
  }

  area.appendChild(wrapper);
  area.scrollTop = area.scrollHeight;
}

/* ── Star rating widget ──────────────────────────────────── */
window.initStarRating = function(containerId, inputId) {
  const container = document.getElementById(containerId);
  const input     = document.getElementById(inputId);
  if (!container || !input) return;

  container.innerHTML = '';
  for (let i = 5; i >= 1; i--) {
    const lbl = document.createElement('label');
    lbl.innerHTML = '★';
    lbl.style.cssText = 'font-size:28px;cursor:pointer;color:#EDD9BC;transition:color 0.15s;';
    lbl.dataset.val = i;

    lbl.addEventListener('mouseover', () => highlight(container, i));
    lbl.addEventListener('mouseleave', () => highlight(container, parseInt(input.value) || 0));
    lbl.addEventListener('click', () => {
      input.value = i;
      highlight(container, i);
    });

    container.appendChild(lbl);
  }
  // Reverse so 5 is on left
  const labels = [...container.querySelectorAll('label')];
  labels.reverse().forEach(l => container.appendChild(l));
};

function highlight(container, val) {
  container.querySelectorAll('label').forEach(l => {
    l.style.color = parseInt(l.dataset.val) <= val ? '#E8A020' : '#EDD9BC';
  });
}

/* ── Review / rating submission ──────────────────────────── */
window.submitReview = function(jobId, reviewedUserId) {
  const rating  = document.getElementById('reviewRating')?.value;
  const comment = document.getElementById('reviewComment')?.value.trim();
  if (!rating) { showToast('Please select a star rating.', 'error'); return; }

  const data = new FormData();
  data.append('job', jobId);
  data.append('reviewed_user', reviewedUserId);
  data.append('rating', rating);
  data.append('comment', comment || '');
  data.append('csrfmiddlewaretoken', getCsrf());

  fetch('/jobs/review/', { method: 'POST', body: data, headers: { 'X-Requested-With': 'XMLHttpRequest' } })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        showToast('⭐ Review submitted! Thank you.', 'success');
        document.getElementById('reviewModal')?.classList.remove('show');
        setTimeout(() => window.location.reload(), 1200);
      } else {
        showToast(data.error || 'Could not submit review.', 'error');
      }
    })
    .catch(() => showToast('Review submission failed.', 'error'));
};

/* ── Modal helpers ───────────────────────────────────────── */
window.openModal = function(id) {
  const m = document.getElementById(id);
  if (m) { m.classList.add('show'); document.body.style.overflow = 'hidden'; }
};
window.closeModal = function(id) {
  const m = document.getElementById(id);
  if (m) { m.classList.remove('show'); document.body.style.overflow = ''; }
};
// Close on overlay click
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('show');
    document.body.style.overflow = '';
  }
});
// Close on Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.show').forEach(m => {
      m.classList.remove('show');
      document.body.style.overflow = '';
    });
  }
});

/* ── Helpers ─────────────────────────────────────────────── */
function getCsrf() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value
      || document.cookie.match(/csrftoken=([^;]+)/)?.[1]
      || '';
}

function escapeHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* ── Job search live filter ──────────────────────────────── */
(function() {
  const searchInput = document.getElementById('jobSearch');
  const jobCards    = document.querySelectorAll('.job-card-filterable');
  if (!searchInput || !jobCards.length) return;

  searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase();
    jobCards.forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(q) ? '' : 'none';
    });
  });
})();

/* ── Payment total calculator ────────────────────────────── */
(function() {
  const daysInput = document.getElementById('daysInput');
  const jobSelect = document.getElementById('jobSelect');
  const totalBox  = document.getElementById('totalBox');
  const totalAmt  = document.getElementById('totalAmt');
  const workerInp = document.getElementById('workerInput');

  if (!daysInput || !jobSelect) return;

  let wageMap = {};
  jobSelect.querySelectorAll('option[data-worker]').forEach(opt => {
    wageMap[opt.value] = { worker: opt.dataset.worker, wage: parseFloat(opt.dataset.wage) || 0 };
  });

  function recalc() {
    const sel  = wageMap[jobSelect.value];
    const days = parseFloat(daysInput.value) || 0;
    if (sel) {
      if (workerInp) workerInp.value = sel.worker;
      if (days > 0 && totalAmt && totalBox) {
        totalAmt.textContent = 'Rs. ' + (sel.wage * days).toLocaleString('en-NP');
        totalBox.style.display = '';
      }
    }
  }
  jobSelect.addEventListener('change', recalc);
  daysInput.addEventListener('input', recalc);
})();
