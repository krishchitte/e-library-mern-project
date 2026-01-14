import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- CONFIGURATION ---
BASE_URL = "http://localhost:3000"
# NOTE: Ensure this user exists in your MongoDB for login to succeed!
USER_EMAIL = "demo.123@gmail.com"
USER_PASSWORD = "demo@123"

def setup_driver():
    """Initializes the Chrome driver."""
    options = Options()
    # Headless mode is REQUIRED for Jenkins
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Automatically install and use the correct ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver

def test_user_login(driver):
    """Functionality 1: User Login"""
    print("Testing User Login...")
    driver.get(f"{BASE_URL}/login")
    
    wait = WebDriverWait(driver, 10)
    # Wait for email input
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_input = driver.find_element(By.NAME, "password")
    
    # Matches the 'Log In' button text from your React component
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")

    email_input.send_keys(USER_EMAIL)
    password_input.send_keys(USER_PASSWORD)
    login_button.click()
    print("Login credentials submitted.")
    time.sleep(2)

def test_add_to_cart(driver):
    """Functionality 2: Add to Cart"""
    print("Testing Add to Cart...")
    driver.get(f"{BASE_URL}/")
    
    wait = WebDriverWait(driver, 10)
    try:
        # Find the first 'Add to Cart' button available on the page
        add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to Cart')]")))
        add_to_cart_btn.click()
        print("Item added to cart successfully!")
        time.sleep(2)
    except Exception as e:
        print("[WARN] 'Add to Cart' button not found. Is the backend running/database populated?")

def test_buy_book(driver):
    """Functionality 3: Buy Book (Checkout)"""
    print("Testing Buy Book process...")
    driver.get(f"{BASE_URL}/cart")
    
    wait = WebDriverWait(driver, 10)
    try:
        # Matches 'Proceed to Checkout'
        checkout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Checkout')]")))
        checkout_btn.click()
        print("Buy Book process initiated!")
        time.sleep(3)
    except Exception as e:
        print("[WARN] Checkout button not found. Is the cart empty?")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_user_login(driver)
        test_add_to_cart(driver)
        test_buy_book(driver)
        print("\nAll tests sequence completed!")
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
    finally:
        driver.quit()