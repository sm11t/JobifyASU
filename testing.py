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
    folder_path = "/Users/shiro/Desktop"
    jobName = "HELLOER"
    file_path_cover_letter = os.path.join(folder_path, f"{jobName}_CL.pdf")
    print(file_path_cover_letter)

    openai.api_key = "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"  # Use your API key
    current_date = datetime.now().strftime("%B %d, %Y")
    print("got current date")
    prompt = (
        "thiis is a test"
    )
    print("prompt given")
    print()

    # Adjusted API call using the new interface

    prompt = (
        f"This should be the starting of every cover letter - "
        f"Asmit Datta"
        f"1000 E Apache Blvd, Tempe AZ 85281"
        f"new line"
        f"{current_date}"
        f"Get the details of the hiring manager, department from the job description"
        f"Generate a compelling cover letter tailored to the following job description and my resume. this one is a test just generate anything you like any random cover letter"
        f"Highlight how my skills and experiences match the job requirements, and emphasize why I am a worthy candidate for this position.\n\n"
        f"make sure the formatting is done correctly with all the names and double check that all the information like name address etc is propoerly included in the cover letter"
        f"Resume: blah blah blah"
        f"Job Description:blah blah blah"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    cover_letter_text = response.choices[0].message.content
    cover_letter_text = cover_letter_text.encode('utf-8', 'replace').decode('utf-8')
    print(cover_letter_text)

def openNewTab(driver, url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(5)


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



main1()
