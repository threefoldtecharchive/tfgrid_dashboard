from utils.utils import generate_string, get_seed
from pages.swap import SwapPage
from pages.polka import PolkaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#  Time required for the run (11 cases) is approximately 3 minutes.

"""
  Test Case: TC1112 Navigate swap
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
  Result: swap page open.
"""
def test_navigate_swap(browser):
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  assert 'Transfer TFT Across Chains' in browser.page_source


"""
  Test Case: TC1113 transfer chain
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
  Result: Steller should be selected.
"""
def test_transfer_chain(browser):
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()


"""
  Test Case: TC1114 choose deposit
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on deposit button.
    - Click on close button.
  Result: Deposit tft will be shown.
"""
def test_choose_deposit(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  swap_page.choose_deposit()
  assert 'Deposit TFT' in browser.page_source


"""
  Test Case: TC1115 choose withdraw
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on withdraw button.
    - Click on close button.
  Result: withdraw tft will be shown.
"""
def test_choose_withdraw(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  swap_page.choose_withdraw()
  assert 'Withdraw TFT' in browser.page_source


"""
  Test Case: TC1116 how it done
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on how it's done text.
  Result: it will go to link
"""
def test_how_it_done(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  assert swap_page.how_it_done() in 'https://library.threefold.me/info/manual/#/manual__grid3_stellar_tfchain_bridge'


"""
  Test Case: TC1117 check deposit
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on deposit button.
    - Click on close button.
  Result: Assert that Destination and memo text will come from drid proxy.
"""
def test_check_deposit(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  user_address = swap_page.twin_addres()
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  assert int(swap_page.check_deposit()[-3:]) == swap_page.get_twin_id(user_address)


"""
  Test Case: TC1118 check withdraw stellar
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on withdraw button.
    - Put stellar Address.
    - Click on close button.
  Result: Assert that stellar address is right.
"""
def test_check_withdraw_stellar(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  assert swap_page.check_withdraw_stellar() == True


"""
  Test Case: TC1143 - Check withdraw invalid Stellar address
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on withdraw button.
    - Put stellar Address.
    - Click on close button.
  Result: Alert with message "invalid address" should be displayed.
"""
def test_check_withdraw_invalid_stellar(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  assert swap_page.check_withdraw_invalid_stellar() == False


"""
  Test Case: TC1131 check withdraw tft amount
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on withdraw button.
    - Put amount of tft you want to send.
    - Click on close button.
  Result: Assert that the amount of tft is right.
"""
def test_check_withdraw_tft_amount(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  for bool in swap_page.check_withdraw_tft_amount():
    assert bool == True


"""
  Test Case: TC1144 - Check withdraw invalid TFT amount
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on withdraw button.
    - Put amount of tft you want to send.
    - Click on close button.
  Result: Alert with message "Amount cannot be negative or 0" should be displayed.
"""
def test_check_withdraw_invalid_tft_amount(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  assert swap_page.check_withdraw_invalid_tft_amount() == False


"""
  Test Case: TC1132 check withdraw 
  Steps:
    - Navigate to the dashboard.
    - Select an account.
    - Click on swap from side menu.
    - Click on chain list.
    - Click on withdraw button.
    - Put stellar Address.
    - Put amount of tft you want to send.
    - Click on close button.
  Result: Assert that Amount of tft should send to the stellar.
"""
def test_check_withdraw(browser): 
  swap_page = SwapPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  swap_page.load() 
  polka_page.authenticate()
  polka_page.import_account(get_seed(), user, password)
  swap_page.navigate_to_swap(user)
  swap_page.transfer_chain()
  balance = browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text
  min_balance = float(balance)-1
  max_balance = float(balance)-1.1
  swap_page.check_withdraw()
  polka_page.authenticate_with_pass(password)
  WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Withdraw submitted!')]" )))
  assert format(float(min_balance),'.3f') <= format(float(browser.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text),'.3f') >= format(float(max_balance),'.3f')  