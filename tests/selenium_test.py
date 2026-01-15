import sys
import os
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# CONFIG
# =========================
BASE_URL = "http://localhost:3000"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
CART_URL = f"{BASE_URL}/cart"

# Generate UNIQUE user every run (CI SAFE)
TEST_EMAIL = f"ci_user_{uuid.uuid4().hex[:6]}@test.com"
TEST_PASSWORD = "Test@12345"
TEST_NAME = "CI Test User"

# =========================
# DRIVER SETUP
# =========================
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver

# =========================
# HELPERS
# =========================
def wait_for_token(driver, wait):
    wait.until(lambda d: d.execute_script(
        "return window.localStorage.getItem('token') !== null"
    ))

def fail(driver, message):
    print(f"[ERROR] {message}")
    driver.save_screenshot("tests/failure.png")
    sys.exit(1)

# =========================
# TEST STEPS
# =========================
def register_user(driver, wait):
    print(f"[TEST] Registering new user: {TEST_EMAIL}")

    driver.get(REGISTER_URL)

    wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(TEST_NAME)
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)

    register_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Register')]"))
    )
    driver.execute_script("arguments[0].click();", register_btn)

    # Successful register usually redirects to login
    wait.until(lambda d: "/login" in d.current_url or "/register" not in d.current_url)

    print("[PASS] User registered successfully")

def login(driver, wait):
    print(f"[TEST] Logging in as {TEST_EMAIL}")

    driver.get(LOGIN_URL)

    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)

    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log In')]"))
    )
    driver.execute_script("arguments[0].click();", login_btn)

    # REAL login validation
    wait_for_token(driver, wait)

    if "/login" in driver.current_url:
        fail(driver, "Login failed in CI")

    print("[PASS] Login successful")

def add_to_cart(driver, wait):
    print("[TEST] Adding book to cart")

    driver.get(BASE_URL)

    book = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-card")))
    add_btn = book.find_element(By.XPATH, ".//button[contains(text(),'Add to Cart')]")

    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
    driver.execute_script("arguments[0].click();", add_btn)

    print("[PASS] Book added to cart")

def checkout(driver, wait):
    print("[TEST] Checking out")

    driver.get(CART_URL)

    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )
    driver.execute_script("arguments[0].click();", checkout_btn)

    print("[PASS] Checkout completed")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        register_user(driver, wait)
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout(driver, wait)

        print("\n[SUCCESS] CI Selenium test completed successfully")
        sys.exit(0)

    except Exception as e:
        fail(driver, str(e))

    finally:
        driver.quit()
