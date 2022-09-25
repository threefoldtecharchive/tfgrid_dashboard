import math
import requests
from utils.base import Base
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

    def __init__(self, browser):
        self.browser = browser
        r = requests.post('https://gridproxy.dev.grid.tf/nodes?rentable=true&status=up')
        self.node_list = r.json()
        r = requests.post('https://gridproxy.dev.grid.tf/nodes?rented=true&status=up')
        self.node_list.extend(r.json())
    
    def load(self):
        self.browser.get(Base.base_url)
      
    def navigate(self, user):
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Connected Accounts')]")))
        self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
        self.twin_id = int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[1]').text[4:])
        self.browser.find_element(*self.dedicate_node).click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]/button')))
    
    def search_nodes(self, node):
        self.browser.find_element(*self.search_bar).send_keys(Keys.CONTROL + "a")
        self.browser.find_element(*self.search_bar).send_keys(Keys.DELETE)
        self.browser.find_element(*self.search_bar).send_keys(node)
    
    def get_node_id(self):
        ids = []
        for i in range(len(self.node_list)):
            ids.append(self.node_list[i]['nodeId']) 
        return ids

    def get_node_location(self):
        locations = []
        for i in range(len(self.node_list)):
            locations.append(self.node_list[i]['country'])
        return locations
    
    def get_node_city(self):
        city = []
        for i in range(len(self.node_list)):
            city.append(self.node_list[i]['city'])
        return city
    
    def get_node_cru(self):
        cru = []
        for i in range(len(self.node_list)):
            cru.append(self.node_list[i]['total_resources']['cru'])
        return cru

    def get_node_hru(self):
        hru = []
        for i in range(len(self.node_list)):
            hru.append(math.ceil(self.node_list[i]['total_resources']['hru']/1073741824))
        return hru

    def get_node_mru(self):
        mru = []
        for i in range(len(self.node_list)):
            mru.append(math.ceil(self.node_list[i]['total_resources']['mru']/1073741824))
        return mru

    def get_node_sru(self):
        sru = []
        for i in range(len(self.node_list)):
            sru.append(math.ceil(self.node_list[i]['total_resources']['sru']/1073741824))
        return sru

    def get_node_price(self):
        price = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            price.append(str(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[8]').text))
        return price

    def get_farm_ips(self, node_id):
        for i in range(len(self.node_list)):
            if self.node_list[i]['nodeId'] == node_id:
                farm_id = str(self.node_list[i]['farmId'])
        r = requests.post('https://gridproxy.dev.grid.tf/farms?farm_id='+ farm_id)
        farm_list = r.json()
        return len(farm_list[0]['publicIps'])
    
    def get_dedicate_status(self, node_id):
        r = requests.post('https://gridproxy.dev.grid.tf/nodes/'+ str(node_id))
        dedicate_status = r.json()
        return (dedicate_status['rentedByTwinId'])
    
    def sort_node_id(self):
        self.browser.find_element(*self.node_id).click()
        node_id = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            node_id.append(int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[2]').text))
        return node_id

    def sort_node_location(self):
        self.browser.find_element(*self.location).click()
        locations = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            locations.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[3]').text)
        return locations

    def sort_node_cru(self):
        self.browser.find_element(*self.cru).click()
        cru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            cru.append(int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[4]').text))
        return cru

    def sort_node_hru(self):
        self.browser.find_element(*self.hru).click()
        hru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            hru.append(int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[5]').text))
        return hru

    def sort_node_mru(self):
        self.browser.find_element(*self.mru).click()
        mru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            mru.append(int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[6]').text))
        return mru

    def sort_node_sru(self):
        self.browser.find_element(*self.sru).click()
        sru = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            sru.append(int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[7]').text))
        return sru

    def sort_node_price(self):
        self.browser.find_element(*self.price).click()
        price = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            price.append(str(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[8]').text))
        return price
    
    def node_details(self):
        self.browser.find_element(*self.node_id).click()
        nodes = []
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            details = []
            self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[1]/button').click()
            details.append(int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[2]').text))
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[1]/div/div[2]/div/div/div[1]').text)
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[1]/div/div[2]/div/div/div[2]').text)
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[1]/div/div[2]/div/div/div[3]').text)
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[1]/div/div[2]/div/div/div[4]').text)
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[2]/div/div[2]/div/div/div[1]').text)
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[2]/div/div[2]/div/div/div[2]').text)
            details.append(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i+1) +']/td/div/div[3]/div/div[2]/div/div/div').text)
            self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[1]/button').click()
            nodes.append(details)
        return nodes

    def check_avail_dedicate(self):
        if ( len(self.browser.find_elements(By.XPATH, "//*[contains(text(), 'Taken')]")) != len(self.node_list) ):
            return True
        return False

    def reserve_node(self):
        for i in range(1, len(self.browser.find_elements(*self.node_table))+1):
            if ((self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[9]/div/button').text) == 'Reserve'):
                self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[9]/div/button').click()
                return (int(self.browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div[1]/table/tbody/tr['+ str(i) +']/td[2]').text))

    def unreserve_node(self):
        self.browser.find_element(By.XPATH, "//*[contains(text(), 'Unreserve')]").click()
        WebDriverWait(self.browser, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[contains(text(), 'Are you sure you want to unreserve this dedicated node?')]")))
        self.browser.find_element(By.XPATH, "//*[@id='app']/div[4]/div/div/div[3]/button[1]").click()