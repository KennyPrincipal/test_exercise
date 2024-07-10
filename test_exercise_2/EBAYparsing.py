import re
import csv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import uuid


class EbayScraper:
    def __init__(self, url):
        self.url = url

    def get_item_info(self):
        driver = self.setup_driver()
        driver.get(self.url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[@class="x-item-title__mainTitle"]/span[@class="ux-textspans ux-textspans--BOLD"]'))
            )
            title_element = driver.find_element(By.XPATH, '//h1[@class="x-item-title__mainTitle"]/span[@class="ux-textspans ux-textspans--BOLD"]')
            title = title_element.text.strip()
            price_element = driver.find_element(By.XPATH, '//div[@class="x-price-primary"]/span[@class="ux-textspans"]')
            # Витягую без усіх знаків (чисту ціну з плаваючою точкою, формат str)
            price = re.findall(r'\d+\.\d+', price_element.text)[0]
            image_link_element = driver.find_element(By.XPATH, '//div[@class="ux-image-carousel-item image-treatment '
                                                               'active  image"]/img')
            image_link = image_link_element.get_attribute('src')
            seller_element = driver.find_element(By.XPATH, '//div[@class="x-sellercard-atf__info__about-seller"]')
            seller_text = seller_element.get_attribute('title')
            #Перевірка, чи є доставка у країну (різний XPath) в залежності від гео
            try:
                shipping_price_element = driver.find_element(By.XPATH,
                                                             '//div[@class="ux-labels-values__values col-9"]//div[@class="ux-labels-values__values-content"]//span[contains(@class, "ux-textspans--BOLD") and not(contains(@class, "ux-textspans--NEGATIVE"))]')
                shipping_price = shipping_price_element.text.strip()
            except NoSuchElementException:
                try:
                    shipping_price_element = driver.find_element(By.XPATH,
                                                                 '//div[@class="ux-labels-values__values col-9"]//div[@class="ux-labels-values__values-content"]//span[@class="ux-textspans ux-textspans--BOLD ux-textspans--NEGATIVE"]')
                    shipping_price = shipping_price_element.text.strip()
                    # shipping_price = re.findall(r'\d+\.\d+', shipping_price_element.text)[0]  #Для отримання лише ціни
                except NoSuchElementException:
                    shipping_price = "Shipping information not found"

            try:
                shipping_price_element = driver.find_element(By.XPATH,
                                                             '//div[@class="ux-labels-values__values col-9"]//div[@class="ux-labels-values__values-content"]//span[contains(@class, "ux-textspans--BOLD") and not(contains(@class, "ux-textspans--NEGATIVE"))]')
                shipping_price = shipping_price_element.text.strip()
            except NoSuchElementException:
                try:
                    shipping_price_element = driver.find_element(By.XPATH,
                                                                 '//div[@class="ux-labels-values__values col-9"]//div[@class="ux-labels-values__values-content"]//span[@class="ux-textspans ux-textspans--BOLD ux-textspans--NEGATIVE"]')
                    shipping_price = shipping_price_element.text.strip()
                except NoSuchElementException:
                    shipping_price = "Shipping information not found"


            data = {
                'Title': title,
                'Price': price,
                'Image Link': image_link,
                'Seller': seller_text,
                'Shipping Price': shipping_price
            }

            # Запис у csv
            with open('ebay_product.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Title', 'Price', 'Image Link', 'Seller', 'Shipping Price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(data)

            print("Дані про товар успішно додані до таблиці ebay_product.csv!")

        except Exception as e:
            print("Помилка при отриманні інформації про товар:", str(e))
        finally:
            self.teardown_driver(driver)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        return uc.Chrome(options=chrome_options)

    def teardown_driver(self, driver):
        driver.quit()


if __name__ == "__main__":
    test = EbayScraper("https://www.ebay.com/itm/375468406029")
    test.get_item_info()
