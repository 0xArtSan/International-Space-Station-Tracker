from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get('https://www.amazon.es/Pathfinder-RPG-Advanced-Players-Guide/dp/1640782575/ref=sr_1_5?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3PE2FN5EUWIC4&keywords=pathfinder+advanced&qid=1682319543&sprefix=pathfinder+advanced%2Caps%2C101&sr=8-5')

price = driver.find_element(By.CLASS_NAME, 'a-offscreen')
print('Pathfinder[2e]: Advanced Players Guide: ' + price.get_attribute('innerHTML'))
driver.close()
