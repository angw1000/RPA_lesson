"""
05_sales_system.py
練習貨品銷售系統 - Selenium 教學範例
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://angw1000.work"
STUDENT_ID = "S01"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # ----- 進入銷售系統入口 -----
    driver.get(BASE_URL + "/sales/index.html")
    print("✅ 已開啟銷售系統入口")
    time.sleep(1)

    # ----- 輸入學生代號 -----
    student_input = wait.until(EC.element_to_be_clickable((By.ID, "student-id")))
    student_input.clear()
    student_input.send_keys(STUDENT_ID)
    print(f"✔ 已輸入學生代號: {STUDENT_ID}")

    # ----- 點擊進入銷售輸入 -----
    driver.find_element(By.ID, "btn-to-input").click()
    print("✔ 已點擊「進入銷售輸入」")

    # ----- 等待輸入頁載入 -----
    wait.until(EC.url_contains("input.html"))
    wait.until(EC.visibility_of_element_located((By.ID, "display-student-id")))
    displayed_id = driver.find_element(By.ID, "display-student-id").text
    print(f"✔ 輸入頁顯示學生代號: {displayed_id}")
    assert displayed_id == STUDENT_ID
    time.sleep(1)

    # ----- 等待貨品選單載入 -----
    product_select_el = wait.until(EC.element_to_be_clickable((By.ID, "sales-product")))
    # 等待 option 載入完成 (不再是「-- 載入中 --」)
    wait.until(lambda d: len(d.find_element(By.ID, "sales-product").find_elements(By.TAG_NAME, "option")) > 1)
    print("✔ 貨品清單載入完成")

    # ----- 選擇貨品 -----
    product_select = Select(product_select_el)
    product_select.select_by_index(1)  # 選擇第1個貨品
    selected_text = product_select_el.find_elements(By.TAG_NAME, "option")[1].text
    print(f"✔ 已選擇貨品: {selected_text}")
    time.sleep(0.5)

    # 確認單價顯示
    price_text = driver.find_element(By.ID, "display-price").text
    print(f"✔ 顯示單價: NT$ {price_text}")

    # ----- 輸入數量 -----
    qty_input = driver.find_element(By.ID, "sales-quantity")
    qty_input.clear()
    qty_input.send_keys("3")
    print("✔ 已輸入數量: 3")
    time.sleep(0.3)

    # 確認小計顯示
    subtotal_text = driver.find_element(By.ID, "display-subtotal").text
    print(f"✔ 預估小計: NT$ {subtotal_text}")

    # ----- 設定銷售日期 -----
    date_input = driver.find_element(By.ID, "sales-date")
    date_input.clear()
    date_input.send_keys("2026-03-25")
    print("✔ 已設定銷售日期: 2026-03-25")

    # ----- 點擊送出 -----
    submit_btn = driver.find_element(By.ID, "sales-submit")
    submit_btn.click()
    print("✔ 已點擊送出銷售紀錄")

    # ----- 驗證成功訊息 -----
    msg_el = wait.until(EC.visibility_of_element_located((By.ID, "sales-message")))
    # 等待訊息出現（成功或失敗）
    wait.until(lambda d: d.find_element(By.ID, "sales-message").text != "")
    msg_text = driver.find_element(By.ID, "sales-message").text
    print(f"✔ 銷售訊息: {msg_text}")
    assert "成功" in msg_text, f"銷售失敗，訊息: {msg_text}"
    time.sleep(1)

    # ----- 導航到查詢頁 -----
    nav_query = driver.find_element(By.ID, "nav-to-query")
    nav_query.click()
    wait.until(EC.url_contains("query.html"))
    print("✔ 已進入查詢頁")
    time.sleep(1)

    # ----- 確認查詢頁顯示學生代號 -----
    q_display = wait.until(EC.visibility_of_element_located((By.ID, "display-student-id")))
    print(f"✔ 查詢頁學生代號: {q_display.text}")

    # ----- 等待表格資料載入 -----
    wait.until(lambda d: d.find_element(By.ID, "sales-count").text not in ("--", ""))
    sales_count = driver.find_element(By.ID, "sales-count").text
    sales_total = driver.find_element(By.ID, "sales-total").text
    print(f"✔ 銷售紀錄筆數: {sales_count}")
    print(f"✔ 銷售總金額: {sales_total}")
    assert int(sales_count) > 0, "查詢頁沒有銷售紀錄"

    print("\n🎉 貨品銷售系統練習完成！")

finally:
    time.sleep(2)
    driver.quit()
