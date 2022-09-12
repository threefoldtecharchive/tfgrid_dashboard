from utils.base import Base
from pages.polka import PolkaPage
from utils.utils import generate_gateway, generate_string
from utils.utils import generate_ip
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
  farm=(By.XPATH,'//*[@id="app"]/div[1]/nav/div[1]/div/div[2]/div[2]/div/div/div[2]/div[4]')
  title=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/h3')
  create_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/button')
  farm_name_text_field=(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[1]/form/div/div/div[1]/div/input')
  farm_name_warning=(By.XPATH,'//*[@id="app"]/div[5]/div/div/div[1]/form/div/div/div[2]/div/div/div')
  submit_farm_button=(By.XPATH ,'//*[@id="app"]/div[4]/div/div/div[2]/button[1]/span')
  msg1=(By.XPATH,'//*[@id="zV6r5X-VI"]/div')
  created_msg=(By.XPATH,'//*[@id="zV6r5X-VI"]')
  search_bar=(By.XPATH ,'/html/body/div[1]/div[1]/div[3]/div/div[2]/div[3]/div/div[1]/div/input')
  farms_table=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/header/div')
  details_arrow=(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[1]/button')
  farm_Id_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/thead/tr/th[2]')
  farm_name_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/thead/tr/th[3]/i')
  farm_twin_linked_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/thead/tr/th[4]/i')
  certification_type_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/thead/tr/th[5]/i')
  pricing_policy_arrow=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/thead/tr/th[6]/i')
  add_v2_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[2]/td/div/div[6]/div[2]/div/button')
  ip_v2_textfield=('//*[@id="input-228"]')
  submit_button=(By.XPATH,'//*[@id="app"]/div[4]/div/div/div[2]/button[2]')
  edit_v2_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[2]/td/div/div[6]/div[2]/div/button/span')
  view_bootstrap_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[2]/td/div/div[7]/div[2]/div/a/span')
  public_ip_list=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/button/div')
  add_ip_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/header/div/div/button/span')
  ip_text_field=(By.XPATH ,'//*[@id="app"]/div[4]/div/div/div[2]/div[2]/div/div[1]/div/input')
  path=(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[1]/form/div/div/div[1]/div/input')  
  gateway_text_field=(By.XPATH ,'/html/body/div[1]/div[4]/div/div/div[2]/div[3]/div/div[1]/div/input')
  ip_warning_msg=(By.XPATH ,'//*[@id="app"]/div[7]/div/div/div[2]/div[1]/div/div[2]/div/div/div')
  gateway_warning_msg=(By.XPATH ,'//*[@id="app"]/div[7]/div/div/div[2]/div[2]/div/div[2]/div/div/div')
  save_button=(By.XPATH ,'//*[@id="app"]/div[4]/div/div/div[3]/button[3]')
  delete_ip_button=(By.XPATH ,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[2]/td/div/div[8]/div/div/div/div/div/table/tbody/tr/td[4]/div/button')
  delete_button=(By.XPATH,'//*[@id="app"]/div[4]/div/div/div[3]/button[2]')
  zero=(By.XPATH,'//html/body/main/div[1]/div/h1')
  
  def __init__(self, browser):
    self.browser = browser

  def load(self):
    self.browser.get(Base.base_url)  

  def navigetor(self):
    self.browser.find_element(*self.account_choice).click()
    self.browser.find_element(*self.farm).click()
  
  def create_farm(self,password):
    farm_name=generate_string()
    polka_page = PolkaPage(self.browser)
    self.browser.find_element(*self.create_button).click()
    self.browser.find_element(*self.farm_name_text_field).send_keys(farm_name)
    self.browser.find_element(*self.submit_farm_button).click()
    polka_page.authenticate_with_pass(password) 

  def create_farm_with_existing_name(self):
    farm_name=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]').text)
    self.browser.find_element(*self.create_button).click()
    self.browser.find_element(* self.farm_name_text_field).send_keys(farm_name)
    self.browser.find_element(*self.submit_farm_button).click()

  def verify_search_functionality(self,password):
    #Test Data: [ use the whole name of the farm, only the first part, the second part ]
    polka_page = PolkaPage(self.browser)
    farm_name2=generate_string()
    self.browser.find_element(*self.create_button).click()
    self.browser.find_element(* self.farm_name_text_field).send_keys(farm_name2)
    self.browser.find_element(*self.submit_farm_button).click()
    polka_page.authenticate_with_pass(password)
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/button' )))      
    self.browser.find_element(*self.search_bar).send_keys(farm_name2)
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))      
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table').text
    assert farm_name2 in table

    FirstPart=farm_name2[0:len(farm_name2)//2]
    for i in range(len(farm_name2)):
        self.browser.find_element(*self.search_bar).send_keys(Keys.BACKSPACE)
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))      
    self.browser.find_element(*self.search_bar).send_keys(FirstPart)
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table').text
    assert farm_name2 in table

    for i in range(len(FirstPart)):
        self.browser.find_element(*self.search_bar).send_keys(Keys.BACKSPACE)
    EndPart=farm_name2[len(farm_name2)//2: len(farm_name2)]
    self.browser.find_element(*self.search_bar).send_keys(EndPart)
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table').text
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' ))) 
    assert farm_name2 in table
    
  def search_for_unexisting_farm(self,password): 
    AnotherName=generate_string()
    self.browser.find_element(*self.search_bar).send_keys(AnotherName)
    table= self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table').text
    return table
    
  def farm_table_sorting_by_id(self):
    WebDriverWait(self.browser, 30).until(
          EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))
    id=[]
    rows =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(rows)):                                                                                       
        element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]').text)
        id.append(int(element))
    id.sort()
    self.browser.find_element(*self.farm_Id_arrow).click()
    sorted=[]
    for i in range (1,len(rows)):
        index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]').text)
        sorted.append(int(index))
    return id,sorted,rows
    
  def farm_table_sorting_by_id_up(self,id,rows):    
    id.reverse()
    sorted=[]
    self.browser.find_element(*self.farm_Id_arrow).click()
    for i in range (1,len(rows)):
        index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]').text)
        sorted.append(int(index1))
    return id,sorted

  def farm_table_sorting_by_name(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))      
    name=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)):                                                                                       
        element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text)
        element=element.upper()
        name.append((element))
    name.sort()
    self.browser.find_element(*self.farm_name_arrow).click()
    sorted=[]
    for i in range (1,len(table)):
        index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text)
        index=index.upper()
        sorted.append((index))
    return name,sorted,table

  def farm_sorting_name_up(self,name,table):  
    name.reverse()
    sorted=[]
    self.browser.find_element(*self.farm_name_arrow).click()
    for i in range (1,len(table)):
        index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[3]').text)
        index1=index1.upper()
        sorted.append((index1))
    return name,sorted   

  def farm_table_sorting_by_twin_id(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' ))) 
    id=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)):                                                                                       
        element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[4]').text)
        id.append(int(element))
    id.sort()
    self.browser.find_element(*self.farm_twin_linked_arrow).click()
    sorted=[]
    for i in range (1,len(table)):
        index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[4]').text)
        sorted.append(int(index))
    return id,sorted,table   
  
  def farm_table_sorting_by_twin_id_up(self,id,table):
    id.reverse()
    sorted=[]

    self.browser.find_element(*self.farm_twin_linked_arrow).click()
    for i in range (1,len(table)):
        index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[4]').text)
        sorted.append(int(index1))
    return id , sorted

  def farm_table_sorting_by_cerification_type(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))
    name=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)):                                                                                       
        element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').text)
        name.append((element))
    name.sort()
    self.browser.find_element(*self.certification_type_arrow).click()
    sorted=[]
    for i in range (1,len(table)):

        index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').text)
        sorted.append((index))
    return name ,sorted,table   

  def  farm_table_sorting_by_cerification_type_up(self,name,table): 
    name.reverse()
    sorted=[]

    self.browser.find_element(*self.certification_type_arrow).click()
    for i in range (1,len(table)):
        index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[5]').text)
        sorted.append((index1))
    return name,sorted

  def farm_table_sorting_by_pp_id(self):
    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[3]' )))      
    id=[]
    table =self.browser.find_elements(By.XPATH,'//table/tbody/tr')
    for i in range(1,len(table)):                                                                                       
        element=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[6]').text)
        id.append(int(element))
    id.sort()
    self.browser.find_element(*self.pricing_policy_arrow).click()
    sorted=[]
    for i in range (1,len(table)):
        index=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[6]').text)
        sorted.append(int(index))
    return id,sorted,table

  def farm_table_sorting_by_pp_id_up(self,id,table):  
    id.reverse()
    sorted=[]

    self.browser.find_element(*self.pricing_policy_arrow).click()
    for i in range (1,len(table)):
        index1=(self.browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[3]/div/div[2]/div[4]/div[1]/table/tbody/tr[' + str(i) + ']/td[6]').text)
        sorted.append(int(index1))
    return id, sorted

  def add_farmpayout_address(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.add_v2_button).click()
    self.browser.find_element(*self.path).send_keys("GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG")
    self.browser.find_element(*self.submit_button).click()
  
  def edit_farmpayout_address(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.edit_v2_button).click()
    self.browser.find_element(*self.path).send_keys("GDHJP6TF3UXYXTNEZ2P36J5FH7W4BJJQ4AYYAXC66I2Q2AH5B6O6BCFG")
    self.browser.find_element(*self.submit_button).click()
    
  def add_ip(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    ip=generate_ip()
    gateway=generate_gateway()
    self.browser.find_element(*self.ip_text_field).send_keys(ip)
    self.browser.find_element(*self.gateway_text_field).send_keys(gateway)
    self.browser.find_element(*self.save_button).click()
    
  def add_valid_ip(self,cases):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.ip_text_field).send_keys(cases)

  def add_valid_gateawy(self,cases):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.gateway_text_field).send_keys(cases) 
  
  def delete_ip(self,):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.execute_script("arguments[0].scrollIntoView(true);",
    WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located(self.delete_ip_button)))      
    self.browser.execute_script("arguments[0].click();",
    WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable(self.delete_ip_button)))      
    self.browser.find_element(*self.delete_button).click()
    
  def add_invalid_ip(self,cases):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.ip_text_field).click()
    self.browser.find_element(*self.ip_text_field).send_keys(cases)
    element = self.browser.find_element(*self.save_button)
    return element
    
  def add_invalid_gateway(self,cases):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.public_ip_list).click()
    self.browser.find_element(*self.add_ip_button).click()
    self.browser.find_element(*self.gateway_text_field).send_keys(cases)
    element = self.browser.find_element(*self.save_button)
    return element
    
  def verify_the_availability_of_zero_os_bootstrap(self):
    self.browser.find_element(*self.details_arrow).click()
    self.browser.find_element(*self.view_bootstrap_button).click()
    WebDriverWait(self.browser, 30).until(EC.number_of_windows_to_be(2))
    self.browser.switch_to.window(self.browser.window_handles[1])
    link=self.browser.current_url
    return link
                                                                                                         