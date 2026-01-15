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
# CONFIG (MATCHES YOUR APP)
# =========================
BASE_URL = "http://localhost:3000"
LOGIN_URL = f"{BASE_URL}/login"
CART_URL = f"{BASE_URL}/cart"

EMAIL = "demo123@gmail.com"
PASSWORD = "demo123"

SCREENSHOT_DIR = "tests/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

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
def screenshot(driver, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    print(f"[DEBUG] Screenshot saved: {path}")

def wait_for_token(driver, wait):
    wait.until(lambda d: d.execute_script(
        "return window.localStorage.getItem('token') !== null"
    ))

# =========================
# TEST STEPS
# =========================
def login(driver, wait):
    print(f"[TEST] Logging in as {EMAIL}")

    driver.get(LOGIN_URL)

    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)

    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log In')]"))
    )
    driver.execute_script("arguments[0].click();", login_btn)

    # CRITICAL: Handle alert (your app depends on it)
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"[INFO] Login alert text: {alert.text}")
        alert.accept()
    except:
        raise Exception("Login alert did not appear")

    #  Now wait for token AFTER alert is accepted
    try:
        wait.until(lambda d: d.execute_script(
            "return window.localStorage.getItem('token') !== null"
        ))
    except:
        driver.save_screenshot("tests/screenshots/token_missing.png")
        raise Exception("Token not set after login")

    print("[PASS] Login successful, token detected")

def checkout(driver, wait):
    print("[TEST] Checkout")

    driver.get(CART_URL)

    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn"))
    )

    driver.execute_script("arguments[0].click();", checkout_btn)
    print("[PASS] Checkout clicked")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout(driver, wait)

        print("\n[SUCCESS] Selenium test completed successfully")
        sys.exit(0)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    finally:
        driver.quit()
