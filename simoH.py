from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os  


Country_ToDo = ["germany", "france", "luxembourg", "belgium", "switzerland", "italy", "spain", "norway", "sweden", "united-kingdom" "turkey", "portugal", "poland", "ireland", "iceland", "hungary", "greece", "finland", "czechia", "algeria", "albania", "australia", "china", "cote-divoire", "denmark", "hong-kong", "india", "japan", "south-korea", "monaco", "croatia" "qatar", "the-united-states-of-america", "the-russian-federation", "singapore"]


year = 2024

baseUrl ="https://datareportal.com/reports/digital-" + year + "-"


def getUrls(baseUrl, countryName):

    url = baseUrl + countryName

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    iframe_src = iframe.get_attribute("src")
    driver.quit()
    
    return iframe_src

def take_screenshot(url, country):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    directory_name = f"{country}_data"
    os.makedirs(directory_name, exist_ok=True)  # Create the directory if it doesn't exist

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(8)

        try:
            reject_button = driver.find_element(By.ID, "btn-reject")
            reject_button.click()
        except:
            print("No reject button found")
        print("url: ", url)
        first_file_name = os.path.join(directory_name, f"{country}_data_1.png")
        driver.save_screenshot(first_file_name)
        print(f"First screenshot saved as '{first_file_name}'")

        pointers = driver.find_elements(By.CLASS_NAME, "pointer")
        if len(pointers) >= 1:
            pointers[0].click()

        i = 0
        for i in range(12):
            pointers = driver.find_elements(By.CLASS_NAME, "pointer")
            pointers[1].click()
            i += 1
        time.sleep(1)

        second_file_name = os.path.join(directory_name, f"{country}_data_2.png")
        driver.save_screenshot(second_file_name)
        print(f"Second screenshot saved as '{second_file_name}'")

        try:
            j = 0
            for j in range(200):
                pointers = driver.find_elements(By.CLASS_NAME, "pointer")
                pointers[1].click()
                j += 1
                time.sleep(2)
                screenshot_name = os.path.join(directory_name, f"{country}_data_{j}.png")
                driver.save_screenshot(screenshot_name)
                print(f"Screenshot saved as '{screenshot_name}'")
                time.sleep(3)
                
        except:
            print("No more screenshots to take")

    finally:
        driver.quit()


for country in Country_ToDo:
    url = getUrls(baseUrl, country)
    take_screenshot(url, country)


