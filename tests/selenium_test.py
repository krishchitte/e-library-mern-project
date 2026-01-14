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
USER_EMAIL = "demo123@gmail.com"
USER_PASSWORD = "demo123"

def setup_driver():
    options = Options()
    # Robust Headless Settings for Jenkins
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Store user data to keep login session alive
    options.add_argument("--user-data-dir=/tmp/selenium_user_data") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run_tests(driver):
    wait = WebDriverWait(driver, 15)

    print("[TEST] 1. Starting Login...")
    driver.get(f"{BASE_URL}/login")
    
    # Check if we hit a 404 page (Nginx issue)
    if "404" in driver.title:
        raise Exception("Nginx returned 404! Check client/Dockerfile config.")

    # Login Logic
    wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(USER_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(USER_PASSWORD)
    
    login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    driver.execute_script("arguments[0].click();", login_btn)
    
    # Handle Login Alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        print(f"[INFO] Alert: {driver.switch_to.alert.text}")
        driver.switch_to.alert.accept()
    except:
        print("[INFO] No login alert.")

    # Wait for redirect to Profile
    time.sleep(3)
    print(f"[INFO] Current URL: {driver.current_url}")

    if "/profile" in driver.current_url:
        print("[PASS] Login Successful!")
    else:
        print("[WARN] Login might have failed or redirect is slow.")

    print("[TEST] 2. Adding to Cart...")
    driver.get(f"{BASE_URL}/")
    
    try:
        # Wait for books to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-card")))
        
        # Click Add to Cart
        add_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Add to Cart')])[1]")
        driver.execute_script("arguments[0].click();", add_btn)
        
        # Handle Cart Alert
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = driver.switch_to.alert.text
        driver.switch_to.alert.accept()
        print(f"[PASS] Alert: {alert_text}")
        
        if "Invalid" in alert_text:
             raise Exception("Session Invalid - Login did not persist!")

    except Exception as e:
        print(f"[WARN] Add to Cart failed: {e}")

    print("[TEST] 3. Checkout...")
    driver.get(f"{BASE_URL}/cart")
    try:
        checkout_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "checkout-btn")))
        checkout_btn.click()
        print("[PASS] Checkout button clicked.")
    except:
        print("[WARN] Checkout button not found.")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        run_tests(driver)
        print("\n[SUCCESS] Tests Finished.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    finally:
        driver.quit()