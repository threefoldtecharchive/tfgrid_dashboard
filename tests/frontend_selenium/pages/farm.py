from utils.utils import generate_gateway, generate_inavalid_gateway, generate_inavalid_ip, generate_string, generate_ip
import requests
from utils.base import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FarmPage:
  
  navigate=(By.XPATH,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/i')
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
  
  def __init__(self, browser):
    self.browser = browser

  def load(self):
    self.browser.get(Base.base_url)  

  def navigetor(self,user):
    self.browser.find_element(By.XPATH, "//*[contains(text(), '"+ user +"')]").click()
    self.browser.find_element(*self.farm).click()

  def create_farm(self, farm_name):
    self.browser.find_element(*self.create_button).click()
    self.browser.find_element(*self.farm_name_text_field).send_keys(farm_name)
    self.browser.find_element(*self.submit_farm_button).click()
      
  def create_farm_with_existing_name(self, farm_name):
    self.browser.find_element(*self.create_button).click()
    self.browser.find_element(*self.farm_name_text_field).send_keys(farm_name)
    self.browser.find_element(*self.submit_farm_button).click()

  def create_farm_invalid_name(self):
    self.browser.find_element(*self.create_button).click()
    data = ['f', 'DD', '4', '88', '-', '_-']
    for i in range(len(data)):
      self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.farm_name_text_field).send_keys(data[i])
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Name should be more than or equal 3 characters')]" )
    data = [' ', 'f f', 'ddd#', 'ddd@', '88!', 'gg$', 'aa%', 'bb^', 'cc&', 'h8*', 's5()', '|~</;:']
    for i in range(len(data)):
      self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.farm_name_text_field).send_keys(data[i])
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Name is not formatted correctly (All letters + numbers and (-,_) are allowed')]" )  
    self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.CONTROL + "a")
    self.browser.find_element(*self.farm_name_text_field).send_keys(Keys.DELETE)
    self.browser.find_element(*self.farm_name_text_field).send_keys(generate_string()+generate_string()+'_'+generate_string()+generate_string())
    assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Name too long, only 40 characters permitted')]" )

  def verify_search_functionality(self, farm_name):    
    self.browser.find_element(*self.search_bar).send_keys(farm_name) 
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr/td[3]')))      
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table').text 
    assert farm_name in table
    FirstPart=farm_name[0:len(farm_name)//2]
    self.browser.find_element(*self.search_bar).send_keys(Keys.CONTROL + "a")
    self.browser.find_element(*self.search_bar).send_keys(Keys.DELETE)
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr/td[3]')))      
    self.browser.find_element(*self.search_bar).send_keys(FirstPart)
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table').text
    assert farm_name in table
    self.browser.find_element(*self.search_bar).send_keys(Keys.CONTROL + "a")
    self.browser.find_element(*self.search_bar).send_keys(Keys.DELETE)
    EndPart=farm_name[len(farm_name)//2: len(farm_name)]
    self.browser.find_element(*self.search_bar).send_keys(EndPart)
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table').text
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr/td[3]')))
    assert farm_name in table
    
  def search_for_unexisting_farm(self):
    AnotherName=generate_string()
    self.browser.find_element(*self.search_bar).send_keys(AnotherName)
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH,  "//*[contains(text(), 'No data available')]")))
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table').text
    return table

  def farm_table_sorting_by_id(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))
    id=[]
    rows =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(rows)+1):
      element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]').text)
      id.append(int(element))
    id.sort()
    self.browser.find_element(*self.farm_Id_arrow).click()
    sorted=[]
    for i in range (1,len(rows)+1):
      index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]').text)
      sorted.append(int(index))
    return id,sorted,rows
  
  def farm_table_sorting_by_id_up(self,id,rows):    
    id.reverse()
    sorted=[]
    self.browser.find_element(*self.farm_Id_arrow).click()
    for i in range (1,len(rows)+1):
      index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]').text)
      sorted.append(int(index1))
    return id,sorted

  def farm_table_sorting_by_name(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))      
    name=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)+1):                                                                                       
      element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text)
      element=element.upper()
      name.append((element))
    name.sort()
    self.browser.find_element(*self.farm_name_arrow).click()
    sorted=[]
    for i in range (1,len(table)+1):
      index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text)
      index=index.upper()
      sorted.append((index))
    return name,sorted,table

  def farm_sorting_name_up(self,name,table):  
    name.reverse()
    sorted=[]
    self.browser.find_element(*self.farm_name_arrow).click()
    for i in range (1,len(table)+1):
      index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text)
      index1=index1.upper()
      sorted.append((index1))
    return name,sorted

  def farm_table_sorting_by_twin_id(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[3]' ))) 
    id=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)+1):                                                                                       
      element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[4]').text)
      id.append(int(element))
    id.sort()
    self.browser.find_element(*self.farm_twin_linked_arrow).click()
    sorted=[]
    for i in range (1,len(table)+1):
      index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[4]').text)
      sorted.append(int(index))
    return id,sorted,table   
  
  def farm_table_sorting_by_twin_id_up(self,id,table):
    id.reverse()
    sorted=[]
    self.browser.find_element(*self.farm_twin_linked_arrow).click()
    for i in range (1,len(table)+1):
      index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[4]').text)
      sorted.append(int(index1))
    return id , sorted
    
  def farm_table_sorting_by_cerification_type(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))
    name=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)+1):                                                                                       
      element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').text)
      name.append((element))
    name.sort()
    self.browser.find_element(*self.certification_type_arrow).click()
    sorted=[]
    for i in range (1,len(table)+1):
      index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').text)
      sorted.append((index))
    return name ,sorted,table   

  def  farm_table_sorting_by_cerification_type_up(self,name,table): 
    name.reverse()
    sorted=[]
    self.browser.find_element(*self.certification_type_arrow).click()
    for i in range (1,len(table)+1):
      index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').text)
      sorted.append((index1))
    return name,sorted

  def farm_table_sorting_by_pp_id(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))      
    id=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)+1):                                                                                       
      element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[6]').text)
      id.append(int(element))
    id.sort()
    self.browser.find_element(*self.pricing_policy_arrow).click()
    sorted=[]
    for i in range (1,len(table)+1):
      index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[6]').text)
      sorted.append(int(index))
    return id,sorted,table

  def farm_table_sorting_by_pp_id_up(self,id,table):  
    id.reverse()
    sorted=[]
    self.browser.find_element(*self.pricing_policy_arrow).click()
    for i in range (1,len(table)+1):
      index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[6]').text)
      sorted.append(int(index1))
    return id, sorted

  def add_farmpayout_address(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.add_v2_button).click()
    self.browser.find_element(*self.path).send_keys("GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG")
    self.browser.find_element(*self.submit_button).click()

  def add_invalid_farmpayout_address(self):
    data = [' ', 'dgdd',generate_string(), 'gdhjP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6Bcfg']
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.add_v2_button).click()
    for i in range (len(data)):
      self.browser.find_element(*self.path).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.path).send_keys(Keys.DELETE)
      self.browser.find_element(*self.path).send_keys(data[i])
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'invalid address')]" )
    return self.browser.find_element(*self.submit_button)

  def edit_farmpayout_address(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.edit_v2_button).click()
    self.browser.find_element(*self.path).send_keys("GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG")
    self.browser.find_element(*self.submit_button).click()
    
  def add_valid_ip(self):
    data = ['2.0.0.1/32',  '3.0.0.0/16', '139.255.255.255/17', '59.15.35.78/25']
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.gateway_text_field).send_keys(generate_gateway())
    for i in range (len(data)):
      self.browser.find_element(*self.ip_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.ip_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.ip_text_field).send_keys(data[i]) 
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'IP address in CIDR format xxx.xxx.xxx.xxx/xx')]" )
    return self.browser.find_element(*self.save_button)
  
  def add_invalid_ip(self):
    data = [generate_inavalid_ip(), '1.0.0.0/66', '239.255.255/17', '239.15.35.78.5/25', '239.15.35.78.5', ' ', '*.#.@.!|+-']
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.ip_text_field).click()
    for i in range (len(data)):
      self.browser.find_element(*self.ip_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.ip_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.ip_text_field).send_keys(data[i])
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Incorrect format')]")
    self.browser.find_element(*self.ip_text_field).send_keys(Keys.CONTROL + "a")
    self.browser.find_element(*self.ip_text_field).send_keys(Keys.DELETE)
    self.browser.find_element(*self.ip_text_field).send_keys('255.0.0.1/32')
    assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'IP is not public')]")
    return self.browser.find_element(*self.save_button)

  def add_valid_gateawy(self):
    data = [generate_gateway(), '1.0.0.1',  '1.0.0.0', '255.255.255.255', '239.15.35.78', '1.1.1.1']
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.ip_text_field).send_keys(generate_ip())
    for i in range (len(data)):
      self.browser.find_element(*self.gateway_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.gateway_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.gateway_text_field).send_keys(data[i]) 
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Gateway for the IP in ipv4 format')]" )
    return self.browser.find_element(*self.save_button)

  def add_invalid_gateway(self):
    data = [generate_inavalid_gateway(), '1.0.0.',  '1:1:1:1', '522.255.255.255', '.239.35.78', '1.1.1.1/16', '239.15.35.78.5', ' ', '*.#.@.!|+-']
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.ip_text_field).send_keys(generate_ip())
    for i in range (len(data)):
      self.browser.find_element(*self.gateway_text_field).send_keys(Keys.CONTROL + "a")
      self.browser.find_element(*self.gateway_text_field).send_keys(Keys.DELETE)
      self.browser.find_element(*self.gateway_text_field).send_keys(data[i]) 
      assert self.browser.find_element(By.XPATH, "//*[contains(text(), 'Gateway is not formatted correctly')]" )
    return self.browser.find_element(*self.save_button)
     
  def add_ip(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.ip_text_field).send_keys(generate_ip())
    self.browser.find_element(*self.gateway_text_field).send_keys(generate_gateway())
    self.browser.find_element(*self.save_button).click()

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
      details.append(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div['+ str(i+1) +']/div[2]/div/span').text)
    details.append(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[6]/div[2]/div/div/span').text)
    for i in range(len(self.browser.find_elements(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr'))):
      details.append(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr['+ str(i+1) +']/td[1]').text)
      details.append(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr['+ str(i+1) +']/td[3]').text)
      details.append(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr['+ str(i+1) +']/td[2]').text)
    return details

  def get_farm_details(self, farm_name):
    r = requests.post('https://gridproxy.dev.grid.tf/farms?name='+ farm_name)
    details = r.json()
    return details

  def verify_the_availability_of_zero_os_bootstrap(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.view_bootstrap_button).click()
    WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
    self.browser.switch_to.window(self.browser.window_handles[1])
    return self.browser.current_url
