from utils.utils import generate_string, get_seed
from pages.farm import FarmPage
from pages.polka import PolkaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Time required for the run (17 cases) is approximately 13 minutes.

"""
  Test Case: TC907-Create farm with valid name
  Steps:
      - From the Twin Details Page Click on Farms.
      - In the Farms page Click on "Create Farm" button.
      - Enter the Farm Name.
      - Click on Submit.
      - Authenticate polkadot transaction.
  Result: The user can create a farm.
"""
def test_create_farm(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")


"""
  Test Case: TC911-Create farm with existing name
  Steps:
      - From the Twin Details Page Click on Farms.
      - In the Farms page Click on " Create Farm ".
      - Enter the Farm Name.
      - Click on Submit.
      - Authenticate polkadot transactions.
      - Try to recreate a Farm with same name on the third step
      - Authenticate polkadot transactions.
   Result: You should see the bottom right alert with the message "farm creation failed".
"""
def test_create_farm_with_existing_name(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    farm_page.create_farm_with_existing_name(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm creation failed!')]" )))      
    assert browser.find_element(By.XPATH,"//*[contains(text(), 'Farm creation failed!')]")


"""
  Test Case: TC912 - create a farm with invalid name
  Steps:
      - From the Twin Details Page Click on Farms.
      - In the Farms page Click on " Create Farm ".
      - Enter the Farm Name.
      - Click on Submit.
      - Authenticate polkadot transactions.
   Test Data: [Empty Field, More than 40 char, Spaces, Special chr(@,#%^&*(_+-))]
   Result: You should display a warning message 'Name is not formatted correctly (All letters + numbers and (-,_) are allowed).
"""
def test_create_farm_invalid_name(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm_invalid_name()


"""
  Test Case: TC908-Verify the search functionality
  Steps:
      - From the Twin Details Page Click on Farms
      - In the Farms page Click on the "Create Farm" button.
      - Enter the Farm Name.
      - Click on Submit.
      - Authenticate polkadot transaction.
      - In the Farms search bar enter the name or the id of the farm you just created
   Test Data: [ use the whole name of the farm, only the first part, the second part ]
   Result: The search results should be displayed correctly according to the keywords used.
"""
def test_verify_search_functionality(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    farm_page.verify_search_functionality(farm_name)


"""
  Test Case: TC909 - Search for un-existing farm
  Steps:
      - From the Twin Details Page Click on Farms
      - On the Farms page Click on the "Create Farm" button.
      - Enter the Farm Name.
      - Click on Submit.
      - Authenticate polkadot transaction.
      - In the Farms search bar try to enter a different name or id of the farm you just created.
  Result: You should see "No data available " on the table of farms
"""
def test_search_for_unexisting_farm(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    table=farm_page.search_for_unexisting_farm()   
    assert 'No data available' in table


"""
  Test Case: TC910 - Farm Node table sorting
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure to have at least 2 Farms , If you don't create them
      - Click on the arrow behind farm Id 'once up and once down and once to remove the sorting'
      - Click on the arrow behind the farm Name 'once up and once down and once to remove the sorting'
      - Click on the arrow behind the Linked twin id 'once up and once down and once to remove the sorting'
      - Click on the arrow behind the Certification type 'once up and once down and once to remove the sorting'
      - Click on the arrow behind the pricing policy id 'once up and once down and once to remove the sorting'
  Result: You should see the sorting of the table change according to each case
"""
def test_farm_table_sorting(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    #sort by ID
    id,sorted,rows = farm_page.farm_table_sorting_by_id()
    assert id == sorted
    id_up,sorted_up = farm_page.farm_table_sorting_by_id_up(id,rows)
    assert id_up == sorted_up
    #sort by Name
    name,sorted,table = farm_page.farm_table_sorting_by_name()
    assert name == sorted
    name_up,sorted_up = farm_page.farm_sorting_name_up(name,table)
    assert name_up == sorted_up
    #sort by Twin ID
    id,sorted,table = farm_page.farm_table_sorting_by_twin_id()
    assert id == sorted
    id_up,sorted_up = farm_page.farm_table_sorting_by_twin_id_up(id,table)
    assert id_up == sorted_up
    #sort by Cerification Type
    name ,sorted,table = farm_page.farm_table_sorting_by_cerification_type()
    assert name == sorted
    name_up,sorted_up = farm_page.farm_table_sorting_by_cerification_type_up(name,table)
    assert name_up == sorted_up
    #sort by Pricing Policy ID
    id,sorted,table = farm_page.farm_table_sorting_by_pp_id()
    assert id == sorted
    id_up,sorted_up = farm_page.farm_table_sorting_by_pp_id_up(id,table)
    assert id_up == sorted_up


"""
  Test Case: TC915 - Add farm payout address
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id
      - Click on add v2 address button
      - Put the address
      - Click Submit
  Result: You should see the bottom right alert with the message "address added"
"""
def test_add_farmpayout_address(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    farm_page.add_farmpayout_address()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Address added!')]" )))
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Edit')]") 


"""
  Test Case: TC1140 - Add invalid farm payout address
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id
      - Click on add v2 address button
      - Put the address
      - Click Submit
  Result: You should see alert with the message "invalid address"
"""
def test_add_invalid_farmpayout_address(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    assert farm_page.add_invalid_farmpayout_address().is_enabled()==False


"""
  Test Case: TC916 - Edit farm payout address
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure you have at least one farm.
      - Click on the arrow behind ant farm id
      - Click on the edit v2 address button
      - Put the address you got
      - Click Submit
  Result: You should see the bottom right alert with the message "address added"
"""
def test_edit_farmpayout_address(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    farm_page.edit_farmpayout_address()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Address added!')]" )))      
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Address added!')]") 


"""
  Test Case: TC1141 - Enter valid IP
  Steps:
      - From the Twin Details Page Click on Farms.
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id.
      - Click on Public IPs.
      - Click on add IP button.
      - Add ip and Gateway.
  Test Data for IP: [ should be numbers separated by '.' and end with '/' port ex: 127.0.0.01/16]
  Result: You should see the bottom right alert with the message "IP Created!"
"""
def test_valid_ip(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    assert farm_page.add_valid_ip().is_enabled()==True


"""
  Test Case: TC919 - Enter Invalid IP
  Steps:
      - From the Twin Details Page Click on Farms.
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id.
      - Click on Public IPs.
      - Click on add IP button.
      - Add ip and Gateway.
  Test Data for IP: [ should be numbers separated by '.' and end with '/' port ex: 127.0.0.01/16]
  Result: You should see the bottom right alert with the message "incorrect format".
"""
def test_invalid_ip(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    assert farm_page.add_invalid_ip().is_enabled()==False


"""
  Test Case: TC1142 - Enter valid Gateway
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id
      - Click on Public IPs
      - Click on add IP button
      - Add IP and Getaway
  Test Data for Gateway: [ should be numbers separated by '.' ex: 127.0.0.01/16]
  Result: No alert displayed and button is enabled.
"""
def test_valid_gateway(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    assert farm_page.add_valid_gateawy().is_enabled()==True


"""
  Test Case: TC920 - Enter Invalid Gateway
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id
      - Click on Public IPs
      - Click on add IP button
      - Add IP and Getaway
  Test Data: [Empty Field,All letters, (-,_),54.54,....1270001,127.0.0..1]
  Result: You should see the bottom right alert with the message "Gateway is not formatted correctly".
"""
def test_invalid_gateway(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)   
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    assert farm_page.add_invalid_gateway().is_enabled()==False

"""
  Test Case: TC917 - add IP to Farm
  Steps:
      - From the Twin Details Page Click on Farms.
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id.
      - Click on Public IPs.
      - Click on add IP button.
      - Add ip and Gateway.
      - Click on the save button.
      - Authenticate polkadot transaction.
  Result: You should see the bottom right alert with the message "IP Created!"
"""
def test_add_ip(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    farm_page.add_ip()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IP created!')]" )))      
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'IP created!')]") 


"""
  Test Case: TC918 - Delete IP address from farm
  Steps:
      - From the Twin Details Page Click on Farms.
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id.
      - Click on Public IPs.
      - Click on the Delete IP button.
      - Authenticate polkadot transaction.
  Result: You should see the bottom right alert with the message "IP deleted!"
"""
def test_delete_ip(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    farm_page.add_ip()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IP created!')]" )))      
    farm_page.delete_ip()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IP deleted!')]" )))
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'IP deleted!')]") 


"""
  Test Case: TC914 - Farm Details
  Steps:
      - From the Twin Details Page Click on Farms
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id
  Result: You should see Farm id, Farm Name, Linked Twin Id, Certification Type, 
            Linked Pricing policy Id, stellar payout address, Bootstrap Image, Public IPs.
"""
def test_farm_details(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    farm_page.add_farmpayout_address()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Address added!')]" )))
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Edit')]") 
    browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[1]/button').click()
    farm_page.add_ip()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IP created!')]" )))
    farm_details = farm_page.farm_detials()
    print (farm_details)
    grid_farm_details = farm_page.get_farm_details(farm_details[1])
    print (grid_farm_details)
    assert grid_farm_details[0]['farmId'] == int(farm_details[0])
    assert grid_farm_details[0]['name'] == farm_details[1]
    assert grid_farm_details[0]['twinId'] == int(farm_details[2])
    assert grid_farm_details[0]['certificationType'] == farm_details[3]
    assert grid_farm_details[0]['pricingPolicyId'] == int(farm_details[4])
    assert grid_farm_details[0]['stellarAddress'] == farm_details[5]
    for i in range(len(grid_farm_details[0]['publicIps'])):
        assert grid_farm_details[0]['publicIps'][i]['ip'] == farm_details[6+(i*3)]
        assert grid_farm_details[0]['publicIps'][i]['contractId'] == int(farm_details[7+(i*3)])
        assert grid_farm_details[0]['publicIps'][i]['gateway'] == farm_details[8+(i*3)]

"""
  Test Case: TC921 - Verify the availability of zero os bootstrap
  Steps:
      - From the Twin Details Page Click on Farms.
      - Make sure you have at least one farm.
      - Click on the arrow behind any farm id.
      - Click on View Bootstrap
  Result: You should see Zero-OS bootstrap page is opened     
"""
def test_verify_the_availability_of_zero_os_bootstrap(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))
    assert browser.find_element(By.XPATH,"//*[contains(text(), '"+ farm_name +"')]")
    assert farm_page.verify_the_availability_of_zero_os_bootstrap() == "https://v3.bootstrap.grid.tf/"