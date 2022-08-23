from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.selenium.utils.base import Base

"""
This module contains all polkadot needed utils.
"""

class PolkaPage:
  
  PolkaUnderstand = (By.XPATH ,'//*[@id="root"]/main/div[4]/button')
  PolkaAllow = (By.XPATH ,'//*[@id="root"]/main/div[1]/div[2]/div/button')
  PolkaAddAccountIcon = (By.XPATH ,'//*[@id="root"]/main/div[1]/div/div[2]/div[1]')
  PolkaAddAccount = (By.XPATH ,'//*[@id="root"]/main/div[1]/div/div[3]/div[1]/a')
  PolkaCheckBox = (By.XPATH ,'//*[@id="root"]/main/div[6]/label/span')
  PolkaNextStep = (By.XPATH ,'//*[@id="root"]/main/div[7]/button')
  PolkaUserName = (By.XPATH ,'//*[@id="root"]/main/div[4]/div/input')
  PolkaUserPass = (By.XPATH ,'//*[@id="root"]/main/div[5]/div/input')
  PolkaUserRePass = (By.XPATH ,'//*[@id="root"]/main/div[6]/div/input')
  PolkaSubmit = (By.XPATH ,'//*[@id="root"]/main/div[8]/button[2]')
  PolkaAuthPass = (By.XPATH ,'//*[@id="root"]/main/div[3]/div[1]/div/input')
  PolkaAuthSubmit = (By.XPATH ,'//*[@id="root"]/main/div[3]/button/div[1]')

  def __init__(self, browser):
    self.browser = browser
    
  def Authenticate(self):
    WebDriverWait(self.browser, 20).until(EC.number_of_windows_to_be(2))
    self.browser.switch_to.window(self.browser.window_handles[1])
    self.browser.find_element(*self.PolkaUnderstand).click()
    self.browser.find_element(*self.PolkaAllow).click()
    self.browser.switch_to.window(self.browser.window_handles[0])
  
  def AddAccount(self, Name, Pass):
    self.browser.execute_script("window.open('');")
    self.browser.switch_to.window(self.browser.window_handles[1])
    self.browser.get(Base.extension_url)
    self.browser.find_element(*self.PolkaAddAccountIcon).click()
    self.browser.find_element(*self.PolkaAddAccount).click()
    self.browser.find_element(*self.PolkaCheckBox).click()
    self.browser.find_element(*self.PolkaNextStep).click()
    self.browser.find_element(*self.PolkaUserName).send_keys(Name)
    self.browser.find_element(*self.PolkaUserPass).send_keys(Pass)
    self.browser.find_element(*self.PolkaUserRePass).send_keys(Pass)
    self.browser.find_element(*self.PolkaSubmit).click()
    self.browser.close()
    self.browser.switch_to.window(self.browser.window_handles[0])

  def AuthenticateWithPass(self, Pass):
    WebDriverWait(self.browser, 20).until(EC.number_of_windows_to_be(2))
    self.browser.switch_to.window(self.browser.window_handles[1])
    self.browser.find_element(*self.PolkaAuthPass).send_keys(Pass)
    self.browser.find_element(*self.PolkaAuthSubmit).click()
    self.browser.switch_to.window(self.browser.window_handles[0])