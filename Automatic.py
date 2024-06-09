import os
import time
from datetime import datetime

import PyPDF2
import openai
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import customtkinter as ctk
from tkinter import filedialog, simpledialog, messagebox, Toplevel
import threading
import subprocess
import platform


ctk.set_appearance_mode("dark")  # Dark mode for the GUI
ctk.set_default_color_theme("dark-blue")  # Green theme


def start_automation(user_data, console_output, app, left_frame):
    username = user_data['username']
    password = user_data['password']
    start_date = user_data['start_date']
    resume_path = user_data['resume_path']
    base_path = user_data['base_path']

    folder_path = create_folder(base_path, console_output)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine")

    logIn(driver, username, password, console_output)
    openNewTab(driver, "https://shibboleth2.asu.edu"
                       "/idp/profile/SAML2/Unsolicited/"
                       "SSO?providerId=https%3A//sso.brassring.com"
                       "/sso/saml/SAML2PageListener/Authentication"
                       "Requestor.aspx%3FLocation%3D5495")
    time.sleep(10)
    advDisplay(driver, start_date)
    time.sleep(5)
    newJob(driver, folder_path, resume_path, console_output, app, left_frame)
    driver.quit()
def openNewTab(driver, url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
def logIn(driver, username, password, console_output):
    wait = WebDriverWait(driver, 10)
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
    console_output.insert("end", "Verify Duo Push\n")
    duo_push = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'auth-button') and contains(@class, 'positive')]")))
    duo_push.click()
    WebDriverWait(driver, 30).until(
        EC.url_contains("myasu")  # Check part of the URL that indicates the dashboard
    )
def advDisplay(driver, start_date):
    try:
        print(start_date)
        advSearch = driver.find_element(By.LINK_TEXT, "Advanced Search")
        advSearch.click()
        dateinput = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@class, 'datestring')]"))
        )
    except TimeoutError:
        # Take a screenshot if the element is not found
        driver.get_screenshot_as_file("screenshot.png")
        print("Screenshot taken as 'screenshot.png'")
        raise  # Optionally re-raise the exception for further handling
    except Exception as e:
        # Handle other exceptions and take a screenshot
        driver.get_screenshot_as_file("screenshot_error.png")
        print(f"Error: {str(e)}. Screenshot taken as 'screenshot_error.png'")
        raise  # Re-raise the exception if you want to handle it further up the stack


    dateinput.clear()
    dateinput.send_keys(start_date, Keys.ENTER)
def newJob(driver, folder_path, resume_path, console_output, app, left_frame):
    jobs_count = driver.find_elements(By.XPATH, "//li[contains(@class, 'job baseColorPalette ng-scope')]")

    console_output.insert("end", f"Found {len(jobs_count)} job listings.\n")

    for i in range(0,len(jobs_count)):  # Ensures we do not exceed the list length
        jobID = f"Job_{i}"
        try:
            link = driver.find_element(By.ID, jobID)
            jobName = link.text.strip()
            # Container frame for each job
            job_container = ctk.CTkFrame(master=left_frame)
            job_container.pack(fill='both', padx=20, pady=5)

            # Job name label
            job_label = ctk.CTkLabel(master=job_container, text=f"Job: {jobName}", font=('Courier', 12), anchor='w')
            job_label.pack(side='left', fill='x', expand=True)

            console_output.insert("end",f" Job: {jobName}", "\n")
            print(jobName)
            url1 = link.get_attribute("href")
            openNewTab(driver, url1)  # Ensure this method correctly handles tab management
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body")))  # Wait for the page to load

            warning_messages = driver.find_elements(By.CSS_SELECTOR, ".newMsgContainer.alreadyappliedJob.ng-scope")
            if warning_messages:
                console_output.insert("end", "\nYou have already applied for this job. No further action will be taken.\n")
                driver.close()  # Close the current tab
                driver.switch_to.window(driver.window_handles[1])  # Switch back to the main window
                time.sleep(2)
                continue  # Skip to the next job
            extractInfo(driver, jobName, folder_path, resume_path, console_output, app, left_frame, job_container)

        except Exception as e:
            console_output.insert("end", f"An error occurred for {jobID}: {e}")
            driver.close()  # Ensure to close the tab on error
            driver.switch_to.window(driver.window_handles[0])  # Always switch back to the main window
