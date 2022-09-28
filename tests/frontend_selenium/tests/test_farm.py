from utils.utils import generate_gateway, generate_inavalid_gateway, generate_inavalid_ip, generate_ip, generate_string, get_seed
from pages.farm import FarmPage
from pages.polka import PolkaPage
from pages.grid_proxy import GridProxy

#  Time required for the run (17 cases) is approximately 13 minutes.

def before_test_setup(browser):
    polka_page = PolkaPage(browser)
    farm_page=FarmPage(browser)
    user = generate_string()
    password = generate_string()
    farm_name=generate_string()
    polka_page.load_and_authenticate()
    polka_page.import_account(get_seed(), user, password)
    farm_page.navigetor(user)
    return farm_page, polka_page, farm_name, password

def test_create_farm(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)


def test_create_farm_with_existing_name(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm creation failed!')


def test_create_farm_invalid_name(browser):
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
    farm_page, _, _, _ = before_test_setup(browser)
    browser.find_element(*farm_page.create_button).click()
    cases = ['f', 'DD', '4', '88', '-', '_-']
    for case in cases:
        farm_page.create_farm_invalid_name(case)
        assert farm_page.wait_for('Name should be more than or equal 3 characters')
    cases = [' ', 'f f', 'ddd#', 'ddd@', '88!', 'gg$', 'aa%', 'bb^', 'cc&', 'h8*', 's5()', '|~</;:']
    for case in cases:
        farm_page.create_farm_invalid_name(case)
        assert farm_page.wait_for('Name is not formatted correctly (All letters + numbers and (-,_) are allowed')
    farm_page.create_farm_invalid_name(generate_string()+generate_string()+'_'+generate_string()+generate_string())
    assert farm_page.wait_for('Name too long, only 40 characters permitted')


def test_verify_search_functionality(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_name in farm_page.search_functionality(farm_name) 
    assert farm_name in farm_page.search_functionality(farm_name[:len(farm_name)//2]) 
    assert farm_name in farm_page.search_functionality(farm_name[len(farm_name)//2:])
    

def test_search_for_unexisting_farm(browser):
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
    farm_page, _, _, _ = before_test_setup(browser)
    table=farm_page.search_functionality(generate_string())
    assert 'No data available' in table


def test_farm_table_sorting(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
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


def test_add_farmpayout_address(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    case = "GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG"
    farm_page.setup_farmpayout_address()
    farm_page.add_farmpayout_address(case).click()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Address added!')
    assert farm_page.wait_for('Edit')


def test_add_invalid_farmpayout_address(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.setup_farmpayout_address()
    cases = [' ', 'dgdd',generate_string(), 'gdhjP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6Bcfg']
    for case in cases:
        assert farm_page.add_farmpayout_address(case).is_enabled()==False
        assert farm_page.wait_for('Edit')


def test_edit_farmpayout_address(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    case = "GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG"
    farm_page.setup_farmpayout_address()
    farm_page.add_farmpayout_address(case).click()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Address added!')


def test_valid_ip(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.setup_gateway(generate_gateway())
    cases = ['2.0.0.1/32',  '3.0.0.0/16', '139.255.255.255/17', '59.15.35.78/25']
    for case in cases:
        assert farm_page.add_ip(case).is_enabled()==True
        assert farm_page.wait_for('IP address in CIDR format xxx.xxx.xxx.xxx/xx')
    

def test_invalid_ip(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    cases = [generate_inavalid_ip(), '1.0.0.0/66', '239.255.255/17', '239.15.35.78.5/25', '239.15.35.78.5', ' ', '*.#.@.!|+-']
    farm_page.setup_gateway(generate_gateway())
    for case in cases:
        assert farm_page.add_ip(case).is_enabled()==False
        assert farm_page.wait_for('Incorrect format')
    assert farm_page.add_ip('255.0.0.1/32').is_enabled()==False
    assert farm_page.wait_for('IP is not public')


def test_valid_gateway(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.setup_ip(generate_ip())
    cases = [generate_gateway(), '1.0.0.1',  '1.0.0.0', '255.255.255.255', '239.15.35.78', '1.1.1.1']
    for case in cases:
        assert farm_page.add_gateway(case).is_enabled()==True
        assert farm_page.wait_for('Gateway for the IP in ipv4 format')
    

def test_invalid_gateway(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.setup_ip(generate_ip())
    cases = [generate_inavalid_gateway(), '1.0.0.',  '1:1:1:1', '522.255.255.255', '.239.35.78', '1.1.1.1/16', '239.15.35.78.5', ' ', '*.#.@.!|+-']
    for case in cases:
        assert farm_page.add_gateway(case).is_enabled()==False
        assert farm_page.wait_for('Gateway is not formatted correctly')


def test_add_ip(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.setup_ip(generate_ip())
    farm_page.add_gateway(generate_gateway()).click()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('IP created!')


def test_delete_ip(browser):
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
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    farm_page.setup_ip(generate_ip())
    farm_page.add_gateway(generate_gateway()).click()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('IP created!')     
    farm_page.delete_ip()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('IP deleted!')


def test_farm_details(browser):
    """
    Test Case: TC914 - Farm Details
    Steps:
        - From the Twin Details Page Click on Farms
        - Make sure you have at least one farm.
        - Click on the arrow behind any farm id
    Result: You should see Farm id, Farm Name, Linked Twin Id, Certification Type, 
                Linked Pricing policy Id, stellar payout address, Bootstrap Image, Public IPs.
    """
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    grid_proxy = GridProxy(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    case = "GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG"
    farm_page.setup_farmpayout_address()
    farm_page.add_farmpayout_address(case).click()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Address added!')
    browser.find_element(*farm_page.details_arrow).click()
    farm_page.setup_ip(generate_ip())
    farm_page.add_gateway(generate_gateway()).click()
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('IP created!')
    assert farm_page.wait_for('Edit')  
    farm_details = farm_page.farm_detials()
    grid_farm_details = grid_proxy.get_farm_details(farm_details[1])
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


def test_verify_the_availability_of_zero_os_bootstrap(browser):
    """
    Test Case: TC921 - Verify the availability of zero os bootstrap
    Steps:
        - From the Twin Details Page Click on Farms.
        - Make sure you have at least one farm.
        - Click on the arrow behind any farm id.
        - Click on View Bootstrap
    Result: You should see Zero-OS bootstrap page is opened     
    """
    farm_page, polka_page, farm_name, password = before_test_setup(browser)
    farm_page.create_farm(farm_name)
    polka_page.authenticate_with_pass(password)
    assert farm_page.wait_for('Farm created!')
    assert farm_page.wait_for(farm_name)
    assert farm_page.verify_the_availability_of_zero_os_bootstrap() == "https://v3.bootstrap.grid.tf/"