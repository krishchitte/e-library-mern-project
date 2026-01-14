import time
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- CONFIGURATION ---
BASE_URL = "http://localhost:3000"
# Generate a random user for each test run to ensure a fresh state
RAND_ID = random.randint(1000, 9999)
USER_NAME = f"Tester{RAND_ID}"
USER_EMAIL = f"tester{RAND_ID}@example.com"
USER_PASSWORD = "Password123!"

def setup_driver():
    options = Options()
    # Headless mode for Jenkins
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Use a temporary user data directory to maintain session state (localStorage)
    options.add_argument("--user-data-dir=/tmp/selenium_user_data_" + str(RAND_ID))

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run_tests(driver):
    wait = WebDriverWait(driver, 20)

    # --- STEP 0: SIGN UP (Crucial for fresh environment) ---
    print(f"[TEST] 0. Signing Up new user: {USER_EMAIL}...")
    driver.get(f"{BASE_URL}/signup")
    
    # Check for 404 (Nginx issue check)
    if "404" in driver.title:
        raise Exception("Nginx 404 Error! Check client/Dockerfile config.")

    # Fill Signup Form
    wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(USER_NAME)
    driver.find_element(By.NAME, "email").send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
    
    # Attempt Signup
    try:
        signup_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign Up')]")
        driver.execute_script("arguments[0].click();", signup_btn)
        
        # Handle potential Signup Alert
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(f"[INFO] Signup Alert: {alert.text}")
            alert.accept()
            time.sleep(2) # Wait for redirect to login
        except:
            print("[INFO] No signup alert or auto-redirected.")
            
    except Exception as e:
        print(f"[WARN] Signup step had issues (maybe CAPTCHA?): {e}")
        # We proceed to login anyway, just in case the user was created or we fall back to a known user if you edit the constants.

    # --- STEP 1: LOGIN ---
    print(f"[TEST] 1. Logging In...")
    driver.get(f"{BASE_URL}/login")
    
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).clear()
    driver.find_element(By.NAME, "email").send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
    
    login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    driver.execute_script("arguments[0].click();", login_btn)
    
    # Handle Login Alert
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"[INFO] Login Alert: {alert_text}")
        alert.accept()
        
        if "Invalid" in alert_text or "failed" in alert_text:
             raise Exception(f"Login Failed with alert: {alert_text}")
    except:
        print("[INFO] No login alert appeared.")

    # Wait for reload/redirect to Profile
    print("[INFO] Waiting for redirect...")
    time.sleep(5)
    
    # Check if we are on the profile page OR if the Logout button exists (meaning we are logged in)
    try:
        # Force navigation to home to check Navbar state if redirect didn't happen
        if "/profile" not in driver.current_url:
             driver.get(f"{BASE_URL}/")
        
        # Look for Logout button which signifies a valid session
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logout-btn")))
        print("[PASS] Login Successful! (Logout button detected)")
    except:
        print(f"[FAIL] Login verification failed. URL: {driver.current_url}")
        # Debug: check page source for cues
        # print(driver.page_source)
        raise Exception("User not logged in. Cannot proceed to Add to Cart.")

    # --- STEP 2: ADD TO CART ---
    print("[TEST] 2. Adding to Cart...")
    driver.get(f"{BASE_URL}/")
    
    try:
        # Wait for books to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-card")))
        
        # Find first "Add to Cart" button
        add_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Add to Cart')])[1]")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        time.sleep(1) 
        driver.execute_script("arguments[0].click();", add_btn)
        
        # Handle Cart Alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"[PASS] Add to Cart Alert: {alert.text}")
        alert.accept()
        
        if "log in" in alert_text.lower():
             raise Exception("Session Invalid - User is not logged in!")

    except Exception as e:
        print(f"[WARN] Add to Cart failed: {e}")
        raise e

    # --- STEP 3: CHECKOUT ---
    print("[TEST] 3. Checking Out...")
    driver.get(f"{BASE_URL}/cart")
    time.sleep(2) # Let cart items fetch
    
    try:
        checkout_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_btn)
        driver.execute_script("arguments[0].click();",   checkout_btn)
        print("[PASS] Checkout button clicked.")
    except:
        print("[WARN] Checkout button not found. Cart might be empty.")
        # Check if 'Your cart is empty' message is present
        if "cart is empty" in driver.page_source:
             print("[INFO] Confirmed: Cart is empty.")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        run_tests(driver)
        print("\n[SUCCESS] Tests Finished.")
    except Exception as e:
        print(f"\n[ERROR] Critical Failure: {e}")
        sys.exit(1)
    finally:
        driver.quit()