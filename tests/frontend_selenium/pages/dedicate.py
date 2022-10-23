import math
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This module contains Dedicate Node page elements.
"""

class DedicatePage:

    dedicate_node = (By.XPATH , "//*[contains(text(), 'dedicated nodes')]")
    node_id = (By.XPATH , "//*[contains(text(), 'Node ID')]")
    location = (By.XPATH , "//*[contains(text(), 'Location')]")
    cru = (By.XPATH , "//*[contains(text(), 'CRU')]")
    hru = (By.XPATH , "//*[contains(text(), 'HRU (GB)')]")
    mru = (By.XPATH , "//*[contains(text(), 'MRU (GB)')]")
    sru = (By.XPATH , "//*[contains(text(), 'SRU (GB)')]")
    price = (By.XPATH , "//*[contains(text(), 'Price (USD)')]")
    search_bar = (By.XPATH ,'/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div[1]/div/input')
    node_table = (By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr')
    twin_address = (By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]')
    expand_node_buttom = (By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/button')
    reservation_button = (By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr/td[9]/div/button')
    ok_btn = (By.XPATH, "//*[@id='app']/div[4]/div/div/div[3]/button[1]")
    table_xpath = '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr'

    def __init__(self, browser):
        self.browser = browser
      
    def navigate(self, user):
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.twin_id = int(self.browser.find_element(*self.twin_address).text[4:])
        self.browser.find_element(*self.dedicate_node).click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.expand_node_buttom))
    
    def search_nodes(self, node):
        self.browser.find_element(*self.search_bar).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.search_bar).send_keys(Keys.DELETE)
        self.browser.find_element(*self.search_bar).send_keys(node)
    
    def get_node_id(self, node_list):
        ids = []
        for i in range(len(node_list)):
            ids.append(node_list[i]['nodeId']) 
        return ids

    def get_node_location(self, node_list):
        locations = []
        for i in range(len(node_list)):
            locations.append(node_list[i]['country'])
        return locations
    
    def get_node_city(self, node_list):
        city = []
        for i in range(len(node_list)):
            city.append(node_list[i]['city'])
        return city
    
    def get_node_cru(self, node_list):
        cru = []
        for i in range(len(node_list)):
            cru.append(node_list[i]['total_resources']['cru'])
        return cru

    def get_node_hru(self, bool, node_list):
        hru = []
        for i in range(len(node_list)):
            node_hru = math.ceil(node_list[i]['total_resources']['hru']/(1024 ** 3))
            if(bool and node_hru >= 1024):
                node_hru = math.floor(node_hru/1024)
            hru.append(node_hru)
        return hru

    def get_node_mru(self, bool, node_list):
        mru = []
        for i in range(len(node_list)):
            node_mru = math.ceil(node_list[i]['total_resources']['mru']/(1024 ** 3))
            if(bool and node_mru >= 1024):
                node_mru = math.floor(node_mru/1024)
            mru.append(node_mru)
        return mru

    def get_node_sru(self, bool, node_list):
        sru = []
        for i in range(len(node_list)):
            node_sru = math.ceil(node_list[i]['total_resources']['sru']/(1024 ** 3))
            if(bool and node_sru >= 1024):
                node_sru = math.floor(node_sru/1024)
            sru.append(node_sru)
        return sru

    def get_node_price(self):
        price = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            price.append(str(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[8]").text))
        return price

    def get_farm_id(self, node_id, node_list):
        for i in range(len(node_list)):
            if node_list[i]['nodeId'] == node_id:
                farm_id = str(node_list[i]['farmId'])
        return farm_id
    
    def get_node_count(self):
        return len(self.browser.find_elements(*self.node_table))
    
    def sort_node_id(self):
        self.browser.find_element(*self.node_id).click()
        node_id = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            node_id.append(int(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[2]").text))
        return node_id

    def sort_node_location(self):
        self.browser.find_element(*self.location).click()
        locations = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            locations.append(str(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[3]").text))
        return locations

    def sort_node_cru(self):
        self.browser.find_element(*self.cru).click()
        cru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            cru.append(int(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[4]").text))
        return cru

    def sort_node_hru(self):
        self.browser.find_element(*self.hru).click()
        hru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            hru.append(int(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[5]").text))
        return hru

    def sort_node_mru(self):
        self.browser.find_element(*self.mru).click()
        mru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            mru.append(int(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[6]").text))
        return mru

    def sort_node_sru(self):
        self.browser.find_element(*self.sru).click()
        sru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            sru.append(int(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[7]").text))
        return sru

    def sort_node_price(self):
        self.browser.find_element(*self.price).click()
        price = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            price.append(str(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[8]").text))
        return price
    
    def node_details(self):
        self.browser.find_element(*self.node_id).click()
        nodes = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            details = []
            self.browser.find_element(By.XPATH, self.table_xpath+ '['+ str(i) +']/td[1]/button').click()
            details.append(int(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[2]").text)) # Node ID
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[1]/div/div[2]/div/div/div[1]").text) # CPU Resource Unit
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[1]/div/div[2]/div/div/div[2]").text) # Disk Resource Unit (HDD)
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[1]/div/div[2]/div/div/div[3]").text) # Disk Resource Unit (SSD)
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[1]/div/div[2]/div/div/div[4]").text) # Memory Resource Unit
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[2]/div/div[2]/div/div/div[1]").text) # Country
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[2]/div/div[2]/div/div/div[2]").text) # City
            details.append(self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i+1)}]/td/div/div[3]/div/div[2]/div/div/div").text) # Farm Public Ips
            self.browser.find_element(By.XPATH, f"{self.table_xpath}[{str(i)}]/td[1]/button").click()
            nodes.append(details)
        return nodes

    def check_free_node(self, node_list):
        for node in node_list:
            if (node['rentedByTwinId'] == 0):
                return node['nodeId']
        return 0

    def reserve_node(self, id):
        self.search_nodes(id)
        if ((self.browser.find_element(*self.reservation_button).text) == 'Reserve'):
            self.browser.find_element(*self.reservation_button).click()

    def unreserve_node(self, id):
        self.search_nodes(id)
        if ((self.browser.find_element(*self.reservation_button).text) == 'Unreserve'):
            self.browser.find_element(*self.reservation_button).click()
            WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Are you sure you want to unreserve this dedicated node?')]")))
            self.browser.find_element(*self.ok_btn).click()

    def wait_for(self, keyword):
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '"+ keyword +"')]")))
        return True