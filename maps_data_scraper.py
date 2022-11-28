# -*- coding: utf-8 -*-

import random
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from place_maps import PlaceMaps


class GoogleMapsDataScraper:

    def __init__(self, language, imgOutput):
        self.driver = None
        self.errorCont = 0
        self.imgOutput = imgOutput
        self.configuracion = self.setConfiguracion(language)

    def setConfiguracion(self, language):
        conf = {
            'language': '--lang=es-ES',
            'textoEstrellas': 'estrellas',
            'textoReviews': 'reseñas',
            'textoDireccion': 'Dirección: ',
            'textoWeb': 'Sitio web: ',
            'textoTelefono': 'Teléfono: ',
            'textoPlusCode': 'Plus Code: ',
            'textoHorario': 'Ocultar el horario de la semana',
            'remplazarHorario': [' Ocultar el horario de la semana', 'El horario podría cambiar', '; ']
        }
        if (language == 'EN'):
            conf['language'] = '--lang=en-GB'
            conf['textoEstrellas'] = 'stars'
            conf['textoReviews'] = 'reviews'
            conf['textoDireccion'] = 'Address: '
            conf['textoWeb'] = 'Website: '
            conf['textoTelefono'] = 'Phone: '
            conf['textoPlusCode'] = 'Plus code: '
            conf['textoHorario'] = 'Hide open hours for the week'
            conf['remplazarHorario'] = [
                '. Hide open hours for the week', 'Hours might differ', '; ']

        return conf

    def initDriver(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument(self.configuracion['language'])
            s = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=s, options=chrome_options)
            self.driver.get('https://www.google.com/')
            try:
                self.driver.find_element(By.XPATH, '//*[@id="L2AGLb"]').click()
            except:
                pass
            time.sleep(2)
            self.driver.get('https://www.google.com/maps/')
            return True
        except:
            print('Error with the Chrome Driver')
            return False

    def scraperDatas(self, kw):
        print("============scrapping datas from google map====================")
        try:
            final_place = []
            if (self.errorCont == 5):
                self.errorCont = 0
                time.sleep(1)
                self.driver.get('https://www.google.com/maps/')
                time.sleep(2)
            time.sleep(random.randint(1, 3))
            inputBox = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@id="searchboxinput"]')))
            print("==========tracked search_box============")
            inputBox.click()
            inputBox.clear()
            print("==========cleared search_box============")
            inputBox.click()
            time.sleep(1)
            print("==========sending key-" + kw +
                  " -to the search_box============")
            inputBox.send_keys(kw)
            time.sleep(1)
            inputBox.send_keys(Keys.ENTER)
            time.sleep(5)
            print("==========sent key-" + kw+" -to the search_box============")
            place = PlaceMaps()

            try:
                scrollable_div = self.driver.find_element(
                    By.XPATH, '//div[@class="lXJj5c Hk4XGb"]')

                while scrollable_div:
                    try:
                        scrolled = self.driver.find_element(
                            By.CLASS_NAME, 'HlvSq').text
                        if scrolled == "You've reached the end of the list.":
                            break
                    except:
                        print("Searching...")
                        self.driver.execute_script(
                            'document.getElementsByClassName("dS8AEf")[1].scrollTop = document.getElementsByClassName("dS8AEf")[1].scrollHeight',
                            scrollable_div
                        )
                        time.sleep(3)
            except:
                print("Searched all available elements.")
                pass

            elements = self.driver.find_elements(By.CLASS_NAME, 'Nv2PK')
            time.sleep(5)
            count = len(elements)
            for i in range(count):
                inputBox.clear()
                inputBox.click()
                time.sleep(1)
                inputBox.send_keys(kw)
                time.sleep(1)
                inputBox.send_keys(Keys.ENTER)
                time.sleep(5)
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'Nv2PK')))
                elements = self.driver.find_elements(By.CLASS_NAME, 'Nv2PK')
                if len(elements) < i+1:
                    while len(elements) < i+1:
                        scrollable_div = self.driver.find_element(
                            By.XPATH, '//div[@class="lXJj5c Hk4XGb"]')
                        self.driver.execute_script(
                            'document.getElementsByClassName("dS8AEf")[1].scrollTop = document.getElementsByClassName("dS8AEf")[1].scrollHeight',
                            scrollable_div
                        )
                        time.sleep(3)
                        scrolled_elements = self.driver.find_elements(
                            By.CLASS_NAME, 'Nv2PK')
                        elements = scrolled_elements
                data = elements[i]
                data.click()
                print("==========opened new element===========")
                time.sleep(5)
                print("==========started scrapping an element===========" +
                      str(i+1) + "/" + str(count) + "===================")

                place.keyword = kw
                try:
                    place.name = self.driver.find_element(
                        By.XPATH, '//div[@class="lMbq3e"]/div/h1/span[1]').text
                except:
                    place.name = 'Unkown name'
                print("==========scrapped name===========" +
                      place.name+"=================")
                try:
                    place.category = self.driver.find_element(
                        By.XPATH, '//*[@jsaction="pane.rating.category"]').text
                except:
                    place.category = 'No given'
                print("==========scrapped category===========" +
                      place.category+"=================")
                try:
                    place.direction = self.driver.find_element(
                        By.XPATH, '//*[contains(@aria-label, "Address: ")]').get_attribute("aria-label")
                except:
                    place.direction = ''
                print("==========scrapped direction===========" +
                      place.direction+"=================")
                try:
                    place.phone_number = self.driver.find_element(
                        By.XPATH, '//*[contains(@aria-label, "Phone: ")]').get_attribute("aria-label")
                except:
                    place.phone_number = ''
                print("==========scrapped phone_number===========" +
                      place.phone_number+"=================")
                try:
                    place.website = self.driver.find_element(
                        By.XPATH, '//*[contains(@aria-label, "Website: ")]').get_attribute("aria-label")
                except:
                    place.website = ''
                print("==========scrapped website===========" +
                      place.website+"=================")
                try:
                    place.plus_code = self.driver.find_element(
                        By.XPATH, '//*[contains(@aria-label, "Plus code: ")]').get_attribute("aria-label")
                except:
                    place.plus_code = ''
                print("==========scrapped plus_code===========" +
                      place.plus_code+"=================")
                try:
                    place.open_hours = self.driver.find_element(
                        By.XPATH, '//*[contains(@aria-label, "Hide open hours for the week")]').get_attribute("aria-label")
                except:
                    place.open_hours = ''
                print("==========scrapped open_hours===========" +
                      place.open_hours+"=================")
                try:
                    place.stars = self.driver.find_element(
                        By.XPATH, '//*[@jsaction="pane.rating.moreReviews"]/span[1]/span/span[1]').text
                except:
                    place.stars = ''
                print("==========scrapped stars===========" +
                      place.stars+"=================")
                try:
                    place.reviews = self.driver.find_element(
                        By.XPATH, '//*[@jsaction="pane.rating.moreReviews"]/span[2]/span/span[1]').text
                except:
                    place.reviews = 'No reviews'
                print("==========scrapped reviews===========" +
                      place.reviews+"=================")
                print("........................................................")
                print('------------scrapped an element for ' +
                      kw + "---------------")
                final_place.append(place)
            print("============Completed scrapping for" +
                  kw + "====================")
            return final_place
        except Exception as e:
            print(e)
            self.errorCont += 1
            return None

    def endDriver(self):
        self.driver.quit()
