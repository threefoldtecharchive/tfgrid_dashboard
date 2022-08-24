from frontend_selenium.pages.polka import PolkaPage
from frontend_selenium.pages.dashboard import DashboardPage
from frontend_selenium.utils.utils import generate_string

"""
  Test Suite: TF Grid Dashboard
  Test Cases: TC790 - Create account on TFChain
  Scenario:
      - The user can create an account on TFChain using Polkadot extension.
"""

def test_create_account(browser):

  #Create instance
  dashboard_page = DashboardPage(browser)
  polka_page = PolkaPage(browser)

  #Generate user
  user = generate_string()
  password = generate_string()

  """
   1. Open dashboard page
   2. Authenticate polka
   3. Add account in polka
   4. Verify account created
  """
  dashboard_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
  assert dashboard_page.check_for_only_twin_name() == user
 