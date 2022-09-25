from utils.utils import generate_string,get_seed
from pages.polka import PolkaPage
from pages.dedicate import DedicatePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

#  Time required for the run (12 cases) is approximately 3 minutes.

"""
  Test Case: TC1138 - Navigate to dedicate node
  Steps:
      - Navigate to the dashboard.
      - Select an account.
      - Click on Dedicate Node from side menu.
  Result: User should be navigated to Dedicate Node page.
"""
def test_dedicate_page(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert 'Dedicated Nodes' in browser.page_source


"""
  Test Case: TC997 - Verify the search functionality by valid location or node id
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - In the Farms search bar enter the location or the id of the node
  Test Data: [ ID - Location - case sensitive Location ]
  Result: The search results should be displayed correctly according to the keywords used.
"""
def test_search_by_valid_name_address(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  ids = dedicate_page.get_node_id()
  locations = dedicate_page.get_node_location()
  for i in range (len(ids)):
    dedicate_page.search_nodes(ids[i])
    assert  len(browser.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr')) == 1
  for i in range (len(locations)):
    dedicate_page.search_nodes(locations[i])
    assert  len(browser.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr')) >= 1
    dedicate_page.search_nodes(locations[i].lower())
    assert  len(browser.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr')) >= 1
    dedicate_page.search_nodes(locations[i].upper())
    assert  len(browser.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr')) >= 1


"""
  Test Case: TC1133 - Verify the search functionality by invalid location or node id
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - In the Farms search bar enter invalid location or the id of the node
  Result: The search results should be displayed nothing as search keywords are incorrect.
"""
def test_search_by_invalid_name_address(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  dedicate_page.search_nodes(generate_string())
  assert 'No data available' in browser.page_source


"""
  Test Case: TC998 - Node table sorting by id
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node Id 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the id.
"""
def test_sort_node_id(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert dedicate_page.sort_node_id() == sorted(dedicate_page.get_node_id(), reverse=False) 
  assert dedicate_page.sort_node_id() == sorted(dedicate_page.get_node_id(), reverse=True)


"""
  Test Case: TC998 - Node table sorting by location
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node location 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the location.
"""
def test_sort_node_location(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert dedicate_page.sort_node_location() == sorted(dedicate_page.get_node_location(), reverse=False) 
  assert dedicate_page.sort_node_location() == sorted(dedicate_page.get_node_location(), reverse=True)


"""
  Test Case: TC998 - Node table sorting by CRU
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node CRU 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the CRU.
"""
def test_sort_node_cru(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert dedicate_page.sort_node_cru() == sorted(dedicate_page.get_node_cru(), reverse=False) 
  assert dedicate_page.sort_node_cru() == sorted(dedicate_page.get_node_cru(), reverse=True)


"""
  Test Case: TC998 - Node table sorting by HRU
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node HRU 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the HRU.
"""
def test_sort_node_hru(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert dedicate_page.sort_node_hru() == sorted(dedicate_page.get_node_hru(), reverse=False) 
  assert dedicate_page.sort_node_hru() == sorted(dedicate_page.get_node_hru(), reverse=True)


"""
  Test Case: TC998 - Node table sorting by MRU
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node MRU 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the MRU.
"""
def test_sort_node_mru(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert dedicate_page.sort_node_mru() == sorted(dedicate_page.get_node_mru(), reverse=False) 
  assert dedicate_page.sort_node_mru() == sorted(dedicate_page.get_node_mru(), reverse=True)


"""
  Test Case: TC998 - Node table sorting by SRU
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node SRU 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the SRU.
"""
def test_sort_node_sru(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  assert dedicate_page.sort_node_sru() == sorted(dedicate_page.get_node_sru(), reverse=False) 
  assert dedicate_page.sort_node_sru() == sorted(dedicate_page.get_node_sru(), reverse=True)


"""
  Test Case: TC998 - Node table sorting by Price
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on the arrow behind node Price 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to the Price.
"""
def test_sort_node_price(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  price = dedicate_page.get_node_price()
  assert dedicate_page.sort_node_price() == sorted(price, reverse=False) 
  assert dedicate_page.sort_node_price() == sorted(price, reverse=True)


"""
  Test Case: TC1139 - Node details
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click on expand button on a node
  Result: You should see the node details.
"""
def test_node_details(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  nodes = dedicate_page.node_details()
  for i in range(len(nodes)):
    assert str(dedicate_page.get_node_cru()[i]) in nodes[i][1]
    assert str(dedicate_page.get_node_hru()[i]/1024)[0] in nodes[i][2]
    assert str(dedicate_page.get_node_sru()[i]) in nodes[i][3]
    assert str(dedicate_page.get_node_mru()[i]) in nodes[i][4]
    assert dedicate_page.get_node_location()[i] in nodes[i][5]
    assert dedicate_page.get_node_city()[i] in nodes[i][6]
    assert str(dedicate_page.get_farm_ips(nodes[i][0])) in nodes[i][7]


"""
  Test Case: TC1137 - Reserve a node
  Steps:
      - From the Twin Details Page Click on Dedicated nodes
      - Click reserve button on a node not taken
      - Authenticate polka with password
      - Click unreserve button on same node
  Result: You should see the node details.
"""
def test_reserve_node(browser):
  dedicate_page = DedicatePage(browser)
  polka_page = PolkaPage(browser)
  user = generate_string()
  password = generate_string()
  dedicate_page.load()
  polka_page.authenticate()
  polka_page.import_account(get_seed(),user,password)
  dedicate_page.navigate(user)
  if(dedicate_page.check_avail_dedicate()):
    id = dedicate_page.reserve_node()
    assert dedicate_page.get_dedicate_status(id) == False
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Transaction succeeded: Node "+ str(id) +" reserved')]")))
    status = 0
    while(status==0):
      status = dedicate_page.get_dedicate_status(id)
    assert dedicate_page.get_dedicate_status(id) == dedicate_page.twin_id
    dedicate_page.unreserve_node()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Transaction succeeded: Node "+ str(id) +" Unreserved')]")))
    while(status!=0):
      status = dedicate_page.get_dedicate_status(id)
    assert dedicate_page.get_dedicate_status(id) == False
  else:
    pytest.skip("Can't test as there isn't a free dedicated node.")