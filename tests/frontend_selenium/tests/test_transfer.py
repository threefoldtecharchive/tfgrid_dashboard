from pages.polka import PolkaPage
from pages.transfer import TransferPage
from utils.utils import generate_string

"""
  Test Case: TC982 - Navigate to transfer
  Steps:
      - Navigate to the dashboard.
      - Select an account.
      - Click on Transfer from side menu.
  Result: User should be navigated to Transfer page.
"""
def test_transfer_page(browser):
  seed = 'expect flame equal life foster riot march own drum gas portion spy'

  transfer_page = TransferPage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  transfer_page.load()
  polka_page.authenticate()
  polka_page.import_account(seed, user, password)
  transfer_page.navigate(user)
  assert 'Transfer TFTs on the TFChain' in browser.page_source


"""
  Test Case: TC983 - Recipient List
  Steps:
      - Navigate to the dashboard.
      - Create 2 accounts.
      - Select an account.
      - Click on Transfer from side menu
      - Click on recipient list
  Result: Other unselected account twin address should be the only listed..
"""