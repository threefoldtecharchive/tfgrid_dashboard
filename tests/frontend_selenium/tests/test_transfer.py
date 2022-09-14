from utils.utils import generate_string, invalid_address , invalid_amount, valid_address,valid_amount,invalid_amount_negtive,invalid_exceed_balance
from pages.twin import TwinPage
from pages.polka import PolkaPage
from pages.transfer import TransferPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


"""
  Test Case: TC982 - Navigate to transfer
  Steps:
      - Navigate to the dashboard.
      - Select an account.
      - Click on Transfer from side menu.
  Result: User should be navigated to Transfer page.
"""
def test_transfer_page(browser):
  transfer_page = TransferPage(browser)
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  assert 'Transfer TFTs on the TFChain' in browser.page_source


"""
Test Case: TC986 - Valid amount
Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on Transfer from side menu.
    - Type valid amount in TFT input.
Result: User gets no alerts
"""
def test_valid_amount(browser):
  cases=valid_amount()
  twin_page = TwinPage(browser)
  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  element=transfer_page.amount_TFT_valid_input(cases)
  assert element.is_enabled()==True


"""
Test Case: TC987 - InValid amount
Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on Transfer from side menu.
    - Type Invalid amount in TFT input.
Result: Alert with message "Amount cannot be negative or 0"
"""
@pytest.mark.parametrize('cases', ['0',invalid_amount_negtive()])
def test_invalid_amount_zero_negative(browser,cases):
  twin_page = TwinPage(browser)
  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account( user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  transfer_page.amount_TFT_invalid_input(cases)
  assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount cannot be negative or 0')]") 

def test_invalid_amount_decimals(browser):
  cases= invalid_amount()
  twin_page = TwinPage(browser)
  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account( user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  transfer_page.amount_TFT_invalid_input(cases)
  assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount must have 3 decimals only')]")

def test_invalid_amount_exceed_balance(browser):
  cases= invalid_exceed_balance()
  twin_page = TwinPage(browser)
  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account( user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  transfer_page.amount_TFT_invalid_input(cases)
  assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount cannot exceed balance')]")


"""
Test Case: TC985 -Invalid Address
Steps:
  - Navigate to the dashboard.
  - Select an account.
  - Click on Transfer from side menu.
  - Type invalid address in recipient input.
Results: Alert message "invalid address"
"""
def test_invalid_address(browser):
  cases= invalid_address()
  twin_page = TwinPage(browser)
  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  transfer_page.recipient_invalid_input(cases)
  assert browser.find_elements(By.XPATH,"//*[contains(text(), 'invalid address')]")


"""
  Test Case: TC983 - Recipient List
  Steps:
      - Navigate to the dashboard.
      - Create 2 accounts.
      - Select an account.
      - Click on Transfer from side menu
      - Click on recipient list
  Result: Other unselected account twin address should be the only listed.
"""
def test_recipient_list(browser):
  transfer_page = TransferPage(browser)
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  user1 = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account(user1, password)
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  transfer_page.recipient_list()


"""
Test Case: TC984 - Valid Receipient
  Steps:
      -Navigate to the dashboard.
      -Select an account.
      -Click on Transfer from side menu. -Type valid address in recipient input.
  Results: Accepting address with no alerts
"""
def test_valid_receipient(browser):
  cases= valid_address()
  twin_page = TwinPage(browser)
  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  amount=valid_amount()
  element=transfer_page.recipient_valid_input(cases,amount)
  assert element.is_enabled()==True


"""
Test Case: TC988 -Transfer TFTs on the TFChain
Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on Transfer from side menu.
    - Type valid address in recipient input.
    - Type valid amount in TFT input.
    - Click submit button.
Result: Amount should dedicate from this account twin and transferred to the typed address.
"""
@pytest.mark.parametrize("address,amount", [(valid_address(), valid_amount())])
def test_transfer_TFTs_on_TFChain (browser,address,amount):
  transfer_page = TransferPage(browser)
  twin_page = TwinPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
  twin_page.accept_terms_conditions(user)
  polka_page.authenticate_with_pass(password)
  twin_page.Create_twin_Planetarywith_ValidIP('::1')
  polka_page.authenticate_with_pass(password)  
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
  transfer_page.navigate(user)
  transfer_page.transfer_TFTs_on_TFChain(address,amount)
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer succeeded!')]")))
  