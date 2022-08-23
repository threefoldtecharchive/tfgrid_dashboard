from tests.selenium.pages.polka import PolkaPage
from tests.selenium.pages.dashboard import DashboardPage
from tests.selenium.utils.utils import GenerateString

"""
  Test Suite: TF Grid Dashboard
  Test Cases: TC790 - Create account on TFChain
  Scenario:
      - The user can create an account on TFChain using Polkadot extension.
"""

def test_create_account(browser):

  dashboard_page = DashboardPage(browser)
  polka_page = PolkaPage(browser)

  User = GenerateString()
  Pass = GenerateString()

  dashboard_page.load()
  polka_page.Authenticate()
  polka_page.AddAccount(User, Pass)
 