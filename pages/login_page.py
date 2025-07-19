from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.CSS_SELECTOR, '[data-testid="email-input-field"]')
        self.password_input = (By.CSS_SELECTOR, '[data-testid="password-input-field"]')
        self.login_button = (By.CSS_SELECTOR, '[data-testid="otto-login-btn"]')

    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)  # 10 seconds max
        wait.until(EC.visibility_of_element_located(self.username_input)).send_keys(username)
        wait.until(EC.visibility_of_element_located(self.password_input)).send_keys(password)
        wait.until(EC.element_to_be_clickable(self.login_button)).click()