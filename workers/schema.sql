-- 貨品銷售系統資料庫結構 (Cloudflare D1 / SQLite)

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id  TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    unit_price  REAL NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  TEXT NOT NULL,
    product_id  TEXT NOT NULL,
    quantity    INTEGER NOT NULL,
    total_price REAL NOT NULL,
    sale_date   TEXT NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX IF NOT EXISTS idx_sales_student ON sales(student_id);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_id);

-- 初始貨品資料
INSERT OR IGNORE INTO products (product_id, name, unit_price) VALUES
    ('P001', '筆記本', 45.00),
    ('P002', '原子筆(藍)', 15.00),
    ('P003', '修正帶', 35.00),
    ('P004', 'A4影印紙(包)', 120.00),
    ('P005', '資料夾', 25.00),
    ('P006', '螢光筆組', 60.00),
    ('P007', '釘書機', 85.00),
    ('P008', '剪刀', 40.00),
    ('P009', '膠水', 20.00),
    ('P010', '便利貼(包)', 30.00);
