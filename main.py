from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import os

load_dotenv()  # load .env file


class Bot():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def start(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'upgrade-insecure-requests': '1',
            'dnt': '1'
        }

        self.DRIVER_PATH = '/usr/bin/chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument(f"user-agent={self.headers['User-Agent']}")
        self.options.add_argument(
            "--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            executable_path=self.DRIVER_PATH)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 768)

    def go_to(self, url):
        self.driver.get(url)

    def follower_count(self, username):
        self.xpath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
        self.go_to(f'https://instagram.com/{username}')

        try:
            count = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.xpath))).text
            print(count)
        except TimeoutException:
            return 'Timeout'

    def login(self):
        self.go_to('https://instagram.com/accounts/login')

        self.username_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        self.username_input.send_keys(self.username)

        self.password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
        self.password_input.send_keys(self.password)

        self.login_button = self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]/button')
        self.login_button.click()

        # Wait for presence of search input (redirect)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))


bot = Bot(os.environ.get('USERNAME'), os.environ.get('PASSWORD'))
bot.start()
bot.login()
bot.follower_count('nike')
