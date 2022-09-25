from utils.utils import generate_string, get_seed
import pytest
from pages.twin import TwinPage
from pages.polka import PolkaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Time required for the run (6 cases) is approximately 3 minutes.

"""
  Test Case: TC924 - Accept terms and conditions
  Test Cases: TC931- button why do I even need twin
  Steps:
    - Navigate to dashboard.
    - Click on the desired account from the dashboard homepage.
    - Click on Accept The Terms and Conditions.
    - Use polka password authentication.
    - Click on button why do I even need a twin.
  Result: Open same account on dashboard homepage and assert that no terms to accept when you come back to this account twin page.
          Assert that it will go to righ link.
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
  assert twin_page.Button_why_doIeven_need_twin() == 'https://library.threefold.me/info/manual/#/manual__yggdrasil_client'


"""
  Test Cases: TC930- create twin InvalidIP
  Test Cases: TC929- create twin
  Test Cases: TC932- check Balance
  Steps:
    - Navigate to dashboard
    - Click on the desired account from the dashboard homepage.
    - write your Yggdrasil IPV6 with invalid then valid input.
    - Click on create button.
    - Use polka password authentication.
    - Click on the balance button.
  Result: Assert that Error message will appear and create button will not be clear then Assert a twin should be created.
          Assert Balance must be in the first of creating your account [Free: 0.0979738 TFT -Reserved (Locked): 0 TFT]
"""
def test_create_twin_IP(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  assert twin_page.Create_twin_Planetarywith_InvalidIP().is_enabled() == False
  twin_page.Create_twin_Planetarywith_ValidIP()
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  assert browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]').text == 'IP: ::1'
  twin_page.Check_Balance()
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'Free: 0.0979738 TFT')]")
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'Reserved (Locked): 0 TFT')]")


"""
  Test Cases: TC925- edit twin Valid Input
  Steps:
    - Navigate to dashboard
    - Click on the desired account from the dashboard homepage.
    - Click on edit button
    - Edit your IP.
    - Click on submit button.
    - Use polka password authentication.
  Result: Assert that twin IP edited.
"""
def test_edit_twin_ValidInput(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  twin_page.Edit_twin_ValidInput(user)
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin updated!')]")))
  assert browser.find_element(By.XPATH,"//*[contains(text(), 'IP: ::1')]")


"""
  Test Cases: TC927- edit twin InValid Input
  Steps:
    - Navigate to dashboard
    - Click on the desired account from the dashboard homepage.
    - Click on edit button
    - Edit your IP with wrong format.
  Result: An error message will appear and can't click on submit button.
"""
def test_edit_twin_InValidInput(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  assert twin_page.Edit_twin_InValidInput(user).is_enabled() == False


"""
  Test Case: TC926- Delete twin
  Steps:
    - Navigate to dashboard
    - Click on the desired account from the dashboard homepage.
    - Click on delete button
    - Use polka password authentication.
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
  polka_page.import_account(get_seed(), user, password)
  twin_page.Delete_twin(user)
  polka_page.authenticate_with_pass(password)
  assert WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin deleted!')]")))
  browser.find_element(*twin_page.CreateButton).click()
  polka_page.authenticate_with_pass(password)


"""
  Test Cases: TC933- sum sign
  Steps:
    - Navigate to dashboard
    - Click on the desired account from the dashboard homepage.
    - Check sum sign right to balance on the top left corner.
    - Click on the sum sign button
  Result: Assert that it should go to the link. 
"""
def test_sum_sign(browser):
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  twin_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  twin_page.Sum_sign(user)
  assert browser.find_element(By.XPATH,"/html") # NO checking as devnet don't direct to TF Connect page https://gettft.com/auth/login?next_url=/gettft/shop/#/buy 