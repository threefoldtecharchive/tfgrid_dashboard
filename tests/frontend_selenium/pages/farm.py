from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
This module contains Farm page elements.
"""

class FarmPage:

    avigate=(By.XPATH,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/i')
    account_choice=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div/div[2]/div[1]/div')
    condition_accept=(By.XPATH,'//*[@id="app"]/div[4]/div/button/span')
    portal=(By.XPATH,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[1]/div[1]/i')
    account=(By.XPATH,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div')
    farm=(By.XPATH, "//*[contains(text(), 'farms')]" )
    title=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3')
    create_button=(By.XPATH, "//*[contains(text(), 'Create farm')]")
    farm_name_text_field=(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[1]/form/div/div/div[1]/div/input')
    farm_name_warning=(By.XPATH,'//*[@id="app"]/div[5]/div/div/div[1]/form/div/div/div[2]/div/div/div')
    submit_farm_button=(By.XPATH, "//*[contains(text(), 'Submit')]") 
    msg1=(By.XPATH,'//*[@id="zV6r5X-VI"]/div')
    created_msg=(By.XPATH,'//*[@id="zV6r5X-VI"]')
    search_bar=(By.XPATH ,'/html/body/div[1]/div[1]/div[3]/div/div/div[3]/div/div[1]/div/input')
    farms_table=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/header/div')
    details_arrow=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[1]/button')
    farm_Id_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/thead/tr/th[2]')
    farm_name_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/thead/tr/th[3]/i')
    farm_twin_linked_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/thead/tr/th[4]/i')
    certification_type_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/thead/tr/th[5]/i')
    pricing_policy_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/thead/tr/th[6]/i')
    add_v2_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[6]/div[2]/div/button')
    ip_v2_textfield=('/html/body/div[1]/div[5]/div/div/div[1]/form/div/div/div[1]/div/input')
    submit_button=(By.XPATH,'//*[@id="app"]/div[5]/div/div/div[2]/button[2]')
    edit_v2_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[6]/div[2]/div/button/span')
    view_bootstrap_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[7]/div[2]/div/a')
    public_ip_list=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/button/div')
    add_ip_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/header/div/div/button/span')
    ip_text_field=(By.XPATH ,'/html/body/div[1]/div[5]/div/div/div[2]/div[2]/div/div[1]/div/input')
    path=(By.XPATH,'/html/body/div[1]/div[5]/div/div/div[1]/form/div/div/div[1]/div/input')
    gateway_text_field=(By.XPATH ,'/html/body/div[1]/div[5]/div/div/div[2]/div[3]/div/div[1]/div/input')
    ip_warning_msg=(By.XPATH ,'//*[@id="app"]/div[7]/div/div/div[2]/div[1]/div/div[2]/div/div/div')
    gateway_warning_msg=(By.XPATH ,'//*[@id="app"]/div[7]/div/div/div[2]/div[2]/div/div[2]/div/div/div')
    save_button=(By.XPATH ,'//*[@id="app"]/div[5]/div/div/div[3]/button[3]')
    delete_ip_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr/td[4]/div/button')
    delete_button=(By.XPATH, "//div[contains(@class, 'v-card__actions')]//button[contains(@class, 'red--text')]")
    zero=(By.XPATH,'//html/body/main/div[1]/div/h1')
    table_farm_name=(By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[3]')
    table = (By.XPATH,'//table/tbody/tr')
    stellar_payout_address = (By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[6]/div[2]/div/div/span')
    farm_loading = (By.XPATH, "//*[contains(text(), 'loading farms')]") 
    table_row = '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr['
    farm_public_ips = '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr'
    node_expan_details = '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div['
  
    def __init__(self, browser):
      self.browser = browser

    def navigetor(self,user):
      self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
      self.browser.find_element(*self.farm).click()

    def create_farm(self, farm_name):
      self.browser.find_element(*self.create_button).click()
      self.browser.find_element(*self.farm_name_text_field).send_keys(farm_name)
      self.browser.find_element(*self.submit_farm_button).click()

    def create_farm_invalid_name(self, data):
      self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.farm_name_text_field).send_keys(data)

    def search_functionality(self, farm_name):
      self.browser.find_element(*self.search_bar).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.search_bar).send_keys(Keys.DELETE)
      self.browser.find_element(*self.search_bar).send_keys(farm_name)
      table = self.browser.find_element(*self.table).text
      while('loading farms' in table):
        table = self.browser.find_element(*self.table).text
      return table

    def farm_table_sorting_by_id(self):
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.table_farm_name))
      id=[]
      table = self.browser.find_elements(*self.table)
      for i in range(1,len(table)+1):
        element=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[2]').text)
        id.append(int(element))
      id.sort()
      self.browser.find_element(*self.farm_Id_arrow).click()
      sorted=[]
      table = self.browser.find_elements(*self.table)
      for i in range (1,len(table)+1):
        index=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[2]').text)
        sorted.append(int(index))
      return id,sorted,table
    
    def farm_table_sorting_by_id_up(self,id,rows):    
      id.reverse()
      sorted=[]
      self.browser.find_element(*self.farm_Id_arrow).click()
      for i in range (1,len(rows)+1):
        index1=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[2]').text)
        sorted.append(int(index1))
      return id,sorted

    def farm_table_sorting_by_name(self):
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.table_farm_name))      
      name=[]
      table = self.browser.find_elements(*self.table)
      for i in range(1,len(table)+1):                                                                                       
        element=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[3]').text)
        element=element.upper()
        name.append((element))
      name.sort()
      self.browser.find_element(*self.farm_name_arrow).click()
      sorted=[]
      for i in range (1,len(table)+1):
        index=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[3]').text)
        index=index.upper()
        sorted.append((index))
      return name,sorted,table

    def farm_sorting_name_up(self,name,table):  
      name.reverse()
      sorted=[]
      self.browser.find_element(*self.farm_name_arrow).click()
      for i in range (1,len(table)+1):
        index1=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[3]').text)
        index1=index1.upper()
        sorted.append((index1))
      return name,sorted

    def farm_table_sorting_by_twin_id(self):
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.table_farm_name)) 
      id=[]
      table = self.browser.find_elements(*self.table)
      for i in range(1,len(table)+1):                                                                                       
        element=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[4]').text)
        id.append(int(element))
      id.sort()
      self.browser.find_element(*self.farm_twin_linked_arrow).click()
      sorted=[]
      for i in range (1,len(table)+1):
        index=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[4]').text)
        sorted.append(int(index))
      return id,sorted,table   
    
    def farm_table_sorting_by_twin_id_up(self,id,table):
      id.reverse()
      sorted=[]
      self.browser.find_element(*self.farm_twin_linked_arrow).click()
      for i in range (1,len(table)+1):
        index1=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[4]').text)
        sorted.append(int(index1))
      return id , sorted
      
    def farm_table_sorting_by_cerification_type(self):
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.table_farm_name))
      name=[]
      table = self.browser.find_elements(*self.table)
      for i in range(1,len(table)+1):                                                                                       
        element=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[5]').text)
        name.append((element))
      name.sort()
      self.browser.find_element(*self.certification_type_arrow).click()
      sorted=[]
      for i in range (1,len(table)+1):
        index=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[5]').text)
        sorted.append((index))
      return name ,sorted,table   

    def  farm_table_sorting_by_cerification_type_up(self,name,table): 
      name.reverse()
      sorted=[]
      for i in range (1,len(table)+1):
        index1=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[5]').text)
        sorted.append((index1))
      return name,sorted

    def farm_table_sorting_by_pp_id(self):
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.table_farm_name))      
      id=[]
      table = self.browser.find_elements(*self.table)
      for i in range(1,len(table)+1):                                                                                       
        element=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[6]').text)
        id.append(int(element))
      id.sort()
      self.browser.find_element(*self.pricing_policy_arrow).click()
      sorted=[]
      for i in range (1,len(table)+1):
        index=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[6]').text)
        sorted.append(int(index))
      return id,sorted,table

    def farm_table_sorting_by_pp_id_up(self,id,table):  
      id.reverse()
      sorted=[]
      self.browser.find_element(*self.pricing_policy_arrow).click()
      for i in range (1,len(table)+1):
        index1=(self.browser.find_element(By.XPATH, self.table_row + str(i) + ']/td[6]').text)
        sorted.append(int(index1))
      return id, sorted

    def setup_farmpayout_address(self):
      self.browser.find_element(*self.details_arrow).click()
      self.browser.find_element(*self.add_v2_button).click()

    def add_farmpayout_address(self, data):
      self.browser.find_element(*self.path).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.path).send_keys(Keys.DELETE)
      self.browser.find_element(*self.path).send_keys(data)
      return self.browser.find_element(*self.submit_button)
    
    def setup_gateway(self, data):
      self.browser.find_element(*self.details_arrow).click()
      self.browser.find_element(*self.public_ip_list).click()
      self.browser.find_element(*self.add_ip_button).click()
      self.browser.find_element(*self.gateway_text_field).send_keys(data)

    def add_ip(self, data):
      self.browser.find_element(*self.ip_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.ip_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.ip_text_field).send_keys(data) 
      return self.browser.find_element(*self.save_button)

    def setup_ip(self, data):
      self.browser.find_element(*self.details_arrow).click()
      self.browser.find_element(*self.public_ip_list).click()
      self.browser.find_element(*self.add_ip_button).click()
      self.browser.find_element(*self.ip_text_field).send_keys(data)

    def add_gateway(self, data):
      self.browser.find_element(*self.gateway_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.gateway_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.gateway_text_field).send_keys(data) 
      return self.browser.find_element(*self.save_button)

    def delete_ip(self):
      self.browser.find_element(*self.details_arrow).click()
      self.browser.find_element(*self.details_arrow).click()
      self.browser.find_element(*self.public_ip_list).click()
      self.browser.execute_script("arguments[0].scrollIntoView(true);",
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.delete_ip_button)))      
      self.browser.execute_script("arguments[0].click();",
      WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(self.delete_ip_button))) 
      WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(self.delete_button))
      self.browser.find_element(*self.delete_button).click()
      
    def farm_detials(self):
      details = []
      for i in range(5): 
        details.append(self.browser.find_element(By.XPATH, self.node_expan_details+ str(i+1) +']/div[2]/div/span').text)
      details.append(self.browser.find_element(*self.stellar_payout_address).text)
      for i in range(len(self.browser.find_elements(By.XPATH, self.farm_public_ips))):
        details.append(self.browser.find_element(By.XPATH, self.farm_public_ips+ '['+ str(i+1) +']/td[1]').text)
        details.append(self.browser.find_element(By.XPATH, self.farm_public_ips+ '['+ str(i+1) +']/td[3]').text)
        details.append(self.browser.find_element(By.XPATH, self.farm_public_ips+ '['+ str(i+1) +']/td[2]').text)
      return details

    def verify_the_availability_of_zero_os_bootstrap(self):
      self.browser.find_element(*self.details_arrow).click()
      self.browser.find_element(*self.view_bootstrap_button).click()
      WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
      self.browser.switch_to.window(self.browser.window_handles[1])
      return self.browser.current_url

    def wait_for(self, keyword):
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '"+ keyword +"')]")))
        return True
