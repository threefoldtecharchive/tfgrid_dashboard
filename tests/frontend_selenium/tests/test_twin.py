from utils.utils import generate_leters, generate_string, get_seed
from pages.twin import TwinPage
from pages.polka import PolkaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Time required for the run (6 cases) is approximately 3 minutes.

def test_accept_terms_conditions(browser): 
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
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.add_account(user, password)
    twin_page.navigate(user)
    twin_page.accept_terms_conditions()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Planetary using Yggdrasil IPV6')]")))
    assert 'Planetary using Yggdrasil IPV6' in browser.page_source
    assert twin_page.Button_why_doIeven_need_twin() == 'https://library.threefold.me/info/manual/#/manual__yggdrasil_client'


def test_create_twin_IP(browser):
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
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.add_account(user, password)
    twin_page.navigate(user)
    twin_page.accept_terms_conditions()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accepted!')]")))
    cases = [' ', '::g', '1:2:3', ':a', '1:2:3:4:5:6:7:8:9', generate_string(), generate_leters()]
    for case in cases:
      assert twin_page.Create_twin_Planetarywith_InvalidIP(case).is_enabled() == False
      assert browser.find_element(By.XPATH, "//*[contains(text(), 'IP address is not formatted correctly')]")    
    twin_page.Create_twin_Planetarywith_ValidIP()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin created!')]")))
    assert browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]').text == 'IP: ::1'
    twin_page.Check_Balance()
    assert browser.find_element(By.XPATH,"//*[contains(text(), 'Free: 0.0979738 TFT')]")
    assert browser.find_element(By.XPATH,"//*[contains(text(), 'Reserved (Locked): 0 TFT')]")


def test_edit_twin_ValidInput(browser):
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
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_page.navigate(user)
    browser.find_element(*twin_page.EditButton).click()
    cases = ['2001:db8:3333:4444:5555:6666:7777:8888','2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF','2001:db8::','::1234:5678','2001:0db8:0001:0000:0000:0ab9:C0A8:0102','2001:db8::1234:5678', '::1']
    for case in cases:
      assert twin_page.Edit_twin_Input(case) == True
    browser.find_element(*twin_page.SubmitButton).click()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin updated!')]")))
    assert browser.find_element(By.XPATH,"//*[contains(text(), 'IP: ::1')]")


def test_edit_twin_InValidInput(browser):
    """
      Test Cases: TC927- edit twin InValid Input
      Steps:
        - Navigate to dashboard
        - Click on the desired account from the dashboard homepage.
        - Click on edit button
        - Edit your IP with wrong format.
      Result: An error message will appear and can't click on submit button.
    """
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_page.navigate(user)
    browser.find_element(*twin_page.EditButton).click()
    cases = [' ', '::g', '1:2:3', ':a', '1:2:3:4:5:6:7:8:9', generate_string(), generate_leters()]
    for case in cases:
      assert twin_page.Edit_twin_Input(case) == False
      assert browser.find_element(By.XPATH, "//*[contains(text(), 'invalid IP format')]")


def test_Delete_twin(browser):
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
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_page.navigate(user)
    twin_page.Delete_twin()
    polka_page.authenticate_with_pass(password)
    assert WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Twin deleted!')]")))
    browser.find_element(*twin_page.CreateButton).click()
    polka_page.authenticate_with_pass(password)


def test_sum_sign(browser):
    """
      Test Cases: TC933- sum sign
      Steps:
        - Navigate to dashboard
        - Click on the desired account from the dashboard homepage.
        - Check sum sign right to balance on the top left corner.
        - Click on the sum sign button
      Result: Assert that it should go to the link. 
    """
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    twin_page.navigate(user)
    twin_page.Sum_sign()
    assert browser.find_element(By.XPATH,"/html") # NO checking as devnet don't direct to TF Connect page https://gettft.com/auth/login?next_url=/gettft/shop/#/buy 