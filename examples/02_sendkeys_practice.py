"""
02_sendkeys_practice.py
練習 SendKeys 操作 - Selenium 教學範例
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://angw1000.work"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get(BASE_URL + "/sendkeys.html")
    print("✅ 已開啟 SendKeys 練習頁")
    time.sleep(1)

    # ----- 練習 1: 文字輸入 -----
    text_input = wait.until(EC.element_to_be_clickable((By.ID, "input-text")))
    text_input.click()
    text_input.send_keys("Hello, Selenium!")
    time.sleep(0.5)
    mirror = driver.find_element(By.ID, "text-mirror").text
    print(f"練習1 即時顯示: {mirror}")

    # 清除並重新輸入
    text_input.clear()
    text_input.send_keys("Python 自動化測試")
    mirror = driver.find_element(By.ID, "text-mirror").text
    print(f"練習1 重新輸入: {mirror}")
    time.sleep(0.5)

    # ----- 練習 2: 密碼輸入 -----
    pwd_input = driver.find_element(By.ID, "input-password")
    pwd_input.send_keys("my_secret_password")
    print(f"練習2 密碼欄位類型: {pwd_input.get_attribute('type')}")

    # 切換顯示
    driver.find_element(By.ID, "btn-show-pwd").click()
    print(f"練習2 切換後類型: {pwd_input.get_attribute('type')}")
    time.sleep(0.5)

    # ----- 練習 3: Textarea 多行輸入 -----
    textarea = driver.find_element(By.ID, "input-textarea")
    textarea.click()
    textarea.send_keys("第一行文字\n第二行文字\n第三行文字")
    char_count = driver.find_element(By.ID, "char-count").text
    print(f"練習3 字數: {char_count}")
    time.sleep(0.5)

    # ----- 練習 4: 日期選擇 -----
    date_input = driver.find_element(By.ID, "input-date")
    date_input.send_keys("2026-03-25")
    date_result = driver.find_element(By.ID, "date-result").text
    print(f"練習4 日期結果: {date_result}")
    time.sleep(0.5)

    # ----- 練習 5: 數字輸入 -----
    num_input = driver.find_element(By.ID, "input-number")
    num_input.clear()
    num_input.send_keys("75")
    driver.find_element(By.ID, "btn-show-number").click()
    num_result = driver.find_element(By.ID, "number-result").text
    print(f"練習5 數字結果: {num_result}")
    time.sleep(0.5)

    # ----- 練習 6: 搜尋框 -----
    search_input = driver.find_element(By.ID, "input-search")
    search_input.send_keys("Selenium 自動化")
    driver.find_element(By.ID, "btn-do-search").click()
    search_result = driver.find_element(By.ID, "search-result").text
    print(f"練習6 搜尋結果: {search_result}")

    # 清除
    driver.find_element(By.ID, "btn-clear-search").click()
    print(f"練習6 清除後值: '{search_input.get_attribute('value')}'")
    time.sleep(0.5)

    # ----- 練習 7: 鍵盤按鍵 -----
    hotkey_input = driver.find_element(By.ID, "input-hotkey")
    hotkey_input.click()

    hotkey_input.send_keys(Keys.ENTER)
    result = driver.find_element(By.ID, "hotkey-result").text
    print(f"練習7 Enter 鍵: {result}")
    time.sleep(0.3)

    hotkey_input.send_keys(Keys.ESCAPE)
    result = driver.find_element(By.ID, "hotkey-result").text
    print(f"練習7 Escape 鍵: {result}")
    time.sleep(0.3)

    hotkey_input.send_keys(Keys.TAB)
    print(f"練習7 Tab 鍵已送出")
    time.sleep(0.3)

    print("\n🎉 所有 SendKeys 練習完成！")

finally:
    time.sleep(2)
    driver.quit()
