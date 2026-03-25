"""
03_form_practice.py
練習表單操作 - Selenium 教學範例
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://angw1000.work"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get(BASE_URL + "/form.html")
    print("✅ 已開啟表單操作練習頁")
    time.sleep(1)

    # ----- 填寫姓名 -----
    name_input = wait.until(EC.element_to_be_clickable((By.ID, "form-name")))
    name_input.clear()
    name_input.send_keys("王小明")
    print("✔ 已填寫姓名")

    # ----- 填寫 Email -----
    email_input = driver.find_element(By.ID, "form-email")
    email_input.clear()
    email_input.send_keys("wang@example.com")
    print("✔ 已填寫 Email")

    # ----- 填寫電話 -----
    phone_input = driver.find_element(By.ID, "form-phone")
    phone_input.clear()
    phone_input.send_keys("0912-345-678")
    print("✔ 已填寫電話")

    # ----- 選擇性別 Radio -----
    driver.find_element(By.ID, "form-gender-male").click()
    print("✔ 已選擇性別: 男")

    # ----- 勾選興趣 Checkbox -----
    driver.find_element(By.ID, "form-hobby-reading").click()
    driver.find_element(By.ID, "form-hobby-coding").click()
    print("✔ 已勾選興趣: 閱讀、程式")

    # ----- Select 城市 -----
    city_select = Select(driver.find_element(By.ID, "form-city"))
    city_select.select_by_visible_text("台北")
    print("✔ 已選擇城市: 台北")

    # ----- 填寫備註 -----
    note_textarea = driver.find_element(By.ID, "form-note")
    note_textarea.clear()
    note_textarea.send_keys("這是一筆測試資料，由 Selenium 自動填寫。")
    print("✔ 已填寫備註")

    # ----- 勾選同意條款 -----
    agree_chk = driver.find_element(By.ID, "form-agree")
    if not agree_chk.is_selected():
        agree_chk.click()
    print("✔ 已勾選同意條款")

    # ----- 點擊送出 -----
    submit_btn = driver.find_element(By.ID, "form-submit")
    submit_btn.click()
    print("✔ 已點擊送出")
    time.sleep(1)

    # ----- 驗證結果 -----
    result_section = wait.until(EC.visibility_of_element_located((By.ID, "form-result")))
    result_text = result_section.text
    print(f"\n表單結果:\n{result_text}")

    assert "王小明" in result_text, "結果中找不到姓名"
    assert "wang@example.com" in result_text, "結果中找不到 Email"
    assert "台北" in result_text, "結果中找不到城市"
    print("\n✅ 表單驗證通過！")

    # ----- 點擊重置 -----
    driver.find_element(By.ID, "form-reset").click()
    print("✔ 已點擊重置")
    time.sleep(0.5)
    name_val = driver.find_element(By.ID, "form-name").get_attribute("value")
    print(f"重置後姓名欄位值: '{name_val}'")

    print("\n🎉 表單操作練習完成！")

finally:
    time.sleep(2)
    driver.quit()
