import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.dropdown_helper import DropdownHelper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Function to count ENV events for a given DTID
def count_FN(driver, dtid, table):
    all_rows = table.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
    row_prefix = f"MuiTableRow-root row-{dtid}."
    subrow_count = sum(
        1 for row in all_rows
        if row_prefix in row.get_attribute("class")
    )
    return (f"DTID {dtid} has {subrow_count} sub-rows.")
    
# Delete report file if it exists
report_file = 'test2_report.txt'
if os.path.exists(report_file):
    os.remove(report_file)

# Setup browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://qa-ottoviz.ominf.net/")

# Log in
login_page = LoginPage(driver)
login_page.login("test_user_123@test.com", "rusaiilzsmtvnhet")

# Navigate to correct table and sort it by false
dropdownHelper = DropdownHelper(driver)
dropdownHelper.click_by_testid("program-picker-menu-select")
dropdownHelper.click_by_testid("Camera System VI1")
dropdownHelper.wait_for_idle()
dropdownHelper.click_by_testid("KPI Feature-drawer")
dropdownHelper.click_by_testid("ISA-drawer")
dropdownHelper.click_by_testid("Zone1-drawer")
dropdownHelper.wait_for_idle()
dropdownHelper.click_by_testid("sorting-false-100031")
time.sleep(1)

# Iterate through the first 7 rows and count ENV events for each DTID
table = driver.find_element(By.CSS_SELECTOR, '[data-testid="table-left"]')
rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
for i in range(min(7, len(rows))): 
    try:
        cells = rows[i].find_elements(By.CSS_SELECTOR, "td")
        dtid_cell = cells[1]  # second cell is DTID
        dtid_text = dtid_cell.text.strip()
        # Expanding row for speciffic DTID
        preview_button = rows[i].find_element(By.CSS_SELECTOR, '[data-testid="KeyboardArrowDownIcon"]')
        preview_button.click()
        time.sleep(1)
        report_entry = count_FN(driver, dtid_text, table)
        # Write the result in report file
        with open(report_file, 'a', encoding='utf-8') as file:
            file.write(report_entry + '\n')
        # Collapse the row after processing
        colaps_button = rows[i].find_element(By.CSS_SELECTOR, '[data-testid="KeyboardArrowUpIcon"]')
        colaps_button.click()
        time.sleep(1)
    # Here we handle the case when row is not expanded
    except Exception as e:
        time.sleep(1)
        # Search for elements with data-testid="PreviewIcon" No.1
        preview_icons = driver.find_elements(By.XPATH, '//*[@data-testid="PreviewIcon"]')
        print(f"Row {i+1} error: {e}")
        if preview_icons:
            print(f"Found {len(preview_icons)} element(s) with data-testid='PreviewIcon'")
            for i, elem in enumerate(preview_icons):
                print(f"Element {i+1}: tag={elem.tag_name}, visible={elem.is_displayed()}")
        else:
            print("No elements with data-testid='PreviewIcon' found.")

        from selenium.webdriver.common.by import By

    # Search for elements with data-testid="PreviewIcon" No.2
        all_testid_elements = driver.find_elements(By.XPATH, '//*[@data-testid]')
        for elem in all_testid_elements:
            testid = elem.get_attribute("data-testid")
            if testid == "PreviewIcon":
                print("Found PreviewIcon!")
                print(elem.get_attribute("outerHTML"))
    # data-testid="PreviewIcon" us nowhere to be found. So I found workaround by closing expanded rows
driver.quit()
print(f"Report saved to {report_file}")