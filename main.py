from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from time import sleep
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists

def launchBrowser():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/jobs/search/?f_AL=true&geoId=105001681&keywords=python%20developer&location=Wroc%C5%82aw%2C%20Woj.%20Dolno%C5%9Bl%C4%85skie%2C%20Polska")
    return driver

driver = launchBrowser()
sleep(5)

# Deny cookies:
try:
    driver.find_element(By.CSS_SELECTOR, "#artdeco-global-alert-container > div > section > div > div.artdeco-global-alert-action__wrapper > button:nth-child(2)").click()
except Exception as e:
    print(f"Something went wrong during cookie management: {e}")

# Login:
try:
    driver.find_element(By.CSS_SELECTOR, "body > div.base-serp-page > header > nav > div > a.nav__button-secondary").click()
    sleep(5)
    # type username
    driver.find_element(By.ID, "username").send_keys("xx")
    # type password
    driver.find_element(By.ID, "password").send_keys("xx")

    #click login
    print()
    driver.find_element(By.CSS_SELECTOR, "#organic-div > form > div.login__form_action_container > button").click()
except Exception as e:
    print(f"Something went wrong during Login page click: {e}")

sleep(5)

pages = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator")
pages_number = driver.find_element(By.CSS_SELECTOR, f"#{pages[-1].get_attribute('id')} > button span").text
print(pages_number)

# save job loop
for page in range(int(pages_number)):
    print(f"Go to page: {page + 1}")
    pages = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator")
    driver.find_element(By.CSS_SELECTOR, f"#{pages[page].get_attribute('id')} > button").click()
    sleep(1)
    jobs = []
    try:
        jobs = driver.find_elements(By.CLASS_NAME, "job-card-container--clickable")
    except Exception as e:
        print(f"Something went wrong during jobs lists creation: {e}")
    else:
        for job in jobs:
            try:
                job.click()
                sleep(1)
                save_button = driver.find_element(By.CLASS_NAME, "jobs-save-button")
                save_button_text = driver.find_element(By.CSS_SELECTOR, ".jobs-save-button > span.a11y-text").text

                if "Zapisz" in save_button_text:
                    print(save_button_text)
                    save_button.click()
                    sleep(1)

                # disable notofication
                try:
                    driver.find_element(By.CLASS_NAME, "artdeco-toast-item__dismiss").click()
                except exceptions.NoSuchElementException:
                    pass
                except Exception as e:
                    print(f"Error when disabling notification: {e}")
                sleep(1)
            except Exception as e:
                print(f"Something went wrong when saving the job: {e}")