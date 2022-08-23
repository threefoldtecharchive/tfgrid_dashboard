from tests.selenium.pages.polka import PolkaPage
from tests.selenium.pages.dashboard import DashboardPage
from tests.selenium.utils.utils import generate_string

"""
  Test Suite: TF Grid Dashboard
  Test Cases: TC790 - Create account on TFChain
  Scenario:
      - The user can create an account on TFChain using Polkadot extension.
"""

def test_create_account(browser):

  dashboard_page = DashboardPage(browser)
  polka_page = PolkaPage(browser)

  user = generate_string()
  password = generate_string()

  dashboard_page.load()
  polka_page.authenticate()
  polka_page.add_account(user, password)
 