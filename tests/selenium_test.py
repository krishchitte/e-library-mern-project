import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:3000"
EMAIL = "demo123@gmail.com"
PASSWORD = "demo123"


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

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )
    driver.execute_script("arguments[0].click();", login_btn)

    alert = wait.until(EC.alert_is_present())
    print("[INFO] Login alert text:", alert.text)
    alert.accept()

    time.sleep(2)

    token = driver.execute_script("return localStorage.getItem('token');")
    if not token:
        raise Exception("Token not set after login")

    print("[PASS] Login successful, token detected")


def add_to_cart(driver, wait):
    print("[TEST] Adding book to cart")

    driver.get(BASE_URL)

    # wait for books to load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "books")))

    add_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Add to Cart')]")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
    driver.execute_script("arguments[0].click();", add_btn)

    alert = wait.until(EC.alert_is_present())
    print("[INFO] Add-to-cart alert:", alert.text)
    alert.accept()

    print("[PASS] Book added to cart")


def checkout_and_buy(driver, wait):
    print("[TEST] Checkout and purchase")

    # Open cart by clicking cart icon/button
    cart_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'cart')]")
        )
    )
    driver.execute_script("arguments[0].click();", cart_btn)

    # Proceed to checkout
    checkout_btn = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "checkout-btn")
        )
    )
    driver.execute_script("arguments[0].click();", checkout_btn)

    # Confirm purchase
    confirm_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Confirm Purchase')]")
        )
    )
    driver.execute_script("arguments[0].click();", confirm_btn)

    alert = wait.until(EC.alert_is_present())
    print("[INFO] Checkout alert:", alert.text)
    alert.accept()

    print("[PASS] Purchase completed successfully")


if __name__ == "__main__":
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout_and_buy(driver, wait)

        print("\n[SUCCESS] All Selenium tests passed")

    except Exception as e:
        print("\n[ERROR]", e)
        sys.exit(1)

    finally:
        driver.quit()
