/**
 * Cloudflare Workers - 貨品銷售系統 API
 * Selenium 教學練習網站後端
 */

const ALLOWED_ORIGINS = [
  'https:/rpa-learn.angw1000.work',
  'https://www.rpa-learn.angw1000.work',
];

/**
 * 建立 CORS Headers
 * @param {Request} request
 * @returns {Object}
 */
function getCorsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  // 允許正式域名及 localhost (開發用)
  const isAllowed =
    ALLOWED_ORIGINS.includes(origin) ||
    /^http:\/\/localhost(:\d+)?$/.test(origin) ||
    /^http:\/\/127\.0\.0\.1(:\d+)?$/.test(origin);

  return {
    'Access-Control-Allow-Origin': isAllowed ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

/**
 * 回傳 JSON 回應
 */
function jsonResponse(data, status, corsHeaders) {
  return new Response(JSON.stringify(data), {
    status: status || 200,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders,
    },
  });
}

export default {
  async fetch(request, env) {
    const corsHeaders = getCorsHeaders(request);

    // OPTIONS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    try {
      // GET /api/products
      if (path === '/api/products' && method === 'GET') {
        const { results } = await env.DB.prepare(
          'SELECT product_id, name, unit_price FROM products ORDER BY product_id'
        ).all();
        return jsonResponse({ success: true, data: results }, 200, corsHeaders);
      }

      // POST /api/sales
      if (path === '/api/sales' && method === 'POST') {
        const body = await request.json();
        const { student_id, product_id, quantity, sale_date } = body;

        // 驗證必填欄位
        if (!student_id || !product_id || !quantity || !sale_date) {
          return jsonResponse(
            { success: false, error: '缺少必填欄位: student_id, product_id, quantity, sale_date' },
            400,
            corsHeaders
          );
        }
        if (!Number.isInteger(Number(quantity)) || Number(quantity) < 1) {
          return jsonResponse({ success: false, error: '數量必須為正整數' }, 400, corsHeaders);
        }

        // 查詢單價
        const product = await env.DB.prepare(
          'SELECT unit_price FROM products WHERE product_id = ?'
        ).bind(product_id).first();

        if (!product) {
          return jsonResponse({ success: false, error: '找不到指定貨品' }, 404, corsHeaders);
        }

        const total_price = product.unit_price * Number(quantity);

        const result = await env.DB.prepare(
          'INSERT INTO sales (student_id, product_id, quantity, total_price, sale_date) VALUES (?, ?, ?, ?, ?)'
        ).bind(student_id, product_id, Number(quantity), total_price, sale_date).run();

        return jsonResponse(
          {
            success: true,
            message: '銷售紀錄新增成功',
            data: { id: result.meta.last_row_id, total_price },
          },
          201,
          corsHeaders
        );
      }

      // GET /api/sales?student_id=xxx
      if (path === '/api/sales' && method === 'GET') {
        const studentId = url.searchParams.get('student_id');
        if (!studentId) {
          return jsonResponse({ success: false, error: '缺少 student_id 參數' }, 400, corsHeaders);
        }

        const { results } = await env.DB.prepare(
          `SELECT s.id, s.student_id, s.product_id, p.name, s.quantity,
                  p.unit_price, s.total_price, s.sale_date, s.created_at
           FROM sales s
           JOIN products p ON s.product_id = p.product_id
           WHERE s.student_id = ?
           ORDER BY s.created_at DESC`
        ).bind(studentId).all();

        return jsonResponse({ success: true, data: results }, 200, corsHeaders);
      }

      // DELETE /api/sales/:id?student_id=xxx
      const deleteMatch = path.match(/^\/api\/sales\/(\d+)$/);
      if (deleteMatch && method === 'DELETE') {
        const id = parseInt(deleteMatch[1], 10);
        const studentId = url.searchParams.get('student_id');

        if (!studentId) {
          return jsonResponse({ success: false, error: '缺少 student_id 參數' }, 400, corsHeaders);
        }

        // 安全驗證：只能刪除自己的紀錄
        const result = await env.DB.prepare(
          'DELETE FROM sales WHERE id = ? AND student_id = ?'
        ).bind(id, studentId).run();

        if (result.meta.changes === 0) {
          return jsonResponse({ success: false, error: '找不到指定紀錄或無權限刪除' }, 404, corsHeaders);
        }

        return jsonResponse({ success: true, message: '銷售紀錄已刪除' }, 200, corsHeaders);
      }

      // 404
      return jsonResponse({ success: false, error: '找不到指定路徑' }, 404, corsHeaders);

    } catch (err) {
      console.error('API Error:', err);
      return jsonResponse(
        { success: false, error: '伺服器內部錯誤', message: err.message },
        500,
        corsHeaders
      );
    }
  },
};
