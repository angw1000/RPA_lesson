// 銷售系統前端邏輯 - Selenium 教學練習網站
// API 基礎 URL (部署後改為實際 Workers URL)
const API_BASE = 'https://api.rpa-learn.angw1000.work';

// ===== 工具函式 =====

/**
 * 從 URL search params 取得 student_id
 * @returns {string}
 */
function getStudentId() {
  const params = new URLSearchParams(window.location.search);
  return params.get('student_id') || '';
}

/**
 * 回傳 NT$ x,xxx 格式的貨幣字串
 * @param {number} num
 * @returns {string}
 */
function formatCurrency(num) {
  return 'NT$ ' + Number(num).toLocaleString('zh-TW', { minimumFractionDigits: 0 });
}

/**
 * 顯示訊息
 * @param {string} containerId
 * @param {string} message
 * @param {'success'|'error'} type
 */
function showMessage(containerId, message, type) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.className = type === 'success' ? 'success-msg' : 'error-msg';
  el.textContent = message;
  el.style.display = 'block';
}

// ===== 貨品相關 =====

/** 產品單價快取 */
const productPriceCache = {};

/**
 * 從 API 載入貨品清單，填入 select options
 */
async function loadProducts() {
  const select = document.getElementById('sales-product');
  if (!select) return;

  try {
    const res = await fetch(API_BASE + '/api/products');
    const json = await res.json();
    if (!json.success) throw new Error(json.error || '載入失敗');

    select.innerHTML = '<option value="">-- 請選擇貨品 --</option>';
    json.data.forEach(function (p) {
      productPriceCache[p.product_id] = p.unit_price;
      const opt = document.createElement('option');
      opt.value = p.product_id;
      opt.textContent = p.product_id + ' - ' + p.name + '  (NT$ ' + p.unit_price + ')';
      opt.dataset.price = p.unit_price;
      select.appendChild(opt);
    });
  } catch (err) {
    select.innerHTML = '<option value="">載入失敗，請重新整理</option>';
    console.error('loadProducts error:', err);
  }
}

/**
 * 更新單價與小計顯示
 */
function updatePriceDisplay() {
  const select = document.getElementById('sales-product');
  const qtyInput = document.getElementById('sales-quantity');
  const priceEl = document.getElementById('display-price');
  const subtotalEl = document.getElementById('display-subtotal');
  if (!select || !priceEl || !subtotalEl) return;

  const selectedOpt = select.options[select.selectedIndex];
  const price = selectedOpt && selectedOpt.dataset.price ? parseFloat(selectedOpt.dataset.price) : null;
  const qty = parseInt(qtyInput ? qtyInput.value : 1, 10) || 1;

  if (price !== null) {
    priceEl.textContent = price.toLocaleString('zh-TW');
    subtotalEl.textContent = (price * qty).toLocaleString('zh-TW');
  } else {
    priceEl.textContent = '--';
    subtotalEl.textContent = '--';
  }
}

// ===== 銷售紀錄 =====

/**
 * 送出銷售紀錄 POST /api/sales
 * @param {object} formData
 */
async function submitSale(formData) {
  const res = await fetch(API_BASE + '/api/sales', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  });
  return res.json();
}

/**
 * 載入銷售紀錄 GET /api/sales?student_id=xxx
 * @param {string} studentId
 */
async function loadSales(studentId) {
  const res = await fetch(API_BASE + '/api/sales?student_id=' + encodeURIComponent(studentId));
  return res.json();
}

/**
 * 刪除銷售紀錄 DELETE /api/sales/:id?student_id=xxx
 * @param {number} id
 * @param {string} studentId
 */
async function deleteSale(id, studentId) {
  const res = await fetch(
    API_BASE + '/api/sales/' + id + '?student_id=' + encodeURIComponent(studentId),
    { method: 'DELETE' }
  );
  return res.json();
}

// ===== 頁面邏輯 =====

/**
 * 輸入頁初始化
 */
async function initInputPage() {
  const studentId = getStudentId();
  if (!studentId) {
    window.location.href = '/sales/index.html';
    return;
  }

  // 顯示學生代號
  const displayEl = document.getElementById('display-student-id');
  if (displayEl) displayEl.textContent = studentId;

  // 設定導航連結
  const navQuery = document.getElementById('nav-to-query');
  if (navQuery) navQuery.href = '/sales/query.html?student_id=' + encodeURIComponent(studentId);

  // 設定預設日期為今天
  const dateInput = document.getElementById('sales-date');
  if (dateInput) {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    dateInput.value = yyyy + '-' + mm + '-' + dd;
  }

  // 載入貨品
  await loadProducts();

  // 貨品/數量變更時更新顯示
  const productSelect = document.getElementById('sales-product');
  const qtyInput = document.getElementById('sales-quantity');
  if (productSelect) productSelect.addEventListener('change', updatePriceDisplay);
  if (qtyInput) qtyInput.addEventListener('input', updatePriceDisplay);

  // 載入最近銷售紀錄
  await refreshRecentSales(studentId);

  // 表單送出
  const form = document.getElementById('sales-form');
  if (form) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const productId = productSelect ? productSelect.value : '';
      const qty = qtyInput ? parseInt(qtyInput.value, 10) : 1;
      const saleDate = dateInput ? dateInput.value : '';

      if (!productId) { showMessage('sales-message', '請選擇貨品', 'error'); return; }
      if (!qty || qty < 1) { showMessage('sales-message', '請輸入有效數量', 'error'); return; }
      if (!saleDate) { showMessage('sales-message', '請選擇銷售日期', 'error'); return; }

      const submitBtn = document.getElementById('sales-submit');
      if (submitBtn) submitBtn.disabled = true;

      try {
        const json = await submitSale({ student_id: studentId, product_id: productId, quantity: qty, sale_date: saleDate });
        if (json.success) {
          const subtotal = json.data && json.data.total_price ? formatCurrency(json.data.total_price) : '';
          showMessage('sales-message', '✅ 銷售紀錄新增成功！' + (subtotal ? '  小計: ' + subtotal : ''), 'success');
          form.reset();
          if (dateInput) {
            const today = new Date();
            dateInput.value = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
          }
          updatePriceDisplay();
          await refreshRecentSales(studentId);
        } else {
          showMessage('sales-message', '❌ 新增失敗: ' + (json.error || json.message || '未知錯誤'), 'error');
        }
      } catch (err) {
        showMessage('sales-message', '❌ 連線失敗: ' + err.message, 'error');
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }
}

