from selenium import webdriver
import json


def save_cookies():
    # Start a browser
    driver = webdriver.Chrome()

    # Wait for user
    input("Press Enter when you're ready to save cookies!")

    # Save cookies
    with open("cookies.json", "w") as f:
        json.dump(
            driver.get_cookies(),
            f
        )


def load_saved_cookies(driver):
    with open("cookies.json", "r") as f:
        cookies = json.load(f)

    for cookie in cookies:
        driver.add_cookie(cookie)


if __name__ == '__main__':
    save_cookies()

    with open("cookies.json", "rb") as f:
        cookies = json.load(f)
