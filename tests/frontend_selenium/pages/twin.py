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
    terms_ifram = (By.XPATH, '//*[@id="app"]/div[3]/div/iframe')
    iframe_img_load = (By.XPATH, '//*[@id="main"]/p[1]/img')
    tf_iframe_page = (By.XPATH, '/html/body/main/aside/div[2]/ul[3]/li/a')
    iframe_dialog_icon = (By.XPATH, '//*[@id="cc_dialog"]/div/div[2]/button[1]')
    accept_alert = (By.XPATH, "//*[contains(text(), 'Accepted!')]")
    twin_ip_text = (By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]')

    def __init__(self, browser):
        self.browser = browser
        
    def navigate(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()

    def accept_terms_conditions(self):
        WebDriverWait(self.browser, 30).until(EC.frame_to_be_available_and_switch_to_it(self.terms_ifram))
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.iframe_img_load))
        self.browser.find_element(*self.tf_iframe_page).click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.iframe_img_load))
        self.browser.find_element(*self.iframe_dialog_icon).click()
        self.browser.switch_to.default_content()
        time.sleep(6)
        self.browser.find_element(*self.accept_terms_condition).click()
        time.sleep(6)
        
    def Create_twin_Planetarywith_ValidIP(self):
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.accept_alert))
        self.browser.find_element(*self.twinIpInput).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.twinIpInput).send_keys(Keys.DELETE)
        self.browser.find_element(*self.twinIpInput).send_keys("::1")
        self.browser.find_element(*self.CreateButton).click()

    def Create_twin_Planetarywith_InvalidIP(self, data):
        self.browser.find_element(*self.twinIpInput).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.twinIpInput).send_keys(Keys.DELETE)
        self.browser.find_element(*self.twinIpInput).send_keys(data)
        return self.browser.find_element(*self.CreateButton)   
    
    def Button_why_doIeven_need_twin(self):
        self.browser.find_element(*self.WhyButton).click()
        WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[1])
        return self.browser.current_url

    def Edit_twin_Input(self, data):
        self.browser.find_element(*self.EditInput).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.EditInput).send_keys(Keys.DELETE)
        self.browser.find_element(*self.EditInput).send_keys(data)
        return self.browser.find_element(*self.SubmitButton).is_enabled()

    def Delete_twin(self):
        self.browser.find_element(*self.DeleteButton).click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.OKButton))
        self.browser.find_element(*self.OKButton).click()
    
    def Check_Balance(self):        
        self.browser.find_element(*self.BalanceButton).click()

    def Sum_sign(self):
        self.browser.find_element(*self.SumButton).click()

    def wait_for(self, keyword):
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '"+ keyword +"')]")))
        return True
    
    def get_twin_ip(self):
        return self.browser.find_element(*self.twin_ip_text).text
    
    def press_edit_btn(self):
        self.browser.find_element(*self.EditButton).click()
    
    def press_submit_btn(self):
        self.browser.find_element(*self.SubmitButton).click()
    
    def press_create_btn(self):
        self.browser.find_element(*self.CreateButton).click()