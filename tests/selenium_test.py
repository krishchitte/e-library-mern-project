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
    time.sleep(3)

    try:
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

        print("[PASS] Add to cart clicked")

    except Exception as e:
        driver.save_screenshot("tests/screenshots/add_to_cart_failed.png")
        raise Exception("Add to Cart failed") from e

def checkout_from_cart(driver, wait):
    print("[TEST] Proceeding to checkout")

    try:
        checkout_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "checkout-btn")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", checkout_btn
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", checkout_btn)

        # 🔑 WAIT FOR CART OVERLAY TO DISAPPEAR
        wait.until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "cart-overlay")
            )
        )

        # 🔑 THEN wait for checkout page
        wait.until(EC.url_contains("/checkout"))

        print("[PASS] Navigated to checkout page")

    except Exception as e:
        driver.save_screenshot("tests/screenshots/checkout_failed.png")
        raise Exception("Checkout failed") from e

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

def confirm_purchase(driver, wait):
    print("[TEST] Confirming purchase")

    try:
        confirm_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "payment-button")
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", confirm_btn
        )
        time.sleep(1)
        driver.execute_script("arguments[0].click();", confirm_btn)

        alert = wait.until(EC.alert_is_present())
        print("[INFO] Purchase alert:", alert.text)
        alert.accept()

        wait.until(EC.url_contains("/profile"))
        print("[PASS] Purchase completed successfully")

    except Exception as e:
        driver.save_screenshot("tests/screenshots/confirm_purchase_failed.png")
        raise Exception("Confirm purchase failed") from e


if __name__ == "__main__":
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)

    try:
        login(driver, wait)
        add_to_cart(driver, wait)
        checkout_from_cart(driver, wait)
        confirm_purchase(driver, wait)

        print("\n[SUCCESS] All Selenium tests passed")
        sys.exit(0)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    finally:
        driver.quit()
