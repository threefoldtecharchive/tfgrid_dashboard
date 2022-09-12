from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This module contains Transfer page elements.
"""

class TransferPage:

    transfer_page = (By.XPATH ,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div')
    
    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
    
    def navigate(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.transfer_page).click()
        WebDriverWait(self.browser, 30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3'))
        )
        

