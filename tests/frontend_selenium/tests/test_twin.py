from utils.utils import generate_string,generate_leters
import pytest
from pages.twin import TwinPage
from pages.polka import PolkaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Time required for the run (18 cases) is approximately 17 minutes.

"""
  Test Case: TC924 - Accept terms and conditions
  Steps:
      -Navigate to dashboard.
      -Click on the desired account from the dashboard homepage.
      -Click on Accept The Terms and Conditions.
      -Use polka password authentication.
      -Retry open same account again.
  Result: Open same account on dashboard homepage and assert that no terms to accept when you come back to this account twin page.
"""
def test_accept_terms_conditions(browser): 
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Planetary using Yggdrasil IPV6')]")))
  assert 'Planetary using Yggdrasil IPV6' in browser.page_source

"""
  Test Case: TC926- Delete twin
  Steps:
      -Navigate to dashboard
      -Click on the desired account from the dashboard homepage.
      -Click on delete button
      -Use polka password authentication.
  Result: Assert that If it's the only account it will show new page to make a new account,
          If there's another accounts Search on account you deleted and check if it deleted or not.
"""
def test_Delete_twin(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password) 
  twin_page.Delete_twin()
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Planetary using Yggdrasil IPV6')]")))
  assert 'Planetary using Yggdrasil IPV6' in browser.page_source

"""
  Test Cases: TC931- button why do I even need twin
  Steps:
      -After open account on dashboard home page.
      -Click on button why do I even need a twin.
  Result: Assert that it will go to righ link.
"""
def test_button_why_doIeven_need_twin(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Button_why_doIeven_need_twin()
  assert browser.find_element(By.XPATH,"/html/body")


"""
  Test Cases: TC930- create twin InvalidIP
  Steps:
      -After open account on dashboard page.
      -Should create twin Planetary using Yggdrasil IPV6.
      -write your Yggdrasil IPV6 with invalid input..
  Result: Assert that Error message will appear and create button will not be clear.
"""
@pytest.mark.parametrize('cases', [' ',generate_string(),generate_leters()])
def test_create_twin_InvalidIP(browser,cases):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password) 
  twin_page.Create_twin_Planetarywith_InvalidIP(cases)
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'IP address is not formatted correctly')]")


"""
  Test Cases: TC929- create twin
  Steps:
      -Navigate to dashboard
      -Click on the desired account from the dashboard homepage.
      -write your Yggdrasil IPV6 with valid input.
      -Click on create button.
      -Use polka password authentication..
  Result: Assert a twin should be created.
"""
@pytest.mark.parametrize('cases',['2001:db8:3333:4444:5555:6666:7777:8888'])
def test_create_twin(browser,cases):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password) 
  twin_page.Create_twin_Planetarywith_ValidIP(cases)
  polka_page.authenticate_with_pass(password)

"""
  Test Cases: TC932- check Balance
  Steps:
      -Navigate to dashboard
      -Click on the desired account from the dashboard homepage.
      -Check balance on the top left corner.
      -Click on the balance button.
      -Click on close button.
  Result: Assert Balance must be in the first of creating your account
          Free: 0.0979738 TFT
          Reserved (Locked): 0 TFT
"""
def test_check_Balance(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password) 
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password) 
  twin_page.Check_Balance()
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'Free: 0.0979738 TFT')]")
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'Reserved (Locked): 0 TFT')]")

"""
  Test Cases: TC927- edit twin InValid Input
  Steps:
      -Navigate to dashboard
      -Click on the desired account from the dashboard homepage.
      -Click on edit button
      -Edit your IP with wrong format.
  Result: An error message will appear and can't click on submit button.
"""
@pytest.mark.parametrize('cases', [' ',generate_string(),generate_leters()])
def test_edit_twin_InValidInput(browser,cases):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password) 
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password) 
  twin_page.Edit_twin_InValidInput(cases)
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'invalid IP format')]")


"""
  Test Cases: TC925- edit twin Valid Input
  Steps:
      -Navigate to dashboard
      -Click on the desired account from the dashboard homepage.
      -Click on edit button
      -Edit your IP.
      -Click on submit button.
      -Use polka password authentication.
  Result: Assert that twin IP edited.
"""
@pytest.mark.parametrize('cases', ['2001:db8:3333:4444:5555:6666:7777:8888','2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF','2001:db8::','::1234:5678','2001:0db8:0001:0000:0000:0ab9:C0A8:0102','2001:db8::1234:5678'])
def test_edit_twin_ValidInput(browser,cases):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password) 
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password) 
  twin_page.Edit_twin_ValidInput(cases)
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin updated!')]")))
  assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ cases +"')]")

"""
  Test Cases: TC933- sum sign
  Steps:
      -Navigate to dashboard
      -Click on the desired account from the dashboard homepage.
      -Check sum sign right to balance on the top left corner.
      -Click on the sum sign button
  Result: Assert that it should go to the link. 
"""
def test_sum_sign(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password) 
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password) 
  twin_page.Sum_sign()
  assert browser.find_element(By.XPATH,"/html")


 
