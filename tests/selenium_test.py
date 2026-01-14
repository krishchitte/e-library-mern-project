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

# =========================
# CONFIGURATION
# =========================
BASE_URL = "http://localhost:3000"
LOGIN_URL = f"{BASE_URL}/login"
CART_URL = f"{BASE_URL}/cart"

USER_EMAIL = "krish.v.chitte@gmail.com"
USER_PASSWORD = "Krish@123"

SCREENSHOT_DIR = "tests/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# =========================
# DRIVER SETUP
# =========================
def setup_driver():
    options = Options()

    # Headless Chrome for Jenkins
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Stable User Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver


# =========================
# UTILITY HELPERS
# =========================
def take_screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[DEBUG] Screenshot saved: {path}")


def wait_for_token(driver, timeout=20):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script(
            "return window.localStorage.getItem('token') !== null"
        )
    )


# =========================
# TEST STEPS
# =========================
def login(driver, wait):
    print(f"[TEST] Logging in as {USER_EMAIL}")

    driver.get(LOGIN_URL)

    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)

    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log In')]"))
    )
    driver.execute_script("arguments[0].click();", login_btn)

    # Verify token exists (REAL LOGIN CHECK)
    wait_for_token(driver)

    if "/login" in driver.current_url:
        take_screenshot(driver, "login_failed")
        raise Exception("Login failed — still on login page")

    print("[PASS] Login successful")


def add_to_cart(driver, wait):
    print("[TEST] Adding book to cart")

    driver.get(BASE_URL)

    book_card = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "book-card"))
    )

    add_btn = book_card.find_element(
        By.XPATH, ".//button[contains(text(),'Add to Cart')]"
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
    driver.execute_script("arguments[0].click();", add_btn)

    print("[PASS] Add to Cart clicked")


def checkout(driver, wait):
    print("[TEST] Checking out")

    driver.get(CART_URL)

    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", checkout_btn)
    driver.execute_script("arguments[0].click();", checkout_btn)

    print("[PASS] Checkout initiated")


# =========================
# MAIN TEST RUNNER
# =========================
def run_tests(driver):
    wait = WebDriverWait(driver, 25)

    login(driver, wait)
    add_to_cart(driver, wait)
    checkout(driver, wait)


if __name__ == "__main__":
    driver = setup_driver()

    try:
        run_tests(driver)
        print("\n[SUCCESS] All Selenium tests passed")
        sys.exit(0)

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        take_screenshot(driver, "fatal_error")
        sys.exit(1)

    finally:
        driver.quit()
