from selenium.webdriver.common.by import By
from frontend_selenium.utils.base import Base

"""
This module contains Dashboard page elements.
"""

class DashboardPage:

    polka_connection_btn = (By.XPATH ,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/button/span/button')
    twin_name = (By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div[1]')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
    
    def polka_connection(self):
        self.browser.find_element(*self.polka_connection_btn).click()
    
    def check_for_only_twin_name(self):
        return (self.browser.find_element(*self.twin_name).text)
