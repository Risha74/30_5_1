from telnetlib import EC

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('/Users/ipusi1/Desktop/test/chromedriver')
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()


def test_pets_cards():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('testing111@internet.ru')
   # Водим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('test4testing')
   # нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   pytest.driver.implicitly_wait(10)
   # находим все изображения в карточках питомцев
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   # находим все имена в карточках питомцев
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   # находим все породы и возрасты в карточках питомцев
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
       # проверяем, что все питомцы имеет фото
       assert images[i].get_attribute('src') != ''
       # проверяем, что все питомцы имеют имя
       assert names[i].text != ''
       # проверяем, что все питомцы имеют информацию о породе и возрасте
       assert descriptions[i].text != ''
       parts = descriptions[i].text.split(", ")
       # проверяем, что у каждого питомца указана порода
       assert len(parts[0]) > 0
       # проверяем, что у каждого питомца указан возраст
       assert len(parts[1]) > 0



def test_pets_table():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('testing111@internet.ru')
   # Водим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('test4testing')

   WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
   # нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # нажимаем на кнопку "Мои питомцы"
   pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()

   # находим количество питомцев из статистики пользователя
   pets_numb = int(pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(":")[1])
   # находим всех питомцев в таблице
   all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   # находим все изображения в таблице
   images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
   # находим все имена питомцев в таблице
   names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
   # находим все породы питомцев в таблице
   pets_types = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
   # находим все возрасты питомцев в таблице
   ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

   name_list = []
   pets = {}
   count = 0

   # проверяем, что количество питомцев в таблице соответствует количеству питомцев из статистики пользователя
   assert pets_numb == len(all_pets)

   for i in range(len(images)):
      if images[i].get_attribute('src'):
         count += 1
   # проверяем, что количество питомцев с фото составляет не менеее половины от всех питомцев
   assert count >= pets_numb / 2

   for i in range(len(names)):
      # проверяем, что у всех питомцев есть имя, порода и возраст
      assert names[i].text != ''
      assert pets_types[i].text != ''
      assert ages[i].text != ''
      name_list.append(names[i].text)

   # проверяем уникальность имен питомцев
   assert len(name_list) == len(list(set(name_list)))

   # проверяем уникальность питомцев
   for i in range(len(all_pets)):
      check = False
      if str(names[i].text + '_' + pets_types[i].text + '_' + ages[i].text).lower() in pets:
         check = True
      assert check == False
      if not check:
         pets[str(names[i].text + '_' + pets_types[i].text + '_' + ages[i].text).lower()] = True

