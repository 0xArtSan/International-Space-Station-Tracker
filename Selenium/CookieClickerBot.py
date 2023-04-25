from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import keyboard

driver = webdriver.Firefox()

driver.get('https://orteil.dashnet.org/cookieclicker/')

# driver.find_element(By.CLASS_NAME, '')

manage_cookies = driver.find_elements(By.CLASS_NAME, 'fc-button-label')

for item in manage_cookies:
    if item.get_attribute('innerHTML') == 'Consent':
        consent = item
consent.click()

sleep(1)
accept = driver.find_element(By.XPATH, '/html/body/div[1]/div/a[1]')
accept.click()

language = driver.find_element(By.ID, 'langSelect-EN')
language.click()

sleep(5)

close_message = driver.find_element(By.XPATH, '/html/body/div[2]/div/ins/img[3]')
close_message.click()

big_cookie = driver.find_element(By.ID, 'bigCookie')
amount_cookie = driver.find_element(By.ID, 'cookies')
counter = 0

is_running = True
while is_running:
    if counter > 10:
        generators = driver.find_elements(By.CLASS_NAME, 'enabled')
        try:
            generators[-1].click()
        except:
            pass
        counter = 0
    big_cookie.click()
    counter += 1
    if keyboard.is_pressed("p"):
        is_running = False
driver.close()
