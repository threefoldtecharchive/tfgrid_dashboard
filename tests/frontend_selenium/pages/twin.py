from utils.utils import generate_string,generate_leters
from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
This module contains Twin page elements.
"""
class TwinPage:

    accept_terms_condition = (By.XPATH, '//*[@id="app"]/div[3]/div/button')
    EditButton=(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[2]/button[1]')
    EditInput=(By.XPATH, '/html/body/div[1]/div[4]/div/div/div[1]/div/form/div/div/div[1]/div/input')
    SubmitButton=(By.XPATH, '//*[@id="app"]/div[4]/div/div/div[2]/button[2]')
    DeleteButton=(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[2]/button[2]')
    OKButton=(By.XPATH, '//*[@id="app"]/div[4]/div/div/div[3]/button[2]')
    CreateButton=(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/button')
    twinIpInput=(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/form/div/div/div[1]/div/input')
    WhyButton=(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[2]/div/div/a')
    BalanceButton=(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button')
    SumButton=(By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[2]/button')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='app']/div[1]/div[3]/div/div/div/div[1]/div/div/div/div/div/div[1]/div[3]")))

    def accept_terms_conditions(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="app"]/div[3]/div/iframe')))
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/p[1]/img')))
        self.browser.find_element(By.XPATH, '/html/body/main/aside/div[2]/ul[3]/li/a').click()
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/p[1]/img')))
        self.browser.find_element(By.XPATH, '//*[@id="cc_dialog"]/div/div[2]/button[1]').click()
        self.browser.switch_to.default_content()
        time.sleep(6)
        self.browser.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/button').click()
        time.sleep(6)
        
    def Create_twin_Planetarywith_ValidIP(self):
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted!')]")))
        self.browser.find_element(*self.twinIpInput).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.twinIpInput).send_keys(Keys.DELETE)
        self.browser.find_element(*self.twinIpInput).send_keys("::1")
        self.browser.find_element(*self.CreateButton).click()

    def Create_twin_Planetarywith_InvalidIP(self):
        cases = [' ', '::g', '1:2:3', ':a', '1:2:3:4:5:6:7:8:9', generate_string(), generate_leters()]
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted!')]")))
        for case in cases:
            self.browser.find_element(*self.twinIpInput).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.twinIpInput).send_keys(Keys.DELETE)
            self.browser.find_element(*self.twinIpInput).send_keys(case)
            assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'IP address is not formatted correctly')]")
        return self.browser.find_element(*self.CreateButton)   
    
    def Button_why_doIeven_need_twin(self):
        self.browser.find_element(*self.WhyButton).click()
        WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[1])
        return self.browser.current_url   

    def Edit_twin_ValidInput(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.EditButton).click()
        cases = ['2001:db8:3333:4444:5555:6666:7777:8888','2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF','2001:db8::','::1234:5678','2001:0db8:0001:0000:0000:0ab9:C0A8:0102','2001:db8::1234:5678', '::1']
        for case in cases:
            self.browser.find_element(*self.EditInput).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.EditInput).send_keys(Keys.DELETE)
            self.browser.find_element(*self.EditInput).send_keys(case)
            assert self.browser.find_element(*self.SubmitButton).is_enabled() == True
        self.browser.find_element(*self.SubmitButton).click()

    def Edit_twin_InValidInput(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.EditButton).click()
        cases = [' ', '::g', '1:2:3', ':a', '1:2:3:4:5:6:7:8:9', generate_string(), generate_leters()]
        for case in cases:
            self.browser.find_element(*self.EditInput).send_keys(Keys.CONTROL + "a")
            self.browser.find_element(*self.EditInput).send_keys(Keys.DELETE)
            self.browser.find_element(*self.EditInput).send_keys(case)
            assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'invalid IP format')]")
        return self.browser.find_element(*self.SubmitButton)

    def Delete_twin(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.DeleteButton).click()
        assert self.browser.find_element(By.XPATH,"//*[contains(text(), 'Are you certain you want to delete this twin?')]")
        self.browser.find_element(*self.OKButton).click()
    
    def Check_Balance(self):        
        self.browser.find_element(*self.BalanceButton).click()

    def Sum_sign(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.browser.find_element(*self.SumButton).click()
