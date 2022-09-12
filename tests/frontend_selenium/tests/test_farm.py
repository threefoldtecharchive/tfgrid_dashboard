from utils.utils import generate_gateway, generate_inavalid_gateway, generate_inavalid_ip, generate_string, generate_ip
import pytest
from pages.farm import FarmPage
from pages.polka import PolkaPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
TC907-Create farm with valid name
The user can create a farm.

Test steps
From the Twin Details Page Click on Farms.
In the Farms page Click on "Create Farm" button.
Enter the Farm Name.
Click on Submit.
Authenticate polkadot transaction.

"""
def test_create_farm(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.create_farm(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm created!')]" )))      
    assert browser.find_element(By.XPATH,"//*[contains(text(), 'Farm created!')]")

"""
TC911-Create farm with existing name

Test steps
From the Twin Details Page Click on Farms.
In the Farms page Click on " Create Farm ".
Enter the Farm Name.
Click on Submit.
Authenticate polkadot transactions.
Try to recreate a Farm with same name on the third step
Authenticate polkadot transactions.
"""

def test_create_farm_with_existing_name(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.create_farm_with_existing_name()
    polka_page.authenticate_with_pass(password)

    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Farm creation failed!')]" )))      
    assert browser.find_element(By.XPATH,"//*[contains(text(), 'Farm creation failed!')]")
 
"""
TC908-Verify the search functionality
Test steps
From the Twin Details Page Click on Farms
In the Farms page Click on the "Create Farm" button.
Enter the Farm Name.
Click on Submit.
Authenticate polkadot transaction.
In the Farms search bar enter the name or the id of the farm you just created
Test Data: [ use the whole name of the farm, only the first part, the second part ]
"""
def test_verify_search_functionality(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.verify_search_functionality(password)

"""
 TC909-Enter un-existing id or name of the farm and you should see the details of this farm

Test steps
From the Twin Details Page Click on Farms
On the Farms page Click on the "Create Farm" button.
Enter the Farm Name.
Click on Submit.
Authenticate polkadot transaction.
In the Farms search bar try to enter a different name or id of the farm you just created.
"""
def test_search_for_unexisting_farm(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    table=farm_page.search_for_unexisting_farm(password)   
    assert 'No data available' in table
"""
TC910-Farm Table Sorting

Test steps
From the Twin Details Page Click on Farms
Make sure to have at least 2 Farms , If you don't create them
Click on the arrow behind farm Id 'once up and once down and once to remove the sorting'
Click on the arrow behind the farm Name 'once up and once down and once to remove the sorting'
Click on the arrow behind the Linked twin id 'once up and once down and once to remove the sorting'
Click on the arrow behind the Certification type 'once up and once down and once to remove the sorting'
Click on the arrow behind the pricing policy id 'once up and once down and once to remove the sorting'
"""
def test_farm_table_sorting_by_id(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    id,sorted,rows=farm_page.farm_table_sorting_by_id()
    assert id==sorted
    id_up,sorted_up=farm_page.farm_table_sorting_by_id_up(id,rows)
    assert id_up==sorted_up
    

def test_farm_table_sorting_by_name(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    name,sorted,table=farm_page.farm_table_sorting_by_name()
    assert name== sorted
    name_up,sorted_up=farm_page.farm_sorting_name_up(name,table)
    assert name_up== sorted_up



def test_farm_table_sorting_by_twin_id(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    id,sorted,table =farm_page.farm_table_sorting_by_twin_id()
    assert id==sorted
    id_up,sorted_up =farm_page.farm_table_sorting_by_twin_id_up(id,table)
    assert id_up==sorted_up



def test_farm_table_sorting_by_cerification_type(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    name ,sorted,table=farm_page.farm_table_sorting_by_cerification_type()
    assert name==sorted
    name_up,sorted_up=farm_page.farm_table_sorting_by_cerification_type_up(name,table)
    assert name_up==sorted_up


def test_farm_table_sorting_by_pp_id(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    id,sorted,table=farm_page.farm_table_sorting_by_pp_id()
    assert id==sorted
    id_up,sorted_up =farm_page.farm_table_sorting_by_pp_id_up(id,table)
    assert id_up==sorted_up

"""
TC917-add IP to Farm

