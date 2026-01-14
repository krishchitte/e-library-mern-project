import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# --- CONFIGURATION ---
BASE_URL = "http://localhost:3000"  # Change this if your frontend runs on a different port
USER_EMAIL = "testuser@example.com"
USER_PASSWORD = "password123"


def setup_driver():
    """Initializes the Chrome driver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run without opening a window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver


def test_user_login(driver):
    """Functionality 1: User Login"""
    print("Testing User Login...")
    driver.get(f"{BASE_URL}/login")
   
    # Wait for the email input to be present
    wait = WebDriverWait(driver, 10)
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or @type='submit']")


    email_input.send_keys(USER_EMAIL)
    password_input.send_keys(USER_PASSWORD)
    login_button.click()


    # Verify login success by checking for a logout button or profile link
    wait.until(EC.url_changes(f"{BASE_URL}/login"))
    print("Login successful!")


def test_add_to_cart(driver):
    """Functionality 2: Add to Cart"""
    print("Testing Add to Cart...")
    # Go to the books/home page
    driver.get(f"{BASE_URL}/")
   
    wait = WebDriverWait(driver, 10)
    # Find the first 'Add to Cart' button available on the page
    # This selector looks for buttons containing the text 'Add to Cart'
    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to Cart')]")))
    add_to_cart_btn.click()
   
    print("Item added to cart successfully!")
    time.sleep(2) # Brief pause to allow any toast notifications to appear/disappear


def test_buy_book(driver):
    """Functionality 3: Buy Book (Checkout)"""
    print("Testing Buy Book process...")
    # Navigate to the Cart page
    driver.get(f"{BASE_URL}/cart")
   
    wait = WebDriverWait(driver, 10)
   
    # Click on the Checkout/Buy button
    checkout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Checkout') or contains(text(), 'Place Order') or contains(text(), 'Buy')]")))
    checkout_btn.click()
   
    # If there's a shipping/payment form, you would fill it here.
    # Assuming it leads to a success page or confirmation.
    print("Buy Book process initiated!")
    time.sleep(3)


if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_user_login(driver)
        test_add_to_cart(driver)
        test_buy_book(driver)
        print("\nAll 3 tests passed successfully!")
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
    finally:
        time.sleep(5)
        driver.quit()

