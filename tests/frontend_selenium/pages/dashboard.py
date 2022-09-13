from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

"""
This module contains Dashboard homepage elements.
"""

class DashboardPage:

    polka_connection_btn = (By.XPATH ,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/button/span/button')
    swipe_right = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/button[2]/span/i')
    swipe_left = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/button[1]/span/i')
    download_polka = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[1]/div/div/div/div/div/a')
    discover_tfgrid = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div/div/button')
    learn_more = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div/div/a')
    account_list = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]')
    search_bar_label = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[1]/div/div/div/div[1]/div')
    search_bar = (By.XPATH ,'//*[@id="input-1816"]')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
    
    def polka_connection(self):
        self.browser.find_element(*self.polka_connection_btn).click()
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/h1'))
        )

    def polka_disconnection(self):
        self.browser.find_element(*self.polka_connection_btn).click()
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[1]/div[2]'))
        )

    def polka_connection_status(self):
        return self.browser.find_element(*self.polka_connection_btn).get_attribute("class")

    def navigate_to_polka(self):
        self.browser.find_element(*self.download_polka).click()
        WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[1])
        return self.browser.current_url

    def navigate_to_explorer(self):
        self.browser.find_element(*self.swipe_right).click()
        self.browser.find_element(*self.discover_tfgrid).click()
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/section'))
        )
        return self.browser.current_url

    def navigate_to_manual(self):
        self.browser.find_element(*self.swipe_left).click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]')))
        self.browser.find_element(*self.learn_more).click()
        WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[1])
        return self.browser.current_url
    
    def search_accounts(self, account):
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/h1'))
        )
        self.browser.find_element(*self.search_bar_label).click()
        actions = ActionChains(self.browser)
        for i in range (0,51):
            actions.send_keys(Keys.BACKSPACE)
        actions.send_keys(account)
        actions.perform()

    def accounts_list(self):
        return self.browser.find_element(*self.account_list).text
    
    def get_address(self, account):
        return str(account[13:])