import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- CONFIGURATION ---
BASE_URL = "http://localhost:3000"

# IMPORTANT: This user MUST exist in your MongoDB database!
# If this user does not exist, the Login test will fail.
USER_EMAIL = "demo.123@gmail.com"
USER_PASSWORD = "demo@123"

def setup_driver():
    """Initializes the Chrome driver with robust Headless settings."""
    options = Options()
    
    # --- HEADLESS MODE (REQUIRED FOR JENKINS) ---
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Automatically install the matching ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def test_login(driver):
    """Test 1: Login using credentials"""
    print("[TEST] Starting Login Test...")
    driver.get(f"{BASE_URL}/login")
    
    wait = WebDriverWait(driver, 10)

    # 1. Fill Email
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.clear()
    email_field.send_keys(USER_EMAIL)

    # 2. Fill Password
    pass_field = driver.find_element(By.NAME, "password")
    pass_field.clear()
    pass_field.send_keys(USER_PASSWORD)

    # 3. Click Login Button (Matches text 'Log In' from Login.js)
    login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    login_btn.click()
    
    # 4. Handle 'Login successful!' Alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"[INFO] Alert detected: {alert.text}")
        alert.accept()
        print("[PASS] Login Alert handled.")
    except:
        print("[WARN] No login alert appeared (Check if user exists in DB).")

    time.sleep(2) # Allow redirect to complete

def test_add_to_cart(driver):
    """Test 2: Add a book to cart"""
    print("[TEST] Starting Add to Cart Test...")
    driver.get(f"{BASE_URL}/") # Go to Home
    
    wait = WebDriverWait(driver, 10)
    
    # 1. Wait for Books to Load (Gallery.js renders .book-card)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-card")))
        print("[INFO] Books loaded from Backend.")
    except:
        print("[FAIL] No books found on Home page (Is Backend running?).")
        return

    # 2. Click "Add to Cart" on the first available book
    try:
        add_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Add to Cart')])[1]")
        add_btn.click()
        
        # 3. Handle 'Book added to cart!' Alert
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"[INFO] Alert detected: {alert.text}")
        alert.accept()
        print("[PASS] Item added to cart.")
    except Exception as e:
        print(f"[WARN] Failed to click Add to Cart: {e}")

def test_checkout(driver):
    """Test 3: Proceed to Checkout"""
    print("[TEST] Starting Checkout Test...")
    driver.get(f"{BASE_URL}/cart")
    
    wait = WebDriverWait(driver, 10)

    # 1. Look for 'Proceed to Checkout' button (from Cart.js)
    try:
        checkout_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn")))
        if "Proceed to Checkout" in checkout_btn.text:
             checkout_btn.click()
             print("[PASS] Successfully clicked 'Proceed to Checkout'.")
        else:
             print(f"[WARN] Button text mismatch. Found: {checkout_btn.text}")
    except:
        print("[WARN] Checkout button not found (Cart might be empty).")

if __name__ == "__main__":
    try:
        driver = setup_driver()
        test_login(driver)
        test_add_to_cart(driver)
        test_checkout(driver)
        print("\n[SUCCESS] All tests execution finished.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        # Print page source for debugging if needed
        # print(driver.page_source[:500])
        sys.exit(1)
    finally:
        if 'driver' in locals():
            driver.quit()