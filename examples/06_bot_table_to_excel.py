# -*- coding: utf-8 -*-
"""
RPA 教學範例：
1. 使用 requests + BeautifulSoup 取得網頁原始碼，並尋找 HTML table。
2. 使用 Selenium 開啟同一個網頁，等待 JavaScript 執行後再尋找 table。
3. 將 table 交給 pandas 轉成 DataFrame，再輸出成 Excel 檔。

需要安裝的套件：
    pip install requests beautifulsoup4 pandas openpyxl selenium lxml
"""

from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# URL = "https://www.bot.com.tw/tw/policy-business/public-treasury-service/public-treasury-deposit-business/each-agency-treasury-bank"
# URL = "https://net.tax.nat.gov.tw/PLRX/Lrx200d01/bullitin.html"
URL = "https://net.tax.nat.gov.tw/PLRX/Lrx200d01/quickStart.html"
OUTPUT_DIR = Path(__file__).resolve().parent


def flatten_column_name(column: Any) -> str:
    """將 pandas 多層欄位名稱整理成一般文字欄位名稱。"""
    if not isinstance(column, tuple):
        return str(column)

    # 多層表頭常會出現 Unnamed 欄位，通常是 HTML 合併儲存格造成的，可略過。
    parts = [
        str(part)
        for part in column
        if str(part) and not str(part).startswith("Unnamed:")
    ]
    return "_".join(parts)


def save_first_table_to_excel(html: str, output_file: Path) -> pd.DataFrame:
    """從 HTML 找到第一個 table，轉成 DataFrame 後存成 Excel。"""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if table is None:
        raise ValueError("這份網頁原始碼中找不到任何 <table> 元素。")

    # pandas 可以直接讀取 HTML table，回傳值會是 DataFrame 清單。
    df = pd.read_html(StringIO(str(table)))[0]

    # 如果 HTML table 有多層表頭，pandas 會建立 MultiIndex 欄位。
    # Excel 輸出搭配 index=False 時不支援 MultiIndex，所以先轉成一般欄位名稱。
    # df.columns = [flatten_column_name(column) for column in df.columns]

    df.to_excel(output_file, index=False)
    return df


def fetch_table_with_beautifulsoup() -> None:
    """使用 requests 取得原始 HTML，再用 BeautifulSoup 解析 table。"""
    output_file = OUTPUT_DIR / "bot_table_beautifulsoup.xlsx"

    # 加上 User-Agent，讓請求看起來像一般瀏覽器。
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0 Safari/537.36"
        )
    }
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    df = save_first_table_to_excel(response.text, output_file)
    print(f"BeautifulSoup 輸出檔案：{output_file}")
    print(df.head())


def fetch_table_with_selenium() -> None:
    """使用 Chrome 開啟網頁，等待 JavaScript 產生 table 後再輸出 Excel。"""
    output_file = OUTPUT_DIR / "bot_table_selenium.xlsx"

    options = Options()
    # headless 模式代表背景執行 Chrome，不會跳出瀏覽器視窗。
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1440,1000")

    driver = webdriver.Edge(options=options)
    try:
        driver.get(URL)

        # 最多等待 30 秒，直到網頁中出現 table。
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )

        df = save_first_table_to_excel(driver.page_source, output_file)
        print(f"Selenium 輸出檔案：{output_file}")
        print(df.head())
    finally:
        # 無論成功或失敗，都要關閉瀏覽器，避免背景程序殘留。
        driver.quit()


if __name__ == "__main__":
    print("=== BeautifulSoup 範例 ===")
    try:
        fetch_table_with_beautifulsoup()
    except Exception as exc:
        print(f"BeautifulSoup 抓取失敗：{exc}")
        print("如果 table 是由 JavaScript 動態產生，BeautifulSoup 可能會抓不到。")

    print("\n=== Selenium 範例 ===")
    fetch_table_with_selenium()
