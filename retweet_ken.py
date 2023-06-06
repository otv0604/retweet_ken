from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import secret
import pickle

# Chromeドライバーのパスを指定してWebDriverを初期化
service = Service("chromedriver.exe")
options = Options()
# options.headless = True # ヘッドレスモードを有効化する場合はコメント解除
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

# ツイートの要素を取得
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
)
tweets = driver.find_elements(By.TAG_NAME, "article")

for tweet in tweets:
    tweets = driver.find_elements(By.TAG_NAME, "article")

    # 最初のツイートまでスクロール
    actions = ActionChains(driver)
    actions.move_to_element(tweet)
    actions.perform()
    time.sleep(1)

    # ツイート元アカウント名の要素を取得しページ移動
    account_name_elements = tweet.find_element(
        By.XPATH, './/div[@data-testid="User-Name"]//a[@role="link"]'
    )
    follow_username = account_name_elements.get_attribute("href").split("/")[-1]
    current_url = "https://twitter.com/" + follow_username

    # 新しいタブを作成し、フォーカスする
    driver.switch_to.new_window("tab")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(current_url)

    # ページ遷移の完了を待つ
    wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]',
            )
        )
    )

    time.sleep(3)

    follow_button = driver.find_element(
        By.XPATH,
        '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]',
    )

    actions.move_to_element(follow_button)
    actions.perform()
    follow_button.click()

    time.sleep(2)
    driver.close()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)

    # ツイートをリツイートする
    try:
        retweet_button = tweet.find_element(By.XPATH, './/div[@data-testid="retweet"]')
        actions.move_to_element(retweet_button)
        actions.perform()
        retweet_button.click()

        time.sleep(2)

        confirm_button = tweet.find_element(
            By.XPATH, '//div[@data-testid="retweetConfirm"]'
        )
        actions.move_to_element(confirm_button)
        actions.perform()
        confirm_button.click()

        time.sleep(2)

    except:
        print("リツイート済み")
        continue

driver.quit()
