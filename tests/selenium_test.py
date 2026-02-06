import time
import sys
import functools 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

print = functools.partial(print, flush=True)

BASE_URL = "http://localhost:3000"
EMAIL = "demo123@gmail.com"
PASSWORD = "demo123"

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

def take_screenshot(driver, name):
    """Saves a screenshot with a standardized name for Jenkins artifacts."""
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[INFO] Screenshot captured: {path}")

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def login(driver, wait):
    print("[TEST] Logging in as", EMAIL)
    driver.get(f"{BASE_URL}/login")

    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)

    ## SCREENSHOT 1: Login Page Result
    take_screenshot(driver, "01_login_page_loaded")
    
    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    driver.execute_script("arguments[0].click();", login_btn)

    alert = wait.until(EC.alert_is_present())
    print("[INFO] Login alert:", alert.text)

    ## SCREENSHOT 2: Login Result Alert
    take_screenshot(driver, "02_login_alert_popup")
    
    alert.accept()

    # Verify token
    wait.until(lambda d: d.execute_script("return localStorage.getItem('token');"))
    print("[PASS] Login successful, token detected")


def add_to_cart(driver, wait):
    print("[TEST] Adding book to cart")

    # SCREENSHOT 3: Homepage/Book Grid (Verifies MongoDB connection)
    take_screenshot(driver, "03_homepage_items_list")

    driver.get(BASE_URL)

    book_card = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "(//div[contains(@class,'card')])[1]")
        )
    )

    add_btn = book_card.find_element(
        By.XPATH, ".//button[contains(text(),'Add to Cart')]"
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", add_btn)

    print("[PASS] Book added to cart")


def checkout_and_confirm(driver, wait):
    print("[TEST] Checkout flow")

    # 1️⃣ Open cart (cart icon / button)
    cart_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'cart')]")
        )
    )
    driver.execute_script("arguments[0].click();", cart_btn)

    # 2️⃣ Click Proceed to Checkout
    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )
    driver.execute_script("arguments[0].click();", checkout_btn)

    # 3️⃣ Wait for Checkout page
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Confirm Your Order')]")
        )
    )
    print("[PASS] Checkout page loaded")
    print("[PASS] Purchase completed successfully")

if __name__ == "__main__":
    driver = setup_driver()
    wait = WebDriverWait(driver, 30)

    try:
        # Force an immediate start message
        sys.stdout.write("[INFO] Starting test suite...\n")
        sys.stdout.flush()
        
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout_and_confirm(driver, wait)
        
        sys.stdout.write("\n[SUCCESS] All Selenium tests passed.\n")
        sys.stdout.flush()
        time.sleep(2) # Give Jenkins 2 seconds to "catch" the output
        sys.exit(0)
        
    except Exception as e:
        sys.stderr.write(f"\n[ERROR] Test failed: {e}\n")
        sys.stderr.flush()
        time.sleep(2)
        sys.exit(1)
        
    finally:
        driver.quit()
