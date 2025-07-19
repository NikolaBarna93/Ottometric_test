from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This is the dropdown helper class that handles dropdown interactions
class DropdownHelper:
    def __init__(self, driver):
        self.driver = driver
    # Clicks an element by its data-testid attribute
    def click_by_testid(self, testid):
        # Wait for the element to be clickable and click it
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{testid}"]'))
        )
        element.click()
        return element
    # Waits until an element is selected by its data-testid attribute
    def wait_until_selected_by_testid(self, testid):
        WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            f'//*[@data-testid="{testid}" and (@aria-selected="true" or contains(@class, "Mui-selected"))]'
        ))
    )
    # Waits for the page to be idle
    def wait_for_idle(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

