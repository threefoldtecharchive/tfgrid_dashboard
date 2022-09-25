from utils.utils import generate_leters, generate_string, invalid_address, invalid_amount, invalid_amount_negtive, valid_amount
from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This module contains Transfer page elements.
"""

class TransferPage:
    
    transfer_page = (By.XPATH, '//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div/div/div[3]')
    amount_textfield=(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div[2]/form/div[2]/div/div[1]/div/input')
    receipient_textfield=(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div[2]/form/div[1]/div/div[1]/div[1]/input[1]')
    submit_button=(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div/button[2]')
    address=(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div')
    account_choice=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/div[1]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[1]/div[3]")))
    
    def navigate(self, user):
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Connected Accounts')]")))
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Twin Details')]")))
        self.browser.find_element(*self.transfer_page).click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]")))

    def recipient_list(self):
        self.browser.find_element(*self.receipient_textfield).click()
        return self.browser.find_element(*self.address).text

    def recipient_valid_input(self, receipient_cases):
        self.browser.find_element(*self.receipient_textfield).send_keys(receipient_cases)
        self.browser.find_element(*self.amount_textfield).send_keys(1)
        self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
        return self.browser.find_element(*self.submit_button)
    
    def recipient_invalid_input(self):
        cases = [' ', generate_string(), invalid_address(), generate_leters()]
        for case in cases:
            self.browser.find_element(*self.receipient_textfield).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.receipient_textfield).send_keys(Keys.DELETE)
            self.browser.find_element(*self.receipient_textfield).send_keys(case)
            self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
            assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'invalid address')]")
        self.browser.find_element(*self.amount_textfield).send_keys(1)
        return self.browser.find_element(*self.submit_button)

    def amount_TFT_valid_input(self, receipient_cases):
        self.browser.find_element(*self.receipient_textfield).send_keys(receipient_cases)
        self.browser.find_element(*self.amount_textfield).send_keys(valid_amount())
        self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
        return self.browser.find_element(*self.submit_button)
    
    def amount_TFT_invalid_input(self, receipient_cases):
        cases = [0, -900.009, invalid_amount_negtive()]
        balance = self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text
        self.browser.find_element(*self.receipient_textfield).send_keys(receipient_cases)
        for case in cases:
            self.browser.find_element(*self.amount_textfield).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.amount_textfield).send_keys(Keys.DELETE)
            self.browser.find_element(*self.amount_textfield).send_keys(case)
            self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
            assert self.browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount cannot be negative or 0')]")
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.DELETE)
        self.browser.find_element(*self.amount_textfield).send_keys(invalid_amount())
        self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
        assert self.browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount must have 3 decimals only')]")
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.amount_textfield).send_keys(Keys.DELETE)
        self.browser.find_element(*self.amount_textfield).send_keys(format(float(balance)+100,'.3f'))
        self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
        assert self.browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount cannot exceed balance')]")
        return self.browser.find_element(*self.submit_button)

    def transfer_TFTs_on_TFChain(self, twin_address):
        balance = self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text
        self.browser.find_element(*self.receipient_textfield).send_keys(twin_address)
        self.browser.find_element(*self.amount_textfield).send_keys(1)
        self.browser.find_element(By.XPATH, "//*[contains(text(), 'Transfer TFTs on the TFChain')]").click()
        self.browser.find_element(*self.submit_button).click()
        return balance
