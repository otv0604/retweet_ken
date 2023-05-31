from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import getpass

# Chromeドライバーのパスを指定してWebDriverを初期化
service = Service("chromedriver.exe")
options = Options()
# options.headless = True # ヘッドレスモードを有効化する場合はコメント解除
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# ユーザー名とパスワードの入力
username = input("ログインIDを入力してください: ")
password = getpass.getpass("パスワードを入力してください: ")

# Twitterにログイン
driver.get("https://twitter.com/login")
wait.until(EC.presence_of_element_located((By.NAME, "session[username_or_email]")))
username_field = driver.find_element(By.NAME, "session[username_or_email]")
password_field = driver.find_element(By.NAME, "session[password]")
username_field.send_keys(username)
password_field.send_keys(password)
password_field.submit()

# ツイートの要素を取得
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "article")))
tweets = driver.find_elements(By.TAG_NAME, "article")

for tweet in tweets:
    # 最初のツイートまでスクロール
    actions = ActionChains(driver)
    actions.move_to_element(tweet)
    actions.perform()
    time.sleep(1)

    # ツイート元アカウント名の要素を取得
    account_name_element = tweet.find_element(By.XPATH, './/div[@data-testid="User-Name"]//a[@role="link"]')
    follow_username = account_name_element.get_attribute("href").split("/")[-1]
    current_url = "https://twitter.com/" + follow_username

    # フォローボタンをクリック
    driver.get(current_url)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]')))
    follow_button = driver.find_element(By.XPATH, '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]')
    follow_button.click()

driver.quit()
