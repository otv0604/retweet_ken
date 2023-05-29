from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("test_でていけ")

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

    for _ in range(3):
        # ページのロード完了を待機
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "article")))

        # 新しく表示されたツイート要素のみを取得
        current_tweets = driver.find_elements(By.TAG_NAME, "article")

        for tweet in current_tweets:
            try:
                print("==============================")
                print(tweet.text + "出ていけ")
                print("==============================")

                follow_link = tweet.find_element(
                    By.XPATH, './/div[@data-testid="User-Name"]//a[@role="link"]'
                )

                with open("tweets.txt", "a", encoding="utf-8") as file:
                    text = tweet.text.strip()
                    textf = follow_link.text.strip()
                    if text:
                        file.write("**************************\n")
                        file.write(text + "\n")
                        file.write("**************************\n")

                        file.write("--------------------------\n")
                        file.write(textf + "\n")
                        file.write("--------------------------\n")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                continue

        # 1000pxスクロールする
        driver.execute_script("window.scrollBy(0, 2000);")
        print("スクロールスクロールスクロールスクロール出ていけ")
        print("スクロールスクロールスクロールスクロール出ていけ")
        print("スクロールスクロールスクロールスクロール出ていけ")

        time.sleep(1)

finally:
    driver.quit()
