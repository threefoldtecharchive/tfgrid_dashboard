from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This module contains Transfer page elements.
"""

class TransferPage:

    transfer_page = (By.XPATH ,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div/div/div[3]/div[2]')
    amount_textfield=(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/form/div[2]/div/div[1]/div/input')
    receipient_textfield=(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/form/div[1]/div/div[1]/div[1]/input[1]')
    submit_button=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/div/button[2]')
    clear_button=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/div/button[1]')
    list=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/form/div[1]')
    address=(By.XPATH,'/html/body/div[1]/div[3]/div/div[1]/div/div')
    account_choice=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div')
    add_balance=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]/div[2]/button/span')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
    
    def navigate(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.transfer_page).click()
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3')))

    def amount_TFT_valid_input(self,cases):
        self.browser.find_element(*self.add_balance).click()
        WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]/div[2]/button/span')))
        self.browser.find_element(*self.receipient_textfield).send_keys('5FWW1F7XHaiRgPEqJdkv9nVgz94AVKXkTKNyfbLcY4rqpaNM')
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.BACKSPACE)
        self.browser.find_element(*self.amount_textfield).send_keys(cases)
        self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3').click()
        element = self.browser.find_element(*self.submit_button)
        return element
    
    def amount_TFT_invalid_input(self,cases):
        self.browser.find_element(*self.add_balance).click()
        WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]/div[2]/button/span')))
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.BACKSPACE)
        self.browser.find_element(*self.amount_textfield).send_keys(cases)
    
    def recipient_invalid_input(self,cases):
        self.browser.find_element(*self.receipient_textfield).send_keys(cases)
        self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3').click()
 
    def recipient_list(self):
        #WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[3]/div/div[2]/div[2]/form/div[1]/div/div[1]')))
        self.browser.find_element(*self.list).click()
        self.browser.find_element(*self.address).click()

    def recipient_valid_input(self,receipient_cases,cases):
        self.browser.find_element(*self.receipient_textfield).send_keys(receipient_cases)
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.BACKSPACE)
        self.browser.find_element(*self.amount_textfield).send_keys(cases)
        self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3').click()
        element = self.browser.find_element(*self.submit_button)    
        return element

    def transfer_TFTs_on_TFChain(self,cases1,cases2):
        self.browser.find_element(*self.receipient_textfield).send_keys(cases1)
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.BACKSPACE)
        self.browser.find_element(*self.amount_textfield).send_keys(cases2)
        self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3').click()
        self.browser.find_element(*self.submit_button).click()