Test steps
From the Twin Details Page Click on Farms.
Make sure you have at least one farm.
Click on the arrow behind any farm id.
Click on Public IPs.
Click on add IP button.
Add ip and Gateway.
Click on the save button.
Authenticate polkadot transaction.
"""
def test_add_ip(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.add_ip()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IP created!')]" )))      
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'IP created!')]") 
    


@pytest.mark.parametrize('cases', [generate_ip(), '1.0.0.1/32',  '1.0.0.0/16'])
def test_valid_ip(browser,cases):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.add_valid_ip(cases)
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'IP address in CIDR format xxx.xxx.xxx.xxx/xx')]") 

"""
TC919-Enter Invalid IP and Getaway

Test steps
From the Twin Details Page Click on Farms
Make sure you have at least one farm.
Click on the arrow behind any farm id
Click on Public IPs
Click on add IP button
Add IP , Getaway
"""
@pytest.mark.parametrize('cases', ['',generate_inavalid_ip()])
def test_invalid_ip(browser,cases):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    element=farm_page.add_invalid_ip(cases)  
    assert element.is_enabled()==False  

@pytest.mark.parametrize('cases', [ generate_gateway()])
def test_valid_gateway(browser,cases):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.add_valid_gateawy(cases) 
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Gateway for the IP in ipv4 format')]") 

"""
TC920-Enter Invalid Gateway

Test steps
From the Twin Details Page Click on Farms
Make sure you have at least one farm.
Click on the arrow behind any farm id
Click on Public IPs
Click on add IP button
Add IP and Getaway
"""

@pytest.mark.parametrize('cases', [ generate_inavalid_gateway()])
def test_invalid_gateway(browser,cases):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    element =farm_page.add_invalid_gateway(cases) 
    #assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Gateway is not formatted correctly')]") 
    assert element.is_enabled()==False   

"""
TC918 -Delete IP address from farm

Test steps
From the Twin Details Page Click on Farms.
Make sure you have at least one farm.
Click on the arrow behind any fram id
Click on Public IPs.
Click on the Delete IP button.
Authenticate polkadot transaction.
"""
def test_delete_ip(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.delete_ip()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'IP deleted!')]" )))      

    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'IP deleted!')]") 

"""
TC-915Add farm payout address

Test steps
From the Twin Details Page Click on Farms
Make sure you have at least one farm.
Click on the arrow behind any farm id
Click on add v2 address button
Put the address
Click Submit
"""
def test_add_farmpayout_address(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.add_farmpayout_address()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Address added!')]" )))      
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Address added!')]") 
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Edit')]") 
"""
TC916-Edit farm payout address

Test steps
From the Twin Details Page Click on Farms
Make sure you have at least one farm.
Click on the arrow behind ant farm id
Click on the edit v2 address button
Put the address you got
Click Submit
"""
def test_edit_farmpayout_address(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    farm_page.edit_farmpayout_address()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Address added!')]" )))      
    assert browser.find_elements(By.XPATH,"//*[contains(text(), 'Address added!')]") 

"""
TC921-Verify the availability of zero os bootstrap
Test steps
From the Twin Details Page Click on Farms
Make sure that you have at least on farm
Click on the arrow behind the farm id
Click on View Bootstrap
"""
def test_verify_the_availability_of_zero_os_bootstrap(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    seed = 'grid useful zebra snack feel illness vacant journey amateur master admit nose'
    user = generate_string()
    password = generate_string()
    farm_page.load()
    polka_page.authenticate()
    polka_page.import_account(seed, user, password)
    farm_page.navigetor()
    link=farm_page.verify_the_availability_of_zero_os_bootstrap()
    assert link=="https://v3.bootstrap.grid.tf/"



  