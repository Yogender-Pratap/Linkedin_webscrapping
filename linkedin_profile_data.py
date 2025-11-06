import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# LinkedIn profile URLs
PROFILE_URLS = [
   "https://www.linkedin.com/in/tarushi-khanna-02102001/",
    "https://www.linkedin.com/in/rayyanfarooq10/",
    "https://www.linkedin.com/in/ankit-sharma-87a7b81b0/",
    "https://www.linkedin.com/in/shubhanshu-dtu/",
    "https://www.linkedin.com/in/abinash1997/",
]

# Your LinkedIn login details
EMAIL = "y905078@gmail.com"
PASSWORD = "Yogender!#$123456"

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
