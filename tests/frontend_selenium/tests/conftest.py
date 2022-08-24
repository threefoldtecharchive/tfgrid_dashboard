import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

"""
This module contains shared browser fixtures.
"""

@pytest.fixture
def browser():

  # Initialize the ChromeDriver instance with options
  options = webdriver.ChromeOptions()
  options.add_extension('polka_extension_0_44_1_0.crx')  #PolkaDot Extension
  options.add_argument("--start-maximized")
  driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

  # Make its calls wait up to 20 seconds for elements to appear
  driver.implicitly_wait(20)

  # Return the WebDriver instance for the setup
  yield driver

  # Quit the WebDriver instance for the cleanup
  driver.quit() 