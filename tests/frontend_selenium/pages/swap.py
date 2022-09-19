from utils.utils import generate_leters, generate_string, get_stellar_address
import requests
from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SwapPage:

    swap=(By.XPATH, "//*[contains(text(), 'swap')]")
    stellar_choose=(By.XPATH, "//*[contains(text(), 'stellar')]") 
    stellar=(By.XPATH,'//*[@role="option"]')
    deposit=(By.XPATH, "//*[contains(text(), 'deposit')]")
    withdraw=(By.XPATH, "//*[contains(text(), 'withdraw')]")
    howdone=(By.XPATH, "//*[contains(text(), 'How is it done?')]")
    submit_button=(By.XPATH, "//*[@id='app']/div[5]/div/div/div[3]/button[2]")
    stellar_address=(By.XPATH, '/html/body/div[1]/div[5]/div/div/div[2]/form/div[1]/div/div[1]/div/input')
    amount_tft=(By.XPATH, '/html/body/div[1]/div[5]/div/div/div[2]/form/div[2]/div/div[1]/div/input')

    def __init__(self, browser):
        self.browser = browser

    def load(self):
        self.browser.get(Base.base_url)

    def navigate_to_swap(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.swap).click()
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer TFT Across Chains')]")))
    
    def twin_addres(self):
        return self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div/div/div/div[2]').text 

    def transfer_chain(self):
        self.browser.find_element(*self.stellar_choose).click()
        self.browser.find_element(*self.stellar).click()

    def choose_deposit(self):
        self.browser.find_element(*self.deposit).click()

    def choose_withdraw(self):
        self.browser.find_element(*self.withdraw).click()

    def how_it_done(self):
        self.browser.find_element(*self.howdone).click()
        WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[1])
        return self.browser.current_url
    
    def check_deposit(self):
        self.browser.find_element(*self.deposit).click() 
        assert self.browser.find_element(By.XPATH,"//*[contains(text(), 'Amount: should be larger than 1TFT (deposit fee is: 1TFT)')]").text in self.browser.page_source
        assert self.browser.find_element(By.XPATH, "//*[@id='app']/div[5]/div/div/div[1]/div/div[1]/div[1]/ul/li[1]/b").text == 'GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG'
        twin_id = self.browser.find_element(By.XPATH,"//*[@id='app']/div[5]/div/div/div[1]/div/div[1]/div[1]/ul/li[2]/b").text
        return twin_id

    def get_twin_id(self, user_address):
        r = requests.post('https://gridproxy.dev.grid.tf/twins?account_id='+ user_address)
        details = r.json()
        return details[0]['twinId']

    def check_withdraw_stellar(self):
        self.browser.find_element(*self.withdraw).click()
        self.browser.find_element(*self.stellar_address).send_keys(get_stellar_address())
        self.browser.find_element(*self.amount_tft).send_keys(0.001)
        return self.browser.find_element(*self.submit_button).is_enabled()

    def check_withdraw_invalid_stellar(self):
        data = [' ', generate_string(), generate_leters(), '!@##$%$E^/>|ز%^(;:^*)']
        self.browser.find_element(*self.withdraw).click()
        self.browser.find_element(*self.amount_tft).send_keys(0.001)
        for i in range(len(data)):
            self.browser.find_element(*self.stellar_address).send_keys(data[i])
            assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'invalid address')]" )
        return self.browser.find_element(*self.submit_button).is_enabled()

    def check_withdraw_tft_amount(self):
        data = [1, 0.001, 1.111]
        boolen = []
        balance = self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text
        data.append(format(float(balance), '.3f'))
        self.browser.find_element(*self.withdraw).click()
        self.browser.find_element(*self.stellar_address).send_keys(get_stellar_address())
        for i in range (len(data)):
            self.browser.find_element(*self.amount_tft).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.amount_tft).send_keys(Keys.DELETE)
            self.browser.find_element(*self.amount_tft).send_keys(data[i])
            boolen.append(self.browser.find_element(*self.submit_button).is_enabled())
        return boolen
    
    def check_withdraw_invalid_tft_amount(self):
        data = [0, 0.000, 0.0, -0.1, -1, -22.2, -1.111]
        balance = self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text
        self.browser.find_element(*self.withdraw).click()
        for i in range (len(data)):
            self.browser.find_element(*self.amount_tft).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.amount_tft).send_keys(Keys.DELETE)
            self.browser.find_element(*self.amount_tft).send_keys(data[i])
            assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Amount cannot be negative or 0')]")
        self.browser.find_element(*self.amount_tft).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.amount_tft).send_keys(Keys.DELETE)
        self.browser.find_element(*self.amount_tft).send_keys('1.0123')
        assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Amount must have 3 decimals only')]")
        self.browser.find_element(*self.amount_tft).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.amount_tft).send_keys(Keys.DELETE)
        self.browser.find_element(*self.amount_tft).send_keys(format(float(balance)+100,'.3f'))
        assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Amount cannot exceed balance')]")
        return self.browser.find_element(*self.submit_button).is_enabled()

    def check_withdraw(self):
        self.browser.find_element(*self.withdraw).click()
        self.browser.find_element(*self.stellar_address).send_keys(get_stellar_address())
        self.browser.find_element(*self.amount_tft).send_keys('0.001')
        self.browser.find_element(*self.submit_button).click()