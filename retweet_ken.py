from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Chromeドライバーのパスを指定してWebDriverを初期化
service = Service("chromedriver.exe")
options = Options()
# options.headless = True # ヘッドレスモードを有効化する場合はコメント解除
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)


# Twitterのページを開く
driver.get("https://twitter.com/potitto_tousen/")
# 通知popup消去
time.sleep(10)
driver.find_element(
    By.XPATH,
    '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]',
).click()

# ツイートの要素を取得
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
)
tweets = driver.find_elements(By.TAG_NAME, "article")

for i in range(3):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
    )
    tweets = driver.find_elements(By.TAG_NAME, "article")

    # 最初のツイートまでスクロール
    actions = ActionChains(driver)
    actions.move_to_element(tweets[i])
    actions.perform()
    time.sleep(1)

    # ツイート元アカウント名の要素を取得しページ移動
    account_name_elements = tweets[i].find_element(
        By.XPATH, './/div[@data-testid="User-Name"]//a[@role="link"]'
    )
    follow_username = account_name_elements.get_attribute("href").split("/")[-1]
    current_url = "https://twitter.com/" + follow_username
    driver.get(current_url)

    # ページ遷移の完了を待つ
    time.sleep(3)
    driver.back()
    time.sleep(3)

driver.quit()
