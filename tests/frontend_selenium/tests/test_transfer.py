from utils.utils import generate_leters, generate_string, get_seed, valid_amount, invalid_address, invalid_amount, invalid_amount_negtive
from pages.polka import PolkaPage
from pages.transfer import TransferPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Time required for the run (10 cases) is approximately 2 minutes.

def test_transfer_page(browser):
    """
      Test Case: TC982 - Navigate to transfer
      Steps:
          - Navigate to the dashboard.
          - Select an account.
          - Click on Transfer from side menu.
      Result: User should be navigated to Transfer page.
    """
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    transfer_page.navigate(user)
    assert 'Transfer TFTs on the TFChain' in browser.page_source


def test_recipient_list(browser):
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
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    user1 = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    polka_page.add_account(user1, password)
    twin_address = browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div/div[2]').text
    transfer_page.navigate(user)
    assert transfer_page.recipient_list() == twin_address


def test_valid_receipient(browser):
    """
    Test Case: TC984 - Valid Receipient
      Steps:
          -Navigate to the dashboard.
          -Select an account.
          -Click on Transfer from side menu. -Type valid address in recipient input.
      Results: Accepting address with no alerts
    """
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_address = browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div[2]').text
    transfer_page.navigate(user)
    transfer_page.recipient_input(twin_address)
    transfer_page.amount_tft_input(valid_amount())
    assert transfer_page.get_submit().is_enabled() == True


def test_invalid_address(browser):
    """
    Test Case: TC985 -Invalid Address
    Steps:
      - Navigate to the dashboard.
      - Select an account.
      - Click on Transfer from side menu.
      - Type invalid address in recipient input.
    Results: Alert message "invalid address"
    """
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    transfer_page.navigate(user)
    cases = [' ', generate_string(), invalid_address(), generate_leters()]
    transfer_page.amount_tft_input(valid_amount())
    for case in cases:
      transfer_page.recipient_input(cases)
      assert transfer_page.get_submit().is_enabled() == False
      assert browser.find_element(By.XPATH, "//*[contains(text(), 'invalid address')]")
    

def test_valid_amount(browser):
    """
    Test Case: TC986 - Valid amount
    Steps:
        - Navigate to the dashboard.
        - Select an account.
        - Click on Transfer from side menu.
        - Type valid amount in TFT input.
    Result: User gets no alerts
    """
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_address = browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div[2]').text
    transfer_page.navigate(user)
    transfer_page.recipient_input(twin_address)
    transfer_page.amount_tft_input(valid_amount())
    assert transfer_page.get_submit().is_enabled() == True


def test_invalid_amount(browser):
    """
    Test Case: TC987 - InValid amount
    Steps:
        - Navigate to the dashboard.
        - Select an account.
        - Click on Transfer from side menu.
        - Type Invalid amount in TFT input.
    Result: Alert with message "Amount cannot be negative or 0"
    """
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_address = browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div/div/div[2]').text
    transfer_page.navigate(user)
    transfer_page.recipient_input(twin_address)
    balance = transfer_page.get_balance()
    cases = [0, -900.009, invalid_amount_negtive()]
    for case in cases:
      transfer_page.amount_tft_input(case)
      assert transfer_page.get_submit().is_enabled() == False
      assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount cannot be negative or 0')]")
    transfer_page.amount_tft_input(invalid_amount())
    assert transfer_page.get_submit().is_enabled() == False
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount must have 3 decimals only')]")
    transfer_page.amount_tft_input(format(float(balance)+100,'.3f'))
    assert transfer_page.get_submit().is_enabled() == False
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Amount cannot exceed balance')]")


def test_transfer_TFTs_on_TFChain (browser):
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
    transfer_page = TransferPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    user1 = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    polka_page.add_account(user1, password)
    twin_address = browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div/div[2]').text
    transfer_page.navigate(user)
    balance = transfer_page.get_balance()
    min_balance = float(balance)-1
    max_balance = float(balance)-1.1
    transfer_page.recipient_input(twin_address)
    transfer_page.amount_tft_input(1.01)
    transfer_page.get_submit().click()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer succeeded!')]")))
    assert format(float(min_balance),'.3f') <= format(float(browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[1]/header/div/div[3]/div[1]/div[1]/div[1]/button/span/p[1]').text),'.3f') >= format(float(max_balance),'.3f')
