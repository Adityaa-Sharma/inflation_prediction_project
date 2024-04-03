from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://freefincal.com/rbi-repo-rate-history/').text
soup = BeautifulSoup(html_text, 'lxml')
tbody = soup.find('tbody')

data = []

if tbody:
    tr_tags = tbody.find_all('tr')
    for tr in tr_tags:
        td_tags = tr.find_all('td')
        if len(td_tags) == 2:
            data.append((td_tags[0].text.strip(), td_tags[1].text.strip()))



data_copy = [list(row) for row in data]
def print_data(data):
    for row in data:
        print(row)

# ignoring the days
for row in data_copy[1:]:
    row[0] = row[0][3:]
    



def remove_duplicates_by_first_column(data):
    unique_data = {}  
    for row in data:
        
        key = row[0]
        if key not in unique_data:
            unique_data[key] = row
    # Converting the dictionary back to a list of rows
    unique_data_list = list(unique_data.values())
    return unique_data_list


data_copy=remove_duplicates_by_first_column(data_copy)
# print_data(data_copy)

def missing_month(data):
    l = len(data)
    i = 0
    while i < (len(data) - 1):
        try:
            month1 = int(data[i][0][0:2])
            year1 = int(data[i][0][3:])
            month2 = int(data[i + 1][0][0:2])
            year2 = int(data[i + 1][0][3:])
            rate = data[i + 1][1]

            diff_month = month1 - month2
            diff_yr = year1 - year2
            count = 0

            if diff_yr > 0:
                flag = 0
                for j in range(12 + diff_month - 1):
                    month1 -= 1
                    count += 1
                    if month1 > 0:
                        if flag == 0:
                            data.insert(i + 1 + j, [f"{month1:02d}-{year1}", rate])
                        else:
                            data.insert(i + 1 + j, [f"{month1:02d}-{year2}", rate])

                    else:
                        month1 += 12
                        flag = 1

                        data.insert(i + 1 + j, [f"{month1:02d}-{year2}", rate])
            else:
                for j in range(diff_month - 1):
                    month1 -= 1
                    count += 1
                    data.insert(i + 1 + j, [f"{month1:02d}-{year1}", rate])

            i += count + 1

        except ValueError:
            # Handle invalid month string
            print("Invalid month string:", data[i][0])
            # Skip to the next iteration
            i += 1

    return data

data_repo=missing_month(data_copy)
# print_data(data_repo)





## scrapping of inflation data.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def scrape_table_rows(url, xpath):

    driver = webdriver.Chrome()

    # Load the page
    driver.get(url)

    # Find all <tr> elements within the specified XPath
    tr_elements = driver.find_elements(By.XPATH, xpath)

    # Initialize an empty list to store the data
    data = []

    # Extract and append the text content of each <td> element in each <tr>
    for tr in tr_elements:
        td_elements = tr.find_elements(By.TAG_NAME, "td")
        row_data = [td.text.strip() for td in td_elements]
        data.append(row_data)

    # After you're done, close the WebDriver
    driver.quit()

    return data

# Example usage:
url = 'https://www.macrotrends.net/global-metrics/countries/IND/india/inflation-rate-cpi'
xpath = "//table[@class='historical_data_table table table-striped table-bordered']//tbody//tr"
# data_inflation = scrape_table_rows(url, xpath)

# data_inflation1 = [list(row) for row in data_inflation ]
# print_data(data_inflation1)
# data_inflation1.insert(0,['Year','Inflation_rate','Inflation_change'])
# print_data(data_inflation1)



## calculating the reverse repo rate data.

xpath1 = "//div[@class='econ_tablebx historicdata']//table[@id='hist_tbl']/tbody"
url1='https://www.moneycontrol.com/economic-calendar/india-reverse-repo-rate/9010822'


def scrape_table_rows_button(url, button_class, xpath):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Load the page
        driver.get(url)

        # Find the "Show More" button element
        more_button = driver.find_element(By.CLASS_NAME, button_class)

        # Use JavaScript to click the button
        driver.execute_script("arguments[0].click();", more_button)

        # Wait for the additional data to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

        # Find the table element
        table = driver.find_element(By.XPATH, xpath)

        # Extract the data from the table
        data = []
        for row in table.find_elements(By.TAG_NAME, "tr"):
            row_data = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
            data.append(row_data)

        return data
    finally:
        # Close the WebDriver
        driver.quit()

# Example usage
url = 'https://www.moneycontrol.com/economic-calendar/india-reverse-repo-rate/9010822'
button_class = 'show_more_alink'
xpath = "//table[@class='MT15']//tbody//tr"
data_rrr = scrape_table_rows_button(url, button_class, xpath)
print_data(data_rrr)


