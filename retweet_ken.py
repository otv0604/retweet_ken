from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chromeドライバーのパスを指定してWebDriverを初期化
service = Service("chromedriver.exe")
options = Options()
# options.headless = True # ヘッドレスモードを有効化する場合はコメント解除
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

try:
    # Twitterのページを開く
    driver.get("https://twitter.com/potitto_tousen/")
    # 通知popup消去
    time.sleep(10)
    driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]',
    ).click()

    # 最初のツイート要素を取得
    previous_tweets = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tweet']")

    for _ in range(3):
        # 1000pxスクロールする
        driver.execute_script("window.scrollBy(0, 1000);")
        print("スクロールスクロールスクロールスクロール出ていけ")  # スクロール部分のコメントに「出ていけ」を追加
        print("スクロールスクロールスクロールスクロール出ていけ")
        print("スクロールスクロールスクロールスクロール出ていけ")

        # ページのロード完了を待機
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "article")))

        # 新しく表示されたツイート要素のみを取得
        current_tweets = driver.find_elements(By.TAG_NAME, "article")
        new_tweets = [tweet for tweet in current_tweets if tweet not in previous_tweets]

        for tweet in new_tweets:
            try:
                print("==============================")
                print(tweet.text + "出ていけ")  # コメントの語尾に「出ていけ」を追加
                print("==============================")
                with open("tweets.txt", "a", encoding="utf-8") as file:
                    text = tweet.text.strip()
                if text:
                    file.write("出ていけ\n")
                    file.write(text + "\n")
                    file.write("出ていけ\n")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            continue

    # 新しく表示されたツイートを前回のツイートとして更新
    previous_tweets = current_tweets

finally:
    driver.quit()
