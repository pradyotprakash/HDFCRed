from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


driver = webdriver.Firefox()
driver.get("http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai-Metropolitan-Region&price=Y&pageOption=A")
open('out1', 'w').write(str(BeautifulSoup(driver.page_source)))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
t = WebDriverWait(driver, 60).until(True)
open('out2', 'w').write(str(BeautifulSoup(driver.page_source)))

driver.close()