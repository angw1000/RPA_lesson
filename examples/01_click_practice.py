"""
01_click_practice.py
練習 Click 操作 - Selenium 教學範例
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = "https://angw1000.work"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get(BASE_URL + "/click.html")
    print("✅ 已開啟 Click 練習頁")
    time.sleep(1)

    # ----- 練習 1: 基本按鈕點擊 -----
    btn = wait.until(EC.element_to_be_clickable((By.ID, "btn-click")))
    btn.click()
    result = driver.find_element(By.ID, "click-result").text
    print(f"練習1 結果: {result}")
    assert result == "按鈕已點擊!", f"預期「按鈕已點擊!」，實際得到「{result}」"
    time.sleep(0.5)

    # ----- 練習 2: 超連結點擊 -----
    link = driver.find_element(By.ID, "test-link")
    link.click()
    print("練習2: 已點擊超連結")
    time.sleep(0.5)

    # ----- 練習 3: Checkbox 勾選 -----
    driver.find_element(By.ID, "chk-python").click()
    driver.find_element(By.ID, "chk-js").click()
    driver.find_element(By.ID, "btn-show-chk").click()
    chk_result = driver.find_element(By.ID, "chk-result").text
    print(f"練習3 Checkbox 結果: {chk_result}")
    time.sleep(0.5)

    # ----- 練習 4: Radio 選擇 -----
    driver.find_element(By.ID, "radio-medium").click()
    radio_result = driver.find_element(By.ID, "radio-result").text
    print(f"練習4 Radio 結果: {radio_result}")
    time.sleep(0.5)

    # ----- 練習 5: 下拉選單 (Select) -----
    select_el = driver.find_element(By.ID, "select-city")
    select = Select(select_el)
    select.select_by_visible_text("台北")
    select_result = driver.find_element(By.ID, "select-result").text
    print(f"練習5 Select 結果: {select_result}")
    time.sleep(0.5)

    # ----- 練習 6: 雙擊 -----
    dbl_btn = driver.find_element(By.ID, "btn-dblclick")
    actions = ActionChains(driver)
    actions.double_click(dbl_btn).perform()
    dbl_result = driver.find_element(By.ID, "dblclick-result").text
    print(f"練習6 雙擊結果: {dbl_result}")
    assert dbl_result == "偵測到雙擊!", f"預期「偵測到雙擊!」，實際得到「{dbl_result}」"
    time.sleep(0.5)

    # ----- 練習 7: 右鍵點擊 -----
    context_area = driver.find_element(By.ID, "context-area")
    actions = ActionChains(driver)
    actions.context_click(context_area).perform()
    ctx_result = driver.find_element(By.ID, "context-result").text
    print(f"練習7 右鍵結果: {ctx_result}")
    assert ctx_result == "偵測到右鍵點擊!", f"預期「偵測到右鍵點擊!」，實際得到「{ctx_result}」"
    time.sleep(0.5)

    print("\n🎉 所有 Click 練習完成！")

finally:
    time.sleep(2)
    driver.quit()
