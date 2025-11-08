import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# LinkedIn profile URLs
PROFILE_URLS = [
   "profile url 1",
    "profile url 2",
    "profile url 3",
    "profile url 4",
    "profile url 5", 
   "profile url 6 ", 
   "profile url 7", 
   "profile url 8", 
   "profile url 9", 
   "profile url 10"
]

# Your LinkedIn login details
EMAIL = "enter your email id"
PASSWORD = "your linkedin password which you use to login linkedin"

def login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    driver.find_element(By.ID, "username").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)

def get_profile_data(driver, url):
    driver.get(url)
    time.sleep(3)
    
    data = {"url": url}
    
    try:
        data["name"] = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text
    except:
        data["name"] = ""
    
    try:
        data["headline"] = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").text
    except:
        data["headline"] = ""
    
    try:
        data["location"] = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").text
    except:
        data["location"] = ""
    
    try:
        data["connections"] = driver.find_element(By.CSS_SELECTOR, "span.t-bold").text
    except:
        data["connections"] = ""
    
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(3)
    
    try:
        data["about"] = driver.find_element(By.CSS_SELECTOR, "div.display-flex.ph5.pv3 span[aria-hidden='true']").text
    except:
        data["about"] = ""
    
    try:
        data["experience"] = driver.find_element(By.CSS_SELECTOR, "#experience ~ div li div.display-flex.flex-column").text
    except:
        data["experience"] = ""
    
    try:
        data["education"] = driver.find_element(By.CSS_SELECTOR, "#education ~ div li").text
    except:
        data["education"] = ""
    
    return data


chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

login(driver)

profiles = []
for url in PROFILE_URLS:
    print(f"Scraping: {url}")
    profile = get_profile_data(driver, url)
    profiles.append(profile)
    time.sleep(5)

with open("linkedin_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["url", "name", "headline", "location", "connections", "about", "experience", "education"])
    writer.writeheader()
    writer.writerows(profiles)

print("Done! Data saved to linkedin_data.csv")
driver.quit()
