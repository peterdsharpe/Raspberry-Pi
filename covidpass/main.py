### COVIDPass Auto-Attestation

from selenium import webdriver
import getpass
import time
import os
import pyautogui as pg

pause = lambda: time.sleep(3)  # Add a small pause at times to let elements load

### Print the current date and time to the log file
from datetime import datetime

print("CovidPass Automation")
print(f"Log file from run at: {datetime.now()}")

### Set up user profile
print("Setting up user profile...")
options = webdriver.ChromeOptions()
username = getpass.getuser()
if username == "User":
    import chromedriver_autoinstaller as ca

    ca.install()
    user_data_dir = rf"{os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data"
elif username == "pi":
    os.system("pkill chromium")
    user_data_dir = "/home/pi/.config/chromium"
else:
    raise RuntimeError("Unknown user!")

options.add_argument(
    rf"user-data-dir={user_data_dir}"
)


### Open COVIDPass
print("Opening COVIDPass...")
driver = webdriver.Chrome(options=options)
driver.get("https://covidpass.mit.edu")
pause()

# ### Load cookies
# pause()
# load_saved_cookies(driver)
# pause()
# driver.refresh()
# pause()
#
# ### Login
# username_box = driver.find_element_by_name("j_username")
# password_box = driver.find_element_by_name("j_password")
# username_box.send_keys("pds")
# password_box.send_keys("")
# submit_button = driver.find_element_by_name("Submit")
# submit_button.click()
# pause()
#
# ### Duo Auth
# checkbox = driver.find_element_by_css_selector("input")
# push_button = driver.find_element_by_("push-label")

### Open Attestation page
print("Finding and clicking attestation button...")
buttons = driver.find_elements_by_class_name("nav-item")
attestation_button = None  # Next few lines: identify the attestation button on the webpage
for button in buttons:
    if button.text == "Attestation":
        attestation_button = button
        break
attestation_button.click()
pause()


def find_button_by_text(text: str):  # Returns the first button on the current page with the given text on it.
    for button in driver.find_elements_by_class_name("btn"):
        if button.text == text:
            return button
    raise ValueError(f"No button found with the text '{text}'")


### Attest, Page 1
print("Attesting page 1...")
checkboxes_with_yes = driver.find_elements_by_link_text("Yes")
checkboxes_with_no = driver.find_elements_by_link_text("No")
for no_symptom_answer in checkboxes_with_no:
    no_symptom_answer.click()
find_button_by_text("Continue").click()
pause()

### Attest, Page 2
print("Attesting page 2...")
checkboxes_with_yes = driver.find_elements_by_link_text("Yes")
checkboxes_with_no = driver.find_elements_by_link_text("No")
checkboxes_with_no[0].click()
checkboxes_with_no[1].click()
checkboxes_with_yes[2].click()
checkboxes_with_yes[3].click()
find_button_by_text("Submit").click()
pause()

### Shut down
print("Shutting down...")
driver.close()

