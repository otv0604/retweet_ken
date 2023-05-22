from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Chromeドライバーのパスを指定してWebDriverを初期化
service = Service("./chromedriver113.exe")
service.start()
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

# Twitterのページを開く
driver.get("https://twitter.com/potitto_tousen/")
time.sleep(10)
actions = ActionChains(driver)

# 通知popup消去
driver.find_element(
    By.XPATH,
    '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]',
).click()

# ツイート読み込みまで待機
wait = WebDriverWait(driver, 30)
wait.until(
    EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='cellInnerDiv']"))
)
tweet_elements = driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
for rt in tweet_elements:
    try:
        print("==============================")
        print(rt.text)
        print("==============================")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        continue

for k in range(3):
    # 1000pxスクロールする
    driver.execute_script("window.scrollBy(0, 3000);")
    print("スクロールスクロールスクロールスクロール")
    print("スクロールスクロールスクロールスクロール")
    print("スクロールスクロールスクロールスクロール")
    # 1秒待機して過去ツイートが読み込まれるのを待つ
    time.sleep(1)

    # 過去ツイートの要素を特定し、数を取得
    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-testid='cellInnerDiv']")
        )
    )
    tweet_elements = driver.find_elements(
        By.XPATH, "//div[@data-testid='cellInnerDiv']"
    )
    for rt in tweet_elements:
        try:
            print("==============================")
            print(rt.text)
            print("==============================")
            with open("tweets.txt", "a", encoding="utf-8") as file:
                text = rt.text.strip()
                if text:
                    file.write("==============================\n")
                    file.write(text + "\n")
                    file.write("==============================\n")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

    past_tweet_count = len(tweet_elements)

    # 結果を表示
    print("1000pxスクロール後の過去ツイート数:", past_tweet_count)

    # 追加するコード


# WebDriverを終了
driver.quit()
