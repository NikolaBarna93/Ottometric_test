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
    
#Function to calculate the average percentage from a specific column in the table
def calculate_sum(driver, col_index, column_name):
    table = driver.find_element(By.CSS_SELECTOR, '[data-testid="table-center"]')
    rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
    footer_row = table.find_element(By.CSS_SELECTOR, 'tfoot tr')
    footer_cells = footer_row.find_elements(By.CSS_SELECTOR, 'td')
    # Get the footer value for the column
    if len(footer_cells) > col_index:
        value = footer_cells[col_index].text.strip()
    else:
        print(f"No footer cell at index {col_index}")
    percentages = []
    # Iterate through each row and extract the percentage value from the specified column
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
        if len(cells) > col_index:
            cell_text = cells[col_index].text.strip()
            if "%" in cell_text:
                percentages.append(cell_text)
            else:
                print(f"Skipping non-percentage value: {cell_text}")

    # Convert and average
    values = [float(p.strip().replace('%', '')) for p in percentages if p.strip()]
    if not values:
        return "0.0%"
    average = sum(values) / len(values)
    average = f"{round(average, 1)}%"
    if(average == value):
        return (f"{column_name} \t calculated value matches table value: \t{average}")
        
    else:
        return (f"{column_name} \t calculated value does not match table value: \t {average} != {value}")


report_file = 'test1_report.txt'
if os.path.exists(report_file):
    os.remove(report_file)

# Setup browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://qa-ottoviz.ominf.net/")

# Log in
login_page = LoginPage(driver)
login_page.login("test_user_123@test.com", "rusaiilzsmtvnhet")

# Navigate to correct table
dropdownHelper = DropdownHelper(driver)
dropdownHelper.click_by_testid("program-picker-menu-select")
dropdownHelper.click_by_testid("Camera System VT1")
dropdownHelper.wait_for_idle()
dropdownHelper.click_by_testid("KPI Sensor-drawer")
dropdownHelper.click_by_testid("FCM-drawer")
dropdownHelper.click_by_testid("Lanes-drawer")
dropdownHelper.wait_for_idle()

# Wait for table to load
time.sleep(1) 
# Get needed table elements
table = driver.find_element(By.CSS_SELECTOR,'[data-testid="table-center"]')
header_rows = table.find_elements(By.CSS_SELECTOR, 'thead tr')
first_header = header_rows[0]
second_header = header_rows[1]

first_column = first_header.find_elements(By.CSS_SELECTOR, 'th')
columns = second_header.find_elements(By.CSS_SELECTOR, 'th')
num_columns = len(columns)

for i in range(num_columns):
    j=int(i/2)
    column_name = first_column[j].text.strip() + ' ' + columns[i].text.strip()
    with open(report_file, 'a', encoding='utf-8') as file:
        file.write(calculate_sum(driver,i,column_name) + '\n')

driver.quit()
print(f"Report saved to {report_file}")