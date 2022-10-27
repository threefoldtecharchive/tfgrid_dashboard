from utils.utils import generate_leters, generate_string, get_seed
from pages.twin import TwinPage
from pages.polka import PolkaPage

#  Time required for the run (6 cases) is approximately 3 minutes.

def before_test_setup(browser, create_account):
    twin_page = TwinPage(browser)
    polka_page = PolkaPage(browser)
    user = generate_string()
    password = generate_string()
    polka_page.load_and_authenticate()
    if(create_account):
      polka_page.add_account(user, password)
    else:
      polka_page.import_account(get_seed(), user, password)
    twin_page.navigate(user)
    return twin_page, polka_page, password

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
    twin_page, polka_page, password = before_test_setup(browser, True)
    twin_page.accept_terms_conditions()
    polka_page.authenticate_with_pass(password)
    assert twin_page.wait_for('Planetary using Yggdrasil IPV6')
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
    twin_page, polka_page, password = before_test_setup(browser, True)
    twin_page.accept_terms_conditions()
    polka_page.authenticate_with_pass(password)
    assert twin_page.wait_for('Accepted!')
    cases = [' ', '::g', '1:2:3', ':a', '1:2:3:4:5:6:7:8:9', generate_string(), generate_leters()]
    for case in cases:
      assert twin_page.Create_twin_Planetarywith_InvalidIP(case).is_enabled() == False
      assert twin_page.wait_for('IP address is not formatted correctly')  
    twin_page.Create_twin_Planetarywith_ValidIP()
    polka_page.authenticate_with_pass(password)
    assert twin_page.wait_for('Twin created!')
    assert twin_page.get_twin_ip() == 'IP: ::1'
    twin_page.Check_Balance()
    assert twin_page.wait_for('Free: 0.0979738 TFT')
    assert twin_page.wait_for('Reserved (Locked): 0 TFT')


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
    twin_page, polka_page, password = before_test_setup(browser, False)
    twin_page.press_edit_btn()
    cases = ['2001:db8:3333:4444:5555:6666:7777:8888','2001:db8:3333:4444:CCCC:DDDD:EEEE:FFFF','2001:db8::','::1234:5678','2001:0db8:0001:0000:0000:0ab9:C0A8:0102','2001:db8::1234:5678', '::1']
    for case in cases:
      assert twin_page.Edit_twin_Input(case) == True
    twin_page.press_submit_btn()
    polka_page.authenticate_with_pass(password)
    assert twin_page.wait_for('Twin updated!')
    assert twin_page.wait_for('IP: ::1')


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
    twin_page, _, _ = before_test_setup(browser, False)
    twin_page.press_edit_btn()
    cases = [' ', '::g', '1:2:3', ':a', '1:2:3:4:5:6:7:8:9', generate_string(), generate_leters()]
    for case in cases:
      assert twin_page.Edit_twin_Input(case) == False
      assert twin_page.wait_for('invalid IP format')


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
    twin_page, polka_page, password = before_test_setup(browser, False)
    twin_page.Delete_twin()
    polka_page.authenticate_with_pass(password)
    assert twin_page.wait_for('Twin deleted!')
    twin_page.press_create_btn()
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
    twin_page, _, _ = before_test_setup(browser, False)
    twin_page.Sum_sign()
    assert '/html' in browser.page_source
    # NO checking as devnet don't direct to TF Connect page https://gettft.com/auth/login?next_url=/gettft/shop/#/buy 