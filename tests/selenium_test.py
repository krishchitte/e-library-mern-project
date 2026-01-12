import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def run_test():
    print("Starting Selenium Test (Python)...")

    # 1. Setup Chrome Options for Headless Mode (No GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except WebDriverException as e:
        print(f"Error initializing Chrome driver: {e}")
        print("Ensure you have Chrome and ChromeDriver installed.")
        sys.exit(1)

    try:
        # 2. Open the Website
        # We assume the app is running on localhost:3000 via Docker
        app_url = "http://localhost:3000"
        driver.get(app_url)
        print(f"Opened {app_url}")

        # 3. Wait slightly for the page to render
        time.sleep(2)

        # 4. Check the Title
        title = driver.title
        print(f"Page Title: {title}")

        # 5. Assertion Logic
        # Adjust "React" or your actual app title here
        if title: 
            print("✅ Test Passed: Website loaded and has a title.")
        else:
            print("❌ Test Failed: Page title is empty.")
            sys.exit(1) # Fail the pipeline

    except Exception as e:
        print(f"❌ An error occurred during the test: {e}")
        sys.exit(1) # Fail the pipeline
    finally:
        driver.quit()
        print("Test finished. Browser closed.")

if __name__ == "__main__":
    run_test()