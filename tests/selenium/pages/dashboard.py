from selenium.webdriver.common.by import By
from tests.selenium.utils.base import Base

"""
This module contains Dashboard page elements.
"""

class DashboardPage:

    PolkaConnectionBtn = (By.XPATH ,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/button/span/button')
    Twin1st = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
    
    def polkaConnection(self):
        self.browser.find_element(*self.PolkaConnectionBtn).click()

        