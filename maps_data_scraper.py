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

from lugar_maps import LugarMaps


class GoogleMapsDataScraper:

    def __init__(self, idioma, imgOutput):
        self.driver = None
        self.errorCont = 0
        self.imgOutput = imgOutput
        self.configuracion = self.setConfiguracion(idioma)

    def setConfiguracion(self, idioma):
        conf = {
            'idioma': '--lang=es-ES',
            'textoEstrellas': 'estrellas',
            'textoReviews': 'reseñas',
            'textoDireccion': 'Dirección: ',
            'textoWeb': 'Sitio web: ',
            'textoTelefono': 'Teléfono: ',
            'textoPlusCode': 'Plus Code: ',
            'textoHorario': 'Ocultar el horario de la semana',
            'remplazarHorario': [' Ocultar el horario de la semana', 'El horario podría cambiar', '; ']
        }
        if (idioma == 'EN'):
            conf['idioma'] = '--lang=en-GB'
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
            chrome_options.add_argument(self.configuracion['idioma'])
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

    def scrapearDatos(self, kw):
        print("============scrapping datas from google map====================")
        try:
            final_lugar = []
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
            lugar = LugarMaps()
            elements = self.driver.find_elements(By.CLASS_NAME, 'Nv2PK')
            count = len(elements)
            for i in range(count):
                inputBox.clear()
                inputBox.click()
                time.sleep(1)
                inputBox.send_keys(kw)
                time.sleep(1)
                inputBox.send_keys(Keys.ENTER)
                time.sleep(5)
                elements = self.driver.find_elements(By.CLASS_NAME, 'Nv2PK')
                data = elements[i]
                data.click()
                print("==========opened new element===========")
                time.sleep(5)
                print("==========started scrapping an element===========" +
                      str(i+1) + "/" + str(count) + "===================")

                lugar.keyword = kw
                lugar.name = self.driver.find_element(
                    By.XPATH, '//div[@class="lMbq3e"]/div/h1/span[1]').text
                print("==========scrapped name===========" +
                      lugar.name+"=================")
                lugar.category = self.driver.find_element(
                    By.XPATH, '//*[@jsaction="pane.rating.category"]').text
                print("==========scrapped category===========" +
                      lugar.category+"=================")
                lugar.direction = self.driver.find_element(
                    By.XPATH, '//*[contains(@aria-label, "Address: ")]').get_attribute("aria-label")
                print("==========scrapped direction===========" +
                      lugar.direction+"=================")
                lugar.phone_number = self.driver.find_element(
                    By.XPATH, '//*[contains(@aria-label, "Phone: ")]').get_attribute("aria-label")
                print("==========scrapped phone_number===========" +
                      lugar.phone_number+"=================")
                lugar.website = self.driver.find_element(
                    By.XPATH, '//*[contains(@aria-label, "Website: ")]').get_attribute("aria-label")
                print("==========scrapped website===========" +
                      lugar.website+"=================")
                lugar.plus_code = self.driver.find_element(
                    By.XPATH, '//*[contains(@aria-label, "Plus code: ")]').get_attribute("aria-label")
                print("==========scrapped plus_code===========" +
                      lugar.plus_code+"=================")
                lugar.open_hours = self.driver.find_element(
                    By.XPATH, '//*[contains(@aria-label, "Hide open hours for the week")]').get_attribute("aria-label")
                print("==========scrapped open_hours===========" +
                      lugar.open_hours+"=================")
                lugar.stars = self.driver.find_element(
                    By.XPATH, '//*[@jsaction="pane.rating.moreReviews"]/span[1]/span/span[1]').text
                print("==========scrapped stars===========" +
                      lugar.stars+"=================")
                lugar.reviews = self.driver.find_element(
                    By.XPATH, '//*[@jsaction="pane.rating.moreReviews"]/span[2]/span/span[1]').text
                print("==========scrapped reviews===========" +
                      lugar.reviews+"=================")
                print("........................................................")
                print('------------scrapped an element for ' +
                      kw + "---------------")
                print(lugar)
                final_lugar.append(lugar)
                print(final_lugar)
            print("============Completed scrapping for" +
                  kw + "====================")
            return lugar
        except Exception as e:
            print(e)
            self.errorCont += 1
            return None

    def endDriver(self):
        self.driver.quit()
