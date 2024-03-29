### COVIDPass Auto-Attestation

from selenium import webdriver
import getpass
import time
import os
import pyautogui as pg
import threading
from pathlib import Path
from pushbullet import pushbullet_message

pg.FAILSAFE=False

try:  # Wrap the whole thing in a try-except block and send a text notification if something goes wrong
    this_dir = Path(__file__).parent.absolute()  # Get the current directory

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
        os.system('taskkill /F /IM "chrome.exe" /T')
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

    ### Set up a thread to click enter to authenticate certificate
    cert_button_image_files = [
        this_dir / "images" / "ok_button_pi.png",
        this_dir / "images" / "ok_button_win.png"
    ]
    cert_button_image_files = [str(x) for x in cert_button_image_files]


    def click_certificate_authentication_button(timeout=30):
        start_time = time.time()
        iter = 0
        while time.time() < start_time + timeout:  # For the next x seconds, click all "Ok" buttons that appear
            for image_file in cert_button_image_files:
                button_location = pg.locateCenterOnScreen(image_file)
                if button_location is not None:
                    print("(Background thread): Found certificate authentication button, clicking it...")
                    pg.click(button_location)
                    return
            pause()
            iter += 1
            print(f"(Background thread): Did not see a certificate authentication button in iteration {iter}.")


    print("Prepping to authenticate certificate in separate thread...")
    thread = threading.Thread(target=click_certificate_authentication_button)
    thread.start()

    ### With main thread, open COVIDPass
    print("Opening COVIDPass in main thread...")
    driver = webdriver.Chrome(options=options)
    driver.get("https://covidpass.mit.edu")
    pause()

    ### Open Attestation page
    pause()
    print("Finding and clicking attestation button...")
    buttons = driver.find_elements_by_class_name("nav-item")
    attestation_button = None  # Next few lines: identify the attestation button on the webpage
    for button in buttons:
        if button.text == "Attestation":
            attestation_button = button
            break
    if attestation_button is None:
        raise Exception("Attestation Button not found! Likely because you need to Duo Auth again...")

    attestation_button.click()
    pause()


    def find_button_by_text(text: str):  # Returns the first button on the current page with the given text on it.
        for button in driver.find_elements_by_class_name("btn"):
            if button.text == text:
                return button
        raise ValueError(f"No button found with the text '{text}'")

    ### Attest
    print("Attesting...")
    checkboxes_with_yes = driver.find_elements_by_link_text("Yes")
    checkboxes_with_no = driver.find_elements_by_link_text("No")
    checkboxes_with_no[0].click()
    checkboxes_with_no[1].click()
    checkboxes_with_yes[2].click()
    find_button_by_text("Submit").click()
    pause()

    ### Confirm
    found_confirmation = False
    for popup in driver.find_elements_by_class_name("loadedContent"):
        if "You will be submitting that you do not exhibit symptoms" in popup.text:
            found_confirmation=True
            break

    if found_confirmation:
        find_button_by_text("Yes, I'm sure").click()
        pause()
    else:
        raise Exception("Couldn't find confirmation text!")

    ### Shut down
    print("Shutting down driver...")
    driver.close()

    print("Joining threads...")
    thread.join()

    print("Success!")

    # pushbullet_message("AutoCovidPass", "Success!")

except Exception as e:

    print(f"Exception occurred, sending text. Exception:\n{e}")

    pushbullet_message("AutoCovidPass", f"Error: {e}")
