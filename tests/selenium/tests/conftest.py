import pytest
from selenium import webdriver 

"""
This module contains shared browser fixtures.
"""

@pytest.fixture
def browser():

  # Initialize the ChromeDriver instance with options
  options = webdriver.ChromeOptions()
  options.add_extension('tests/selenium/polka_extension_0_44_1_0.crx')  #PolkaDot Extension
  options.add_argument("--start-maximized")
  driver = webdriver.Chrome(options=options)

  # Make its calls wait up to 20 seconds for elements to appear
  driver.implicitly_wait(20)

  # Return the WebDriver instance for the setup
  yield driver

  # Quit the WebDriver instance for the cleanup
  driver.quit() 