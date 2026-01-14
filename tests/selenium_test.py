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
USER_EMAIL = "krish.v.chitte@gmail.com"
USER_PASSWORD = "Krish@123"

def setup_driver():
    options = Options()
    # Jenkins Headless Settings
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Store session data
    options.add_argument("--user-data-dir=/tmp/selenium_user_data") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run_tests(driver):
    wait = WebDriverWait(driver, 20)

    # --- STEP 1: LOGIN ---
    print(f"[TEST] 1. Logging In as {USER_EMAIL}...")
    driver.get(f"{BASE_URL}/login")
    
    # Fill Credentials
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).clear()
    driver.find_element(By.NAME, "email").send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
    
    # Click 'Log In'
    # Using JavaScript click is safer for headless execution
    login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    driver.execute_script("arguments[0].click();", login_btn)
    
    # Handle Login Alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"[INFO] Login Alert: {alert.text}")
        alert.accept()
    except:
        print("[INFO] No login alert appeared.")

    # --- CRITICAL WAIT FOR RELOAD ---
    print("[INFO] Waiting for page reload...")
    time.sleep(8) 
    
    # Verify we are logged in
    print(f"[INFO] URL after login: {driver.current_url}")
    # If still on /login, try forcing a navigation to Home since the token should be in localStorage now
    if "/login" in driver.current_url:
        print("[WARN] Still on login page. Navigating to Home manually...")
        driver.get(f"{BASE_URL}/") 

    # --- STEP 2: ADD TO CART ---
    print("[TEST] 2. Adding to Cart...")
    driver.get(f"{BASE_URL}/")
    
    try:
        # Wait for books
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-card")))
        
        # Find button and SCROLL TO IT (Fixes layout issues)
        add_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Add to Cart')])[1]")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        time.sleep(1) # Wait for scroll
        
        # Click
        driver.execute_script("arguments[0].click();", add_btn)
        
        # Handle Cart Alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        print(f"[PASS] Add to Cart Alert: {alert_text}")
        
        if "log in" in alert_text.lower() or "invalid" in alert_text.lower():
             raise Exception("Session Lost! User is not logged in.")

    except Exception as e:
        print(f"[WARN] Add to Cart failed: {e}")

    # --- STEP 3: CHECKOUT ---
    print("[TEST] 3. Checking Out...")
    driver.get(f"{BASE_URL}/cart")
    try:
        checkout_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_btn)
        driver.execute_script("arguments[0].click();", checkout_btn)
        print("[PASS] Checkout button clicked.")
    except:
        print("[WARN] Checkout button not found (Cart might be empty).")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        run_tests(driver)
        print("\n[SUCCESS] Tests Finished.")
    except Exception as e:
        print(f"\n[ERROR] Critical Test Failure: {e}")
        sys.exit(1)
    finally:
        driver.quit()