import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# ============================
# CONFIGURATION
# ============================

BASE_URL = "http://localhost:3000"
EMAIL = "demo123@gmail.com"
PASSWORD = "demo123"
TIMEOUT = 30


# ============================
# DRIVER SETUP
# ============================

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# ============================
# LOGIN TEST
# ============================

def login(driver, wait):
    print(f"[TEST] Logging in as {EMAIL}")

    driver.get(f"{BASE_URL}/login")

    wait.until(
        EC.presence_of_element_located((By.NAME, "email"))
    ).send_keys(EMAIL)

    driver.find_element(By.NAME, "password") \
        .send_keys(PASSWORD)

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )
    driver.execute_script("arguments[0].click();", login_btn)

    alert = wait.until(EC.alert_is_present())
    print("[INFO] Login alert:", alert.text)
    alert.accept()

    # Verify token
    wait.until(
        lambda d: d.execute_script(
            "return localStorage.getItem('token');"
        )
    )

    print("[PASS] Login successful, token detected")


# ============================
# ADD TO CART TEST
# ============================

def add_to_cart(driver, wait):
    print("[TEST] Adding book to cart")

    driver.get(BASE_URL)

    book_card = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "(//div[contains(@class,'card')])[1]")
        )
    )

    add_btn = book_card.find_element(
        By.XPATH,
        ".//button[contains(text(),'Add to Cart')]"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        add_btn
    )
    time.sleep(1)

    driver.execute_script("arguments[0].click();", add_btn)

    print("[PASS] Book added to cart")


# ============================
# CHECKOUT TEST
# ============================

def checkout_and_confirm(driver, wait):
    print("[TEST] Checkout flow")

    # Open cart
    cart_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'cart')]")
        )
    )
    driver.execute_script("arguments[0].click();", cart_btn)

    # Proceed to checkout
    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )
    driver.execute_script("arguments[0].click();", checkout_btn)

    # Verify checkout page
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Confirm Your Order')]")
        )
    )
    print("[PASS] Checkout page loaded")

    # Confirm purchase
    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "payment-button"))
    )
    driver.execute_script("arguments[0].click();", confirm_btn)

    alert = wait.until(EC.alert_is_present())
    print("[INFO] Purchase alert:", alert.text)
    alert.accept()

    # Verify redirect
    wait.until(EC.url_contains("/profile"))
    print("[PASS] Purchase completed successfully")


# ============================
# MAIN EXECUTION
# ============================

if __name__ == "__main__":

    driver = setup_driver()
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout_and_confirm(driver, wait)

        print("\n[SUCCESS] All Selenium tests passed")
        sys.exit(0)

    except Exception as e:
        driver.save_screenshot("tests/screenshots/test_failed.png")
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    finally:
        driver.quit()