def extractInfo(driver, jobName, folder_path, resume_path, console_output, app, left_frame, job_container):
    # Dictionary to hold job details
    job_details = {}

    # Extract Job Description
    try:
        desc = driver.find_element(By.XPATH, "//p[@class='answer ng-scope jobdescriptionInJobDetails']")
        job_text = desc.text.strip()
        job_details["Description"] = job_text
    except Exception as e:
        console_output.insert("end", f"An error occurred while extracting job description: {e}")

        # Extract sections with the specified class name

    # Extract sections with the specified class name
    try:
        sections = driver.find_elements(By.XPATH,
                                        "//p[@class='answer ng-scope section2LeftfieldsInJobDetails jobDetailTextArea']")
        for index, section in enumerate(sections):
            section_text = section.text.strip()
            if index == 0:
                job_details["Grant Funded Position"] = section_text
            elif index == 1:
                job_details["Essential Duties"] = section_text
            elif index == 2:
                job_details["Minimum Qualifications"] = section_text
            elif index == 3:
                job_details["Desired Qualifications"] = section_text
    except Exception as e:
        print("end", f"An error occurred while extracting sections: {e}")

    job_text = "\n".join([f"{key}: {value}" for key, value in job_details.items()])

    pdf_path = resume_path  # Update with the correct path to your PDF file
    resume_text = extract_text_from_pdf(pdf_path)
    cover_letter = generate_cover_letter("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", job_text, resume_text)
    save_cover_letter(folder_path, jobName, cover_letter, console_output)
    print("\n Inside extract drivers info cover letter saved \n")
    finalize_cover_letter(driver, folder_path, jobName, console_output, resume_path, app, job_container)
    print("Cover letter finalised")
    # Close the current tab and switch back to the main tab
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
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
def generate_cover_letter(api_key, job_text, resume_text):
    try:
        openai.api_key = api_key
        current_date = datetime.now().strftime("%B %d, %Y")
        # Prepare the prompt in a conversational format
        prompt = (
            f"Today's date is {current_date}.\n\n"


            "Generate a professional cover letter for a job application."
            " Below are the details of the applicant and the job. "
            "Tailor the letter to highlight how the applicant's experiences and skills align with the job requirements,"
            "emphasizing why the applicant is an ideal candidate. Please format the letter correctly, ensuring it "
            "includes"
            "the applicant's personal information at the top, a formal greeting to the hiring manager, "
            "and an appropriate closing signature.\n\n"


            "Applicant's Resume:\n"
            f"{resume_text}\n\n"
            "Job Description:\n"
            f"{job_text}\n\n"
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        cover_letter_text = response.choices[0].message.content
        cover_letter_text = cover_letter_text.encode('utf-8', 'replace').decode('utf-8')
        return (cover_letter_text)
    except Exception as e:
        print(f"Cover Letter could not be generated due to: {str(e)}\n")
def create_folder(base_path, console_output):
    # Create a folder with today's date
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(base_path, current_date)
    print("\nFolder for " + current_date + " created.\n")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path
def save_cover_letter(folder_path, jobName, cover_letter, console_output):
    try:
        # Save the cover letter to a file
        pdf = FPDF()
        pdf.add_page()

        # Set font
        pdf.set_font("Arial", size=12)

        # Add a cell (this is a line in the PDF)
        pdf.multi_cell(0, 10, cover_letter)

        file_path = os.path.join(folder_path, f"{jobName}_CL.pdf")
        pdf.output(file_path)
    except Exception as e:
        print(f"Cover Letter could not be saved due to: {str(e)}\n")
def finalize_cover_letter(driver, folder_path, jobName, console_output, resume_path, app, job_container):
    # Event to control the flow, waiting for the user to click 'Apply'
    user_action = "pending"
    hyperlink_label = None
    apply_button = None
    cancel_button = None

    continue_event = threading.Event()
    cover_letter_path = os.path.join(folder_path, f"{jobName}_CL.pdf")
    def update_gui():
        nonlocal hyperlink_label, apply_button, cancel_button
        try:
                # Hyperlink to open the cover letter
                hyperlink_label = ctk.CTkLabel(master=job_container, text="Open Cover Letter", text_color="green",
                                               cursor="hand2", font=("Arial", 12, "underline"))
                hyperlink_label.pack(side='left', padx=10)
                hyperlink_label.bind("<Button-1>", open_cover_letter)

                # Apply button
                apply_button = ctk.CTkButton(master=job_container, text="Apply",
                                             command=lambda: on_apply())
                apply_button.pack(side='right')

                cancel_button = ctk.CTkButton(master=job_container, text="Cancel",
                                              command=on_cancel, fg_color='red', hover_color='dark red')
                cancel_button.pack(side='right', padx=10)

        except Exception as e:
            console_output.insert("end", f"Error setting up job application GUI: {str(e)}\n")


    def remove_specific_widgets():
        # Remove only specific widgets
        hyperlink_label.pack_forget()
        apply_button.pack_forget()
        cancel_button.pack_forget()
    def open_cover_letter(event=None):
        if platform.system() == "Windows":
            subprocess.run(["start", cover_letter_path], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", cover_letter_path])
        else:  # Linux
            subprocess.run(["xdg-open", cover_letter_path])

    def display_result(text, color):
        result_label = ctk.CTkLabel(master=job_container, text=text, text_color=color, font=('Courier', 12, 'bold'))
        result_label.pack(side= 'right', pady=0, padx= 5)

    def on_apply():
        nonlocal user_action
        user_action = "apply"
        console_output.insert("end", f"\nApplying to job: {jobName}.\n")
        remove_specific_widgets()
        display_result("APPLIED", "green")
        continue_event.set()
    def on_cancel():
        nonlocal user_action
        user_action = "cancel"
        console_output.insert("end", f"\nApplication cancelled for {jobName}.\n")
        remove_specific_widgets()
        display_result("CANCELLED", "red")
        continue_event.set()  # Resume execution to move to the next job

    app.after(0, update_gui)
    continue_event.wait()  # Wait for user action before proceeding
    if user_action == "apply":
        apply_to_job(driver, jobName, folder_path, resume_path)
        console_output.insert("end", f"\nSuccesfully applied to job: {jobName}\n")
    elif user_action == "cancel":
        console_output.insert("end", f"Moving to next job.\n")
        # Here you would move to the next job; implementation depends on your job loop/control flow


def apply_to_job(driver, jobName, folder_path, resume_path):
    print(f"Applying to the job: {jobName}")
    wait = wait = WebDriverWait(driver, 10)
    try:
        # Click the apply button
        apply_button = wait.until(EC.element_to_be_clickable((By.ID, "applyFromDetailBtn")))
        apply_button.click()

        # Click the get started button
        get_started = wait.until(EC.element_to_be_clickable((By.ID, "startapply")))
        get_started.click()

        # Click the save and continue button
        save_continue1 = wait.until(EC.element_to_be_clickable((By.ID, "shownext")))
        save_continue1.click()

        # Handle radio buttons interaction
        radio1 = wait.until(EC.element_to_be_clickable((By.ID, "radio-44674-No")))
        radio1.click()
        radio2 = wait.until(EC.element_to_be_clickable((By.ID, "radio-45523-Yes")))
        radio2.click()
        radio3 = wait.until(EC.element_to_be_clickable((By.ID, "radio-45534-Yes")))
        radio3.click()
        radio4 = wait.until(EC.element_to_be_clickable((By.ID, "radio-61829-No")))
        radio4.click()

        # Select the dropdown option
        dropdown = wait.until(EC.element_to_be_clickable((By.ID, "custom_44925_1291_fname_slt_0_44925-button_text")))
        dropdown.click()
        time.sleep(2)
        options = driver.find_elements(By.XPATH, "//li[contains(@class, 'ui-menu-item')]")
        for option in options:
            if option.get_attribute("aria-label") == "Searching ASU Website":
                option.click()
                break
        time.sleep(3)
        save_continue2 = driver.find_element(By.ID, "shownext")
        save_continue2.click()
        time.sleep(5)

        # Adding resume
        add_resume_link = driver.find_element(By.ID, "AddResumeLink")
        add_resume_link.click()
        time.sleep(3)

        # Switch to the iframe for the resume upload
        iframe = driver.find_element(By.ID, "profileBuilder")
        driver.switch_to.frame(iframe)
        time.sleep(1)

        # Find the input for the resume file and upload the file
        browse_resume = driver.find_element(By.ID, "file")
        file_path_resume = resume_path
        browse_resume.send_keys(file_path_resume)
        time.sleep(5)
        # Switch back to the main document before proceeding to upload the cover letter
        driver.switch_to.default_content()

        # uploading cover letter
        add_cover_letter_link = driver.find_element(By.ID, "AddCLLink")
        add_cover_letter_link.click()
        time.sleep(3)
        iframe = driver.find_element(By.ID, "profileBuilder")
        driver.switch_to.frame(iframe)
        time.sleep(1)

        # Find the input for the cover letter file and upload the file
        browse_cover_letter = driver.find_element(By.ID, "file")  # This may need to be adjusted if the input ID differs
        cover_letter_path = os.path.join(folder_path, f"{jobName}_CL.pdf")
        browse_cover_letter.send_keys(cover_letter_path)
        time.sleep(5)

        # Switch back to the main content after uploading the cover letter
        driver.switch_to.default_content()

        # going next page
        save_continue3 = driver.find_element(By.ID, "shownext")
        save_continue3.click()
        time.sleep(3)

        # going next page
        save_continue4 = driver.find_element(By.ID, "shownext")
        save_continue4.click()
        time.sleep(3)

        # going next page
        save_continue5 = driver.find_element(By.ID, "shownext")
        save_continue5.click()
        time.sleep(3)

        # going next page
        save_continue6 = driver.find_element(By.ID, "shownext")
        save_continue6.click()
        time.sleep(3)

        # going next page
        save_continue7 = driver.find_element(By.ID, "shownext")
        save_continue7.click()
        time.sleep(3)

        apply = driver.find_element(By.ID, "save")
        apply.click()
        time.sleep(3)

    except Exception as e:
        print(f"Failed to apply to the job: {jobName} due to {e}")
def open_file(path):
    """ Open file in default system application. """
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    else:  # Linux
        subprocess.run(["xdg-open", path])

def start_login_gui():
    app = ctk.CTk()

    app.title("ASU JOB APPLICATION TOOL")
    app.config(bg='white')  # Reset background color for main GUI


    app.geometry("1200x675")
    app.title("ASU JOB APPLICATION TOOL")

    # Define the frames
    global left_frame
    left_frame = ctk.CTkFrame(master=app, width=300, height=400)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = ctk.CTkFrame(master=app, width=900, height=400)
    right_frame.pack(side="right", fill="both", expand=True)

    # Console output on the right
    console_output = ctk.CTkTextbox(master=right_frame, font=('Courier', 14, 'normal'), spacing3=7)
    console_output.pack(pady=20, padx=20, fill="both", expand=True)

    # Inner frame for centralized content in the left frame
    inner_frame = ctk.CTkFrame(master=left_frame)
    inner_frame.pack(expand=True)

    # Entry for username
    username_entry = ctk.CTkEntry(master=inner_frame, placeholder_text="Username", font=('Courier', 14), width=250)
    username_entry.pack(pady=20, padx=20, expand=True)

    # Entry for password
    password_entry = ctk.CTkEntry(master=inner_frame, placeholder_text="Password", show="*", font=('Courier', 14), width=250)
    password_entry.pack(pady=20, padx=20, expand=True)

    def choose_file():
        global resume_path
        filename = filedialog.askopenfilename(initialdir="/", title="Select Resume File",
                                              filetypes=(("PDF files", "*.pdf"), ("All files", "*.*")))
        if filename:
            resume_path = filename  # Update the global resume_path
            console_output.insert("end", f"Resume Selected: {resume_path}\n")
        else:
            console_output.insert("end", f"! ! ! No Resume Selected ! ! !\n")


    def choose_directory():
        global base_path
        directory = filedialog.askdirectory()  # Open a dialog to choose a directory
        if directory:
            base_path = directory  # Set the base_path to the selected directory
            console_output.insert("end", f"Saving Cover Letters to: {base_path}\n")
        else:
            console_output.insert("end", f"! ! ! No Directory Selected ! ! !\n")


    file_button = ctk.CTkButton(master=inner_frame, text="Select Resume File", command=choose_file,
                                font=('Courier', 12))
    file_button.pack(pady=20)

    directory_button = ctk.CTkButton(master=inner_frame, text="Select Directory", command=choose_directory,
                                     font=('Courier', 12))
    directory_button.pack(pady=20)  # Make sure to pack this button as well

    date_entry = ctk.CTkEntry(master=inner_frame, placeholder_text="Start Date (MM/DD/YYYY)", font=('Courier', 14), width=250)
    date_entry.pack(pady=20, padx=20)



    def on_continue():
        global resume_path
        global base_path
        user_details = {
            "username": username_entry.get(),
            "password": password_entry.get(),
            "start_date": date_entry.get(),
            "resume_path": resume_path,
            "base_path": base_path
        }
        console_output.insert("end", f"Searching for jobs posted since: {date_entry.get()} \n")
        try:
            thread = threading.Thread(target=start_automation, args=(user_details, console_output, app, left_frame))
        except:
            print("fiefe")
        thread.start()
        clear_frame(left_frame)
        create_status_view(left_frame)

    continue_button = ctk.CTkButton(master=left_frame, text="Continue", command=on_continue, font=('Courier', 12), text_color='white')
    continue_button.pack(pady=20, padx=20)

    app.mainloop()


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_status_view(frame):
    status_label = ctk.CTkLabel(master=frame, text="STATUS", font=('Courier', 24, 'bold'), text_color='green')
    status_label.pack(pady=10, padx=20, anchor='w')


if __name__ == "__main__":
    start_login_gui()