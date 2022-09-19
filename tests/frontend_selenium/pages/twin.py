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

    Account=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div')
    accept_terms_condition = (By.XPATH, '//*[@id="app"]/div[3]/div/button')
    PolkaPassword=(By.XPATH,'//*[@id="root"]/main/div[3]/div[1]/div/input')
    SignButton=(By.XPATH,'//*[@id="root"]/main/div[3]/button/div[1]')
    EditButton=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/button[1]')
    EditInput=(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[1]/div/form/div/div/div[1]/div/input')
    SubmitButton=(By.XPATH,'//*[@id="app"]/div[4]/div/div/div[2]/button[2]/span')
    DeleteButton=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[2]/button[2]')
    Deletetitile=(By.XPATH,'//*[@id="app"]/div[4]/div/div/div[1]')
    OKButton=(By.XPATH,'//*[@id="app"]/div[4]/div/div/div[3]/button[2]')
    titletwin=(By.XPATH,'///*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/div[1]/h2')
    CreateButton=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/button')
    twinIpInput=(By.XPATH,'/html/body/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/form/div/div/div[1]/div/input')
    WhyButton=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[2]/div/div/a')
    BalanceButton=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]/div[1]/button/span')
    SumButton=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]/div[2]/button/span')
    win=(By.XPATH,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[2]')

    def __init__(self, browser):
        self.browser = browser
    
    def load(self):
        self.browser.get(Base.base_url)
   
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
        
    def Create_twin_Planetarywith_ValidIP(self,cases):
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted!')]")))
        for _ in range (0,3):
         self.browser.find_element(*self.twinIpInput).send_keys(Keys.BACKSPACE)
        self.browser.find_element(*self.twinIpInput).send_keys(cases)
        self.browser.find_element(*self.CreateButton).click()   
    
    def Button_why_doIeven_need_twin(self):
        self.browser.find_element(*self.Account).click()
        self.browser.find_element(*self.WhyButton).click()
    
    def Create_twin_Planetarywith_InvalidIP(self,cases):
        WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted!')]")))
        for _ in range (0,3):
         self.browser.find_element(*self.twinIpInput).send_keys(Keys.BACKSPACE)
        self.browser.find_element(*self.twinIpInput).send_keys(cases)

    def Edit_twin_ValidInput(self,cases):
        self.browser.find_element(*self.EditButton).click()
        self.browser.find_element(*self.EditInput).send_keys(cases)
        self.browser.find_element(*self.SubmitButton).click()

    def Edit_twin_InValidInput(self,cases):
        self.browser.find_element(*self.EditButton).click()
        self.browser.find_element(*self.EditInput).send_keys(cases)

    def Delete_twin(self):
        self.browser.find_element(*self.DeleteButton).click()
        assert self.browser.find_element(By.XPATH,"//*[contains(text(), 'Are you certain you want to delete this twin?')]")
        self.browser.find_element(*self.OKButton).click()
    
    def Check_Balance(self):        
        self.browser.find_element(*self.BalanceButton).click()

    def Sum_sign(self):
        self.browser.find_element(*self.SumButton).click()
