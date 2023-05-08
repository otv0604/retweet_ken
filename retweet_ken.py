from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import secret

# ユーザー名とパスワード
username = secret.credentials["LOGIN_ID"]
password = secret.credentials["PASSWORD"]

# Chromeを起動する
service = Service("./chromedriver.exe")
service.start()
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)
# driver.maximize_window()

# Twitterにログインする
driver.get("https://twitter.com/login")
# time.sleep(5)
wait.until(EC.presence_of_all_elements_located((By.NAME, "text")))
driver.find_element(By.NAME, "text").send_keys(username)
driver.find_element(By.NAME, "text").send_keys(Keys.ENTER)
# time.sleep(2)
wait.until(EC.presence_of_all_elements_located((By.NAME, "password")))
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
time.sleep(2)

# リツイートするユーザーのページに移動する
driver.get("https://twitter.com/potitto_tousen")

# 最新のツイートから取得する
# wait.until(
#     EC.presence_of_all_elements_located(
#         (By.XPATH, "//div[@data-testid='cellInnerDiv']")
#     )
# )
# tweet = driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")

# tweetsにappend
# tweets = []
# try:
#     for x in tweet:
#         tweets.append(x)
# except:
#     pass

# scrollしながらRT
y = 0
for k in range(10):
    # 初期画面から取得
    wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@data-testid='cellInnerDiv']")
        )
    )
    tweet = driver.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")

    # try:
    #     for x in tweet:
    #         tweets.append(x)
    # except:
    #     continue

    # RT
    for rt in tweet[:10]:
        try:
            # リツイート元のツイートをしたユーザーをフォローする
            follow_link = rt.find_element(
                By.XPATH, './/div[@data-testid="User-Name"]//a[@role="link"]'
            )
            follow_username = follow_link.get_attribute("href").split("/")[-1]
            driver.execute_script("arguments[0].click();", follow_link)
            follow_link.click()
            time.sleep(2)
            follow_button = driver.find_element(
                By.XPATH,
                '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]//div[@data-testid="FollowButton"]//div[@role="button"]',
            )
            follow_button_text = follow_button.text.strip()
            if "フォロー中" in follow_button_text:
                print("フォロー済みです。")
            else:
                follow_button.click()
                print("フォローしました。")

            # ツイートをリツイートする
            retweet_button = rt.find_element(By.XPATH, './/div[@data-testid="retweet"]')
            driver.execute_script("arguments[0].click();", retweet_button)
            time.sleep(2)

            confirm_button = driver.find_element(
                By.XPATH, '//div[@data-testid="retweetConfirm"]'
            )
            confirm_button_text = confirm_button.text.strip()
            driver.execute_script("arguments[0].click();", confirm_button)
            print("リツイートしました。")
            time.sleep(2)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

    y += 1000
    driver.execute_script(f"window.scrollTo(0,{y})")
    time.sleep(2)

# WebDriverを終了する
driver.quit()


#     driver.get(f"https://twitter.com/{retweet_user_name}")
#     time.sleep(2)
#     follow_button = driver.find_element(
#         By.XPATH,
#         '//div[@data-testid="primaryColumn"]//div[@data-testid="placementTracking"]//div[contains(@data-testid,"follow")]',
#     )
#     follow_button_text = follow_button.text.strip()
#     if "フォロー中" in follow_button_text:
#         print("すでにフォロー済みです。")
#     else:
#         follow_button.click()
#         print("フォローしました。")
#         time.sleep(2)
# except:
#     continue
