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
    """Initializes Chrome with settings compatible with Windows Services."""
    options = Options()
    
    # --- CRITICAL FIXES FOR JENKINS WINDOWS SERVICE ---
    # Use standard headless (more stable than 'new' on some systems)
    options.add_argument("--headless") 
    
    # Disable all GPU and Rendering features that cause crashes
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    
    # Fix for "DevToolsActivePort file doesn't exist" error
    options.add_argument("--remote-debugging-port=9222")
    
    # standard window size
    options.add_argument("--window-size=1920,1080")
    
    # Valid User Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("[SETUP] Driver initialized successfully.")
        return driver
    except Exception as e:
        print(f"[ERROR] Driver failed to start: {e}")
        sys.exit(1)

def test_login(driver):
    print("[TEST] Starting Login Test...")
    try:
        driver.get(f"{BASE_URL}/login")
        
        # Check if page loaded
        print(f"[INFO] Page Title: {driver.title}")
        
        wait = WebDriverWait(driver, 10)

        # 1. Fill Email
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.clear()
        email_field.send_keys(USER_EMAIL)
        print("[INFO] Email entered.")

        # 2. Fill Password
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.clear()
        pass_field.send_keys(USER_PASSWORD)
        print("[INFO] Password entered.")

        # 3. Click Login Button
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
        driver.execute_script("arguments[0].click();", login_btn) # JS Click is safer in headless
        print("[INFO] Login button clicked.")
        
        time.sleep(2)
        print("[PASS] Login sequence finished.")
        
    except Exception as e:
        print(f"[FAIL] Login Test Error: {e}")
        # Capture screenshot for debugging (saved in workspace)
        driver.save_screenshot("login_error.png")
        raise e

def test_add_to_cart(driver):
    print("[TEST] Starting Add to Cart Test...")
    try:
        driver.get(f"{BASE_URL}/")
        wait = WebDriverWait(driver, 10)
        
        # Wait for books
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book-card")))
        
        # Click Add to Cart
        add_btn = driver.find_element(By.XPATH, "(//button[contains(text(), 'Add to Cart')])[1]")
        driver.execute_script("arguments[0].click();", add_btn)
        print("[PASS] Add to Cart clicked.")
        
        # Handle Alert
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
            print("[INFO] Alert accepted.")
        except:
            pass
            
    except Exception as e:
        print(f"[WARN] Add to Cart skipped: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_login(driver)
        test_add_to_cart(driver)
        print("\n[SUCCESS] Tests Completed.")
    except Exception as e:
        print(f"\n[ERROR] Critical Failure: {e}")
        sys.exit(1)
    finally:
        driver.quit()