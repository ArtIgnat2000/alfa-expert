/* Сайт экспертной организации «АЛЬФА» — интерфейсные скрипты */
(function () {
  'use strict';

  /* ---------- Мобильное меню ---------- */
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('mainnav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) burger.click();
    });
  }

  /* ---------- Маска телефона ---------- */
  function maskPhone(el) {
    el.addEventListener('input', function () {
      var d = el.value.replace(/\D/g, '');
      if (d[0] === '8') d = '7' + d.slice(1);
      if (d[0] !== '7') d = '7' + d;
      d = d.slice(0, 11);
      var out = '+7';
      if (d.length > 1) out += ' (' + d.slice(1, 4);
      if (d.length >= 5) out += ') ' + d.slice(4, 7);
      if (d.length >= 8) out += '-' + d.slice(7, 9);
      if (d.length >= 10) out += '-' + d.slice(9, 11);
      el.value = out;
    });
    el.addEventListener('focus', function () { if (!el.value) el.value = '+7 '; });
    el.addEventListener('blur', function () { if (el.value.replace(/\D/g, '').length < 2) el.value = ''; });
  }
  document.querySelectorAll('input[type="tel"]').forEach(maskPhone);

  /* ---------- Файлы ---------- */
  var MAX_FILES = 10, MAX_SIZE = 20 * 1024 * 1024;
  document.querySelectorAll('[data-files]').forEach(function (input) {
    var list = input.closest('.field').querySelector('[data-file-list]');
    input.addEventListener('change', function () {
      var files = Array.prototype.slice.call(input.files);
      var errors = [];
      if (files.length > MAX_FILES) errors.push('Можно приложить не более ' + MAX_FILES + ' файлов.');
      files.forEach(function (f) {
        if (f.size > MAX_SIZE) errors.push('Файл «' + f.name + '» превышает 20 МБ.');
      });
      if (errors.length) {
        list.innerHTML = '<span style="color:#A33B35">' + errors.join(' ') + '</span>';
        input.value = '';
        return;
      }
      if (!files.length) { list.innerHTML = ''; return; }
      var total = files.reduce(function (s, f) { return s + f.size; }, 0);
      list.innerHTML = 'Выбрано файлов: <b>' + files.length + '</b> (' +
        (total / 1048576).toFixed(1) + ' МБ)<br>' +
        files.map(function (f) { return '• ' + f.name; }).join('<br>');
    });
    // drag & drop
    var drop = input.closest('.file-drop');
    if (drop) {
      ['dragenter', 'dragover'].forEach(function (ev) {
        drop.addEventListener(ev, function (e) { e.preventDefault(); drop.style.borderColor = '#B8944D'; });
      });
      ['dragleave', 'drop'].forEach(function (ev) {
        drop.addEventListener(ev, function (e) { e.preventDefault(); drop.style.borderColor = ''; });
      });
      drop.addEventListener('drop', function (e) {
        if (e.dataTransfer && e.dataTransfer.files.length) {
          input.files = e.dataTransfer.files;
          input.dispatchEvent(new Event('change'));
        }
      });
    }
  });

  /* ---------- Валидация и отправка ---------- */
  function setError(field, on) {
    if (!field) return;
    field.classList.toggle('has-error', !!on);
  }

  document.querySelectorAll('[data-form]').forEach(function (form) {
    var status = form.querySelector('[data-status]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, firstBad = null;

      form.querySelectorAll('input[required], textarea[required], select[required]').forEach(function (el) {
        if (el.type === 'checkbox') return;
        var field = el.closest('.field');
        var bad = !el.value.trim();
        if (!bad && el.type === 'tel') bad = el.value.replace(/\D/g, '').length !== 11;
        if (!bad && el.type === 'email' && el.value) bad = !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value);
        setError(field, bad);
        if (bad) { ok = false; firstBad = firstBad || el; }
      });

      var email = form.querySelector('input[type="email"]');
      if (email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value)) {
        setError(email.closest('.field'), true); ok = false; firstBad = firstBad || email;
      }

      var consent = form.querySelector('[data-consent]');
      if (consent && !consent.checked) {
        ok = false; firstBad = firstBad || consent;
        status.className = 'form__status is-err';
        status.textContent = 'Необходимо согласие на обработку персональных данных.';
      }

      if (!ok) {
        if (status && (!consent || consent.checked)) {
          status.className = 'form__status is-err';
          status.textContent = 'Проверьте отмеченные поля — не все данные заполнены корректно.';
        }
        if (firstBad) { firstBad.focus(); firstBad.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
        return;
      }

      /* ДЕМОНСТРАЦИОННАЯ ОТПРАВКА.
         Для боевого сайта: заменить блок ниже на fetch() к обработчику,
         например /api/lead.php (FormData поддерживает вложения). */
      var btn = form.querySelector('button[type="submit"]');
      var txt = btn.textContent;
      btn.disabled = true; btn.textContent = 'Отправляем…';

      setTimeout(function () {
        btn.disabled = false; btn.textContent = txt;
        status.className = 'form__status is-ok';
        status.textContent = 'Заявка отправлена. Эксперт свяжется с вами в течение 1 рабочего дня. (Демонстрационный режим: подключите серверный обработчик формы.)';
        form.reset();
        var fl = form.querySelector('[data-file-list]'); if (fl) fl.innerHTML = '';
        status.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }, 700);
    });

    form.addEventListener('input', function (e) {
      var f = e.target.closest('.field');
      if (f && f.classList.contains('has-error') && e.target.value.trim()) setError(f, false);
    });
  });

  /* ---------- Подсветка активного раздела на главной ---------- */
  var isIndex = /(^|\/)(index\.html)?$/.test(location.pathname.split('/').pop() || 'index.html');
  if (isIndex && 'IntersectionObserver' in window) {
    var map = {};
    document.querySelectorAll('.nav a[href*="#"]').forEach(function (a) {
      var id = a.getAttribute('href').split('#')[1];
      if (id) map[id] = a;
    });
  }
})();