/**
 * 刷新最近銷售紀錄 (輸入頁，最近 5 筆)
 */
async function refreshRecentSales(studentId) {
  const tbody = document.getElementById('recent-sales');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#888">載入中...</td></tr>';
  try {
    const json = await loadSales(studentId);
    if (!json.success) throw new Error(json.error || '載入失敗');
    const records = (json.data || []).slice(0, 5);
    if (records.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#888">目前沒有銷售紀錄</td></tr>';
      return;
    }
    tbody.innerHTML = '';
    records.forEach(function (r, i) {
      const tr = document.createElement('tr');
      tr.innerHTML = [
        '<td>' + (i + 1) + '</td>',
        '<td>' + escHtml(r.name || '') + '</td>',
        '<td>' + r.quantity + '</td>',
        '<td>' + formatCurrency(r.unit_price) + '</td>',
        '<td>' + formatCurrency(r.total_price) + '</td>',
        '<td>' + escHtml(r.sale_date || '') + '</td>',
      ].join('');
      tbody.appendChild(tr);
    });
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#e74c3c">載入失敗: ' + escHtml(err.message) + '</td></tr>';
  }
}

/**
 * 查詢頁初始化
 */
async function initQueryPage() {
  const studentId = getStudentId();
  if (!studentId) {
    window.location.href = '/sales/index.html';
    return;
  }

  const displayEl = document.getElementById('display-student-id');
  if (displayEl) displayEl.textContent = studentId;

  const navInput = document.getElementById('nav-to-input');
  if (navInput) navInput.href = '/sales/input.html?student_id=' + encodeURIComponent(studentId);

  await refreshQueryTable(studentId);

  const btnRefresh = document.getElementById('btn-refresh');
  if (btnRefresh) {
    btnRefresh.addEventListener('click', function () { refreshQueryTable(studentId); });
  }
}

/**
 * 刷新查詢頁表格
 */
async function refreshQueryTable(studentId) {
  const tbody = document.getElementById('sales-tbody');
  const countEl = document.getElementById('sales-count');
  const totalEl = document.getElementById('sales-total');
  if (!tbody) return;

  tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:#888">載入中...</td></tr>';
  if (countEl) countEl.textContent = '--';
  if (totalEl) totalEl.textContent = '--';

  try {
    const json = await loadSales(studentId);
    if (!json.success) throw new Error(json.error || '載入失敗');
    const records = json.data || [];

    if (records.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:#888">目前沒有銷售紀錄</td></tr>';
      if (countEl) countEl.textContent = '0';
      if (totalEl) totalEl.textContent = formatCurrency(0);
      return;
    }

    tbody.innerHTML = '';
    let grandTotal = 0;
    records.forEach(function (r, i) {
      grandTotal += Number(r.total_price || 0);
      const tr = document.createElement('tr');
      tr.innerHTML = [
        '<td>' + (i + 1) + '</td>',
        '<td>' + escHtml(r.product_id || '') + '</td>',
        '<td>' + escHtml(r.name || '') + '</td>',
        '<td>' + r.quantity + '</td>',
        '<td>' + formatCurrency(r.unit_price) + '</td>',
        '<td>' + formatCurrency(r.total_price) + '</td>',
        '<td>' + escHtml(r.sale_date || '') + '</td>',
        '<td><button class="btn-delete danger small" data-id="' + r.id + '">刪除</button></td>',
      ].join('');
      tbody.appendChild(tr);
    });

    if (countEl) countEl.textContent = records.length;
    if (totalEl) totalEl.textContent = formatCurrency(grandTotal);

    // 綁定刪除按鈕
    tbody.querySelectorAll('.btn-delete').forEach(function (btn) {
      btn.addEventListener('click', async function () {
        const id = this.dataset.id;
        if (!confirm('確定要刪除這筆銷售紀錄嗎？')) return;
        try {
          const json = await deleteSale(id, studentId);
          if (json.success) {
            await refreshQueryTable(studentId);
          } else {
            alert('刪除失敗: ' + (json.error || json.message || '未知錯誤'));
          }
        } catch (err) {
          alert('連線失敗: ' + err.message);
        }
      });
    });
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:#e74c3c">載入失敗: ' + escHtml(err.message) + '</td></tr>';
  }
}

/**
 * HTML 特殊字元跳脫（防止 XSS）
 */
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ===== 頁面初始化 =====
document.addEventListener('DOMContentLoaded', function init() {
  const path = window.location.pathname;
  if (path.includes('input.html')) {
    initInputPage();
  } else if (path.includes('query.html')) {
    initQueryPage();
  }
});
