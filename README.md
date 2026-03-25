# 🐍 Selenium 教學練習網站

> Python + Selenium 自動化測試教學實作平台

## 🌐 網站網址

<https://angw1000.work>

## 📋 功能列表

### Selenium 基礎練習

| 頁面 | 練習內容 |
|------|----------|
| 🖱️ Click 練習 | 按鈕、超連結、Checkbox、Radio、Select、雙擊、右鍵 |
| ⌨️ SendKeys 練習 | 文字、密碼、Textarea、日期、數字、鍵盤按鍵 |
| 📋 表單操作 | 完整表單填寫與送出驗證 |
| ⚠️ Alert 處理 | Alert、Confirm、Prompt、延遲 Alert、連續 Alert、自訂 Modal |

### 貨品銷售系統

- 🛒 貨品銷售輸入：選擇貨品、輸入數量、自動計算金額、送出紀錄
- 🔍 銷售紀錄查詢：查看、刪除、統計（最多同時 30 位學生操作）

## 🏗️ 技術架構

| 層級 | 技術 | 說明 |
|------|------|------|
| 前端 | HTML + CSS + Vanilla JS | 靜態練習頁面 |
| 託管 | Cloudflare Pages | 靜態網站託管 |
| 後端 API | Cloudflare Workers | Serverless REST API |
| 資料庫 | Cloudflare D1 (SQLite) | 銷售資料儲存 |
| 域名/CDN | Cloudflare | DNS + CDN |

## 📁 專案目錄結構

```
RPA_lesson/
├── public/                    # 靜態頁面 (Cloudflare Pages)
│   ├── index.html             # 首頁導航
│   ├── click.html             # Click 練習
│   ├── sendkeys.html          # SendKeys 練習
│   ├── form.html              # 表單操作練習
│   ├── alert.html             # Alert 處理練習
│   ├── sales/
│   │   ├── index.html         # 銷售系統入口（輸入學生代號）
│   │   ├── input.html         # 貨品銷售輸入頁面
│   │   └── query.html         # 貨品銷售查詢頁面
│   ├── css/
│   │   └── style.css          # 全站共用樣式
│   └── js/
│       └── sales.js           # 銷售系統前端邏輯 (Fetch API)
│
├── workers/                   # Cloudflare Workers (後端 API)
│   ├── src/
│   │   └── index.js           # API 路由與邏輯
│   ├── schema.sql             # D1 資料表結構與初始資料
│   ├── wrangler.toml          # Workers 設定檔
│   └── package.json
│
├── examples/                  # 學生 Selenium 練習範例程式碼
│   ├── 01_click_practice.py
│   ├── 02_sendkeys_practice.py
│   ├── 03_form_practice.py
│   ├── 04_alert_practice.py
│   └── 05_sales_system.py
│
└── README.md
```

## 🚀 部署步驟

### 前置需求

- Node.js v18+
- Wrangler CLI：`npm install -g wrangler`
- Cloudflare 帳號（已綁定域名 `angw1000.work`）
- GitHub 帳號

### Step 1: 部署靜態頁面 (Cloudflare Pages)

1. 登入 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 進入 **Pages** → **Create a project** → **Connect to Git**
3. 選擇本 Repository，設定：
   - **Build output directory**: `public`
   - **Build command**: （留空，無需建置）
4. 點擊 **Save and Deploy**
5. 在 **Custom domains** 中綁定 `angw1000.work`

### Step 2: 建立 D1 資料庫

```bash
# 登入 Cloudflare
wrangler login

# 建立 D1 資料庫
wrangler d1 create selenium-sales-db

# 複製輸出的 database_id，填入 workers/wrangler.toml 的 database_id 欄位

# 初始化資料表與貨品資料
wrangler d1 execute selenium-sales-db --file=workers/schema.sql
```

### Step 3: 部署 Workers API

```bash
cd workers

# 部署至 Cloudflare Workers
npm run deploy

# 部署成功後，在 Cloudflare Dashboard → Workers
# 設定自訂域名: api.angw1000.work
```

### Step 4: 設定域名

在 Cloudflare DNS 確認以下設定：

| 類型 | 名稱 | 目標 |
|------|------|------|
| CNAME | `@` / `www` | Cloudflare Pages 提供的網址 |
| CNAME | `api` | Workers 提供的網址 |

### Step 5: 驗證部署

```bash
# 測試 API
curl https://api.angw1000.work/api/products

# 預期回傳 { success: true, data: [...] }
```

## 👨‍🎓 學生使用說明

1. 開啟 <https://angw1000.work>
2. 選擇要練習的項目（Click / SendKeys / 表單 / Alert / 銷售系統）
3. 貨品銷售系統：
   - 進入 `/sales/index.html`，輸入學生代號（例如 `S01` ~ `S30`）
   - 點擊「進入銷售輸入」新增銷售紀錄
   - 點擊「進入銷售查詢」查看、刪除自己的紀錄

## 🐍 Selenium 範例程式碼

`examples/` 目錄提供完整可執行的練習範例：

| 檔案 | 說明 |
|------|------|
| `01_click_practice.py` | 各種點擊操作範例 |
| `02_sendkeys_practice.py` | 鍵盤輸入操作範例 |
| `03_form_practice.py` | 完整表單填寫範例 |
| `04_alert_practice.py` | Alert / Confirm / Prompt 處理範例 |
| `05_sales_system.py` | 貨品銷售系統端對端範例 |

### 執行範例

```bash
# 安裝 Selenium
pip install selenium

# 確保已安裝 ChromeDriver（與 Chrome 版本相符）
# 或使用 webdriver-manager:
pip install webdriver-manager

# 執行範例
python examples/01_click_practice.py
```

## 📡 API 端點文件

Base URL: `https://api.angw1000.work`

### GET /api/products

取得所有貨品清單。

**回應範例:**
```json
{
  "success": true,
  "data": [
    { "product_id": "P001", "name": "筆記本", "unit_price": 45 },
    ...
  ]
}
```

### POST /api/sales

新增銷售紀錄。

**Request Body:**
```json
{
  "student_id": "S01",
  "product_id": "P001",
  "quantity": 3,
  "sale_date": "2026-03-25"
}
```

**回應範例:**
```json
{
  "success": true,
  "message": "銷售紀錄新增成功",
  "data": { "id": 1, "total_price": 135 }
}
```

### GET /api/sales?student_id=xxx

取得指定學生的所有銷售紀錄。

### DELETE /api/sales/:id?student_id=xxx

刪除指定銷售紀錄（需提供 student_id 驗證，只能刪除自己的紀錄）。
