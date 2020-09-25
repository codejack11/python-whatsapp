from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time

class whatsappBot():

    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get("https://web.whatsapp.com")
        print("Scan QR Code, And then Enter")
        input()
        print("Logged In")
        self.main_menu()

    def main_menu(self):
        print("\n\nSelect one from below options:")
        print("1. Send Bulk messages")
        print("2. Send single message")

        selected_option = input()
        self.get_method(selected_option)

    def send_bulk_messages(self):
        print("\n\nSelect one from below options:")
        print("Enter path for CSV file")
        csv_filepath = input()
        print("\nloading csv....\n\n")
        contacts = pd.DataFrame()
        try:
            contacts = pd.read_csv(csv_filepath)
        except Exception:
            print("Cannot find file. Make sure the path is correct.\n\n")
            self.send_bulk_messages()

        print("Enter message")
        message = input()
        for index, row in contacts.iterrows():
            self.send_msg_with_phone_numbers(row[0], message)
            time.sleep(1)

        print("\nRedirecting to main menu...")
        time.sleep(1)
        self.main_menu()

    def send_msg(self):
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
            send_btn = WebDriverWait(self.driver, 500).until(element_present)
            print("Page is ready!")
            send_btn.click()
        except TimeoutException:
            print ("Timed out waiting for page to load")

    def send_msg_with_phone_numbers(self, contact_number, msg):
        try:
            self.driver.get("https://web.whatsapp.com/send?phone=91" + str(contact_number) + "&text='"+msg+"'")
        except Exception:
            print("\nThis contact not found: " + str(contact_number))
        # time.sleep(2)
        self.send_msg()

    def send_single_message(self):
        print("\n\nEnter name or number of a person")
        user_input = input()

        try:
            number = int(user_input)
            print("Enter message")
            message = input()
            self.send_msg_with_phone_numbers(number, message)
            
        except Exception:
            name = str(user_input)
            input_box_search = self.driver.find_element_by_xpath("//div[@class='_3FRCZ copyable-text selectable-text']")
            input_box_search.send_keys(name)

            try:
                time.sleep(1)
                select_from_search = self.driver.find_element_by_xpath("//div[@class='eJ0yJ']")
                select_from_search.click()

                print("Enter message")
                message = input()

                msg_box = ActionChains(self.driver)
                msg_box.send_keys(message)
                msg_box.perform()
                self.send_msg()
            
            except Exception:
                print("No contact found")

        print("\nRedirecting to main menu...")
        time.sleep(1)
        self.main_menu()

    def invalid_option(self):
        print("\n\nplease select valid option")

        print("\nRedirecting to main menu...")
        time.sleep(1)
        self.main_menu()

    def get_method(self, x):
        switcher = {
            '1': self.send_bulk_messages,
            '2': self.send_single_message,
        }
        func = switcher.get(x, self.invalid_option)

        return func()

bot = whatsappBot()
bot.login()
# import time
# contact = ['8905969487','7990681191']
# text = "Hey, this message was sent using Selenium"
# driver = webdriver.Chrome()
# driver.get("https://web.whatsapp.com")
# print("Scan QR Code, And then Enter")
# input()
# print("Logged In")

# timeout = 500

# for i in contact:
#     driver.get("https://web.whatsapp.com/send?phone=91" + i + "&text='"+text+"'")
#     # time.sleep(2)
#     try:
#         element_present = EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
#         target = WebDriverWait(driver, timeout).until(element_present)
#         print("Page is ready!")
#     except TimeoutException:
#         print ("Timed out waiting for page to load")


# ------------------------------------------------------------------------------------
    # send = driver.find_element_by_xpath("//button[@class='_1U1xa']")
    # send.click()
    # &text=%27Hey%2C+this+message+was+sent+using+Selenium%27&source&data&app_absent
    
# inp_xpath_search = "//input[@title='Search or start new chat']"
# input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
# input_box_search.click()
# time.sleep(2)
# input_box_search.send_keys(contact)
# time.sleep(2)
# selected_contact = driver.find_element_by_xpath("//button[@class="_1U1xa"]")
# selected_contact.click()
# inp_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
# input_box = driver.find_element_by_xpath(inp_xpath)
# time.sleep(2)
# input_box.send_keys(text + Keys.ENTER)
# time.sleep(2)
# driver.quit()
