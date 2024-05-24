import os
import time
from datetime import datetime

import PyPDF2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import openai

def main1():
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")  # Optional, but sometimes helpful for headless mode.

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    logIn(driver, "adatta18", "Quechua@2406")




def extract_text_from_pdf(pdf_path):
    pdf_text = ""

    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_text += page.extract_text() + "\n"
        return (pdf_text.strip())
    except:
        print("text could not be extracted from the pdgf")

def logIn(driver, username, password):
    driver.get("https://weblogin.asu.edu/cas/login?service=http"
               "s%3A%2F%2Fweblogin.asu.edu%2Fcgi-bin%2Fcas-login%"
               "3Fcallapp%3Dhttps%253A%252F%252Fwebapp4.asu.edu%2"
               "52Fmyasu%252F%253Finit%253Dfalse")
    user1 = driver.find_element(By.ID, "username")
    user1.send_keys(username)
    pass1 = driver.find_element(By.ID, "password")
    pass1.send_keys(password, Keys.ENTER)

    time.sleep(5)

    iframe = driver.find_element(By.ID, "duo_iframe")
    driver.switch_to.frame(iframe)
    time.sleep(1)
    print("switched to frame")
    duo_push = driver.find_element(By.XPATH,
                                   "//button[contains(@class, 'auth-button') and contains(@class, 'positive')]")
    duo_push.click()
    time.sleep(5)
main1()
