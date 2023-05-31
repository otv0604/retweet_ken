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

# Twitterクッキー保存する
driver.get("https://twitter.com/login")

wait.until(EC.presence_of_all_elements_located((By.NAME, "text")))
driver.find_element(By.NAME, "text").send_keys(username)
driver.find_element(By.NAME, "text").send_keys(Keys.ENTER)

wait.until(EC.presence_of_all_elements_located((By.NAME, "password")))
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
time.sleep(5)

cookies = driver.get_cookies()  # クッキーを取得する
pickle.dump(cookies, open(cookies_file, "wb"))  # クッキーを保存する
