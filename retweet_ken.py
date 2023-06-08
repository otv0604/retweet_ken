from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import secret
import pickle
import random


def get_article():
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
    )
    article = driver.find_elements(By.TAG_NAME, "article")
    return article


# Chromeドライバーのパスを指定してWebDriverを初期化
service = Service("chromedriver.exe")
options = Options()
options.headless = False
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# ユーザー名とパスワード
username = secret.credentials["LOGIN_ID"]
password = secret.credentials["PASSWORD"]
cookies_file = "twi.pkl"

# クッキーを読み込む
web_url = "https://twitter.com/potitto_tousen/"
cookies = pickle.load(open(cookies_file, "rb"))  # クッキーを読み込む
driver.get(web_url)  # まずは一度サイトにアクセス
for c in cookies:  # クッキーを設定する
    driver.add_cookie(c)
driver.get(web_url)  # クッキーを設定した後またアクセス

y = 0
tweets = get_article()

for _ in range(30):
    tweets = get_article()

    for tweet in tweets:
        try:
            tweets = get_article()

            # 最初のツイートまでスクロール
            actions = ActionChains(driver)
            actions.move_to_element(tweet)
            actions.perform()

            # ツイート元アカウント名の要素を取得しページ移動
            account_name_elements = tweet.find_element(
                By.XPATH, './/div[@data-testid="User-Name"]//a[@role="link"]'
            )
            print(account_name_elements.text)
            follow_username = account_name_elements.get_attribute("href").split("/")[-1]
            current_url = "https://twitter.com/" + follow_username

            # 新しいタブを作成・フォーカス・ページ移動
            driver.switch_to.new_window("tab")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(current_url)

            # フォロー実行
            wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]',
                    )
                )
            )
            follow_button = driver.find_element(
                By.XPATH,
                '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]',
            )
            actions.move_to_element(follow_button)
            actions.perform()
            follow_button.click()

            time.sleep(random.uniform(0.5, 2.0))

            # タブを閉じる
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            # リツイートボタンを押す
            retweet_button = tweet.find_element(
                By.XPATH, './/div[@data-testid="retweet"]'
            )
            actions.move_to_element(retweet_button)
            actions.perform()
            retweet_button.click()

            # リツイート確認ボタンを押す
            confirm_button = tweet.find_element(
                By.XPATH, '//div[@data-testid="retweetConfirm"]'
            )
            actions.move_to_element(confirm_button)
            actions.perform()
            confirm_button.click()
            print("リツイート実行")

            time.sleep(random.uniform(0.5, 2.0))

        except:
            print("リツイート済み")
            continue

    # スクロール
    print("-------------ループ終わり-------------")
    y += 5000
    driver.execute_script(f"window.scrollTo(0,{y})")

driver.quit()
