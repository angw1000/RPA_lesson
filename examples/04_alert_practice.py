"""
04_alert_practice.py
練習 Alert 處理 - Selenium 教學範例
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://angw1000.work"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get(BASE_URL + "/alert.html")
    print("✅ 已開啟 Alert 練習頁")
    time.sleep(1)

    # ----- 練習 1: Alert -----
    driver.find_element(By.ID, "btn-alert").click()
    alert = wait.until(EC.alert_is_present())
    print(f"練習1 Alert 訊息: {alert.text}")
    alert.accept()
    print("練習1 Alert 已關閉")
    time.sleep(0.5)

    # ----- 練習 2: Confirm - 按確定 -----
    driver.find_element(By.ID, "btn-confirm").click()
    confirm = wait.until(EC.alert_is_present())
    print(f"練習2 Confirm 訊息: {confirm.text}")
    confirm.accept()
    result = driver.find_element(By.ID, "confirm-result").text
    print(f"練習2 按確定結果: {result}")
    assert "確定" in result
    time.sleep(0.5)

    # Confirm - 按取消
    driver.find_element(By.ID, "btn-confirm").click()
    confirm2 = wait.until(EC.alert_is_present())
    confirm2.dismiss()
    result2 = driver.find_element(By.ID, "confirm-result").text
    print(f"練習2 按取消結果: {result2}")
    assert "取消" in result2
    time.sleep(0.5)

    # ----- 練習 3: Prompt -----
    driver.find_element(By.ID, "btn-prompt").click()
    prompt = wait.until(EC.alert_is_present())
    print(f"練習3 Prompt 訊息: {prompt.text}")
    prompt.send_keys("Selenium 學員")
    prompt.accept()
    prompt_result = driver.find_element(By.ID, "prompt-result").text
    print(f"練習3 Prompt 結果: {prompt_result}")
    assert "Selenium 學員" in prompt_result
    time.sleep(0.5)

    # ----- 練習 4: 延遲 Alert (3 秒) -----
    driver.find_element(By.ID, "btn-delayed-alert").click()
    print("練習4 等待延遲 Alert...")
    delayed_wait = WebDriverWait(driver, 5)
    delayed_alert = delayed_wait.until(EC.alert_is_present())
    print(f"練習4 延遲 Alert 訊息: {delayed_alert.text}")
    delayed_alert.accept()
    print("練習4 延遲 Alert 已關閉")
    time.sleep(0.5)

    # ----- 練習 5: 連續 Alert -----
    driver.find_element(By.ID, "btn-multi-alert").click()
    for i in range(1, 4):
        alert_i = wait.until(EC.alert_is_present())
        print(f"練習5 第{i}個 Alert: {alert_i.text}")
        alert_i.accept()
        time.sleep(0.3)
    multi_result = driver.find_element(By.ID, "multi-alert-result").text
    print(f"練習5 完成訊息: {multi_result}")
    time.sleep(0.5)

    # ----- 練習 6: 自訂 Modal -----
    driver.find_element(By.ID, "btn-modal").click()
    modal = wait.until(EC.visibility_of_element_located((By.ID, "custom-modal")))
    print("練習6 Modal 已開啟")

    # 確認按鈕
    modal_confirm = driver.find_element(By.ID, "modal-confirm")
    modal_confirm.click()

    modal_result = wait.until(EC.visibility_of_element_located((By.ID, "modal-result")))
    print(f"練習6 Modal 結果: {modal_result.text}")
    assert "確定" in modal_result.text
    time.sleep(0.5)

    print("\n🎉 所有 Alert 練習完成！")

finally:
    time.sleep(2)
    driver.quit()
