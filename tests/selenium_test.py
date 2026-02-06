import time
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# =====================================================
# CONFIGURATION
# =====================================================

BASE_URL = "http://localhost:3000"
EMAIL = "demo123@gmail.com"
PASSWORD = "demo123"

SCREENSHOT_DIR = os.path.join(
    os.path.dirname(__file__),
    "screenshots"
)

TIMEOUT = 25


# =====================================================
# SCREENSHOT HANDLER
# =====================================================

if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)


def take_screenshot(driver, name):
    """
    Saves a screenshot with a standardized name
    for Jenkins artifacts.
    """
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[INFO] Screenshot captured: {path}")


# =====================================================
# DRIVER SETUP
# =====================================================

def setup_driver():
    """
    Sets up Chrome for Headless execution
    (required for Jenkins/Docker).
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# =====================================================
# LOGIN TEST
# =====================================================

def login(driver, wait):
    print("[TEST] Starting Login Phase...")

    driver.get(f"{BASE_URL}/login")

    # Screenshot 01 - Login Page
    take_screenshot(driver, "01_login_page_loaded")

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

    # Screenshot 02 - Login Alert
    alert = wait.until(EC.alert_is_present())
    take_screenshot(driver, "02_login_alert_popup")
    alert.accept()

    # Verify JWT Token
    wait.until(
        lambda d: d.execute_script(
            "return localStorage.getItem('token');"
        )
    )

    print("[PASS] User authenticated successfully.")


# =====================================================
# ADD TO CART TEST
# =====================================================

def add_to_cart(driver, wait):
    print("[TEST] Starting Shop Phase...")

    driver.get(BASE_URL)

    # Screenshot 03 - Homepage Items
    take_screenshot(driver, "03_homepage_items_list")

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

    print("[PASS] Item added to cart.")


# =====================================================
# CHECKOUT TEST
# =====================================================

def checkout_and_confirm(driver, wait):
    print("[TEST] Starting Checkout Phase...")

    # Open Cart
    cart_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'cart')]")
        )
    )
    driver.execute_script("arguments[0].click();", cart_btn)

    # Screenshot 04 - Cart Modal
    take_screenshot(driver, "04_cart_modal_view")

    # Proceed to Checkout
    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )
    driver.execute_script("arguments[0].click();", checkout_btn)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(text(),'Confirm Your Order')]")
        )
    )

    # Screenshot 05 - Confirmation Page
    take_screenshot(driver, "05_order_confirmation_page")

    # Confirm Purchase
    confirm_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "payment-button"))
    )
    driver.execute_script("arguments[0].click();", confirm_btn)

    alert = wait.until(EC.alert_is_present())
    alert.accept()

    # Verify Redirect
    wait.until(EC.url_contains("/profile"))

    # Screenshot 06 - Profile Page
    take_screenshot(driver, "06_final_profile_redirect")

    print("[PASS] Transaction completed.")


# =====================================================
# MAIN EXECUTION
# =====================================================

if __name__ == "__main__":

    driver = setup_driver()
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout_and_confirm(driver, wait)

        print("\n[SUCCESS] All steps passed in CI/CD simulation.")
        sys.exit(0)

    except Exception as e:
        take_screenshot(driver, "DEBUG_FAIL_LOG")
        print(f"\n[ERROR] Test Interrupted: {e}")
        sys.exit(1)

    finally:
        driver.quit()
