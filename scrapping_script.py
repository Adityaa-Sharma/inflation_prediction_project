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
import pandas as  pd
combined_df = pd.DataFrame(data_repo, columns=['Date', 'Repo Rate'])

# Save the DataFrame to an Excel file
# combined_df.to_excel('Repo_Rate.xlsx', index=False)


## scrapping of inflation data yoy.
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


## inflation based on the cpi
url1='https://labourbureau.gov.in/rate-of-inflation'
xpath1 = "//table[@class='table']//tbody//tr"

# inflation_mom_cpi=scrape_table_rows(url1,xpath1)
# inflation_mom1_cpi = [list(row) for row in inflation_mom_cpi ]

# print(inflation_mom1_cpi)


## consumer confidence index

import pandas as pd

# Provided CPI data
cci_data = [
    98.5, 98.4, 98.2, 97.9, 97.4, 96.6, 95.9, 95.5, 95.7, 96.0, 95.3, 93.1,
    90.2, 88.0, 87.6, 88.4, 89.8, 91.5, 93.2, 94.8, 96.2, 97.3, 98.3, 99.1,
    99.6, 99.6, 99.1, 98.6, 98.6, 99.8, 101.6, 103.1, 103.8, 103.8, 103.4,
    102.5, 101.5, 100.7, 100.3, 100.2, 100.4, 100.8, 101.3, 101.7, 102.0,
    102.2, 102.3, 102.4, 102.7, 103.1, 103.7, 104.4, 104.7, 104.3, 103.6,
    102.9, 102.2, 101.8, 101.6, 101.6, 101.7, 101.7, 101.3, 100.8, 100.4,
    100.3, 100.4, 100.3, 99.9, 99.5, 99.4, 99.9, 100.6, 101.1, 101.0, 100.6,
    100.2, 100.2, 100.4, 100.7, 101.0, 101.1, 101.3, 101.4, 101.6, 101.7,
    101.7, 101.8, 102.0, 102.4, 103.0, 103.7, 104.3, 104.8, 105.0, 104.8,
    104.3, 103.7
]

# Generate date range from August 2012 to September 2020
# date_range = pd.date_range(start='2012-08-01', end='2020-09-01', freq='MS')

# Create a DataFrame
# cci_df = pd.DataFrame({'Date': date_range, 'CCI': cci_data})

# Display the DataFrame
# print(cci_df)



# gdp data mmanipulation


l=[6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.25,
5.90,
5.90,
5.90,
5.40,
4.90,
4.90,
4.40,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.00,
4.40,
4.40,
5.15,
5.15,
5.15,
5.15,
5.15,
5.40,
5.40,
5.75,
5.75,
6,
6,
6.25,
6.25,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.25,
6.25,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.25,
6.25,
6.25,
6.25,
6.25,
6.25,
6.25,
6.25,
6.25,
6.25,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
7.25,
7.25,
7.25,
7.50,
7.50,
7.50,
7.75,
7.75,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
7.75,
7.75,
7.75,
7.50,
7.25,
7.25,
7.25,
7.25,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.75,
6.50,
6.50,
6.25,
6.25,
6.00,
6.00,
5.75,
5.75,
5.25,
5.25,
5.25,
5.00,
4.75,
4.75,
4.75,
4.75,
4.75,
4.75,
4.75,
4.75,
4.75,
4.75,
4.75,
5.00,
5.50,
5.50,
6.50,
7.50,
8.00,
9.00,
9.00,
9.00,
8.50,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.75,
7.50,
7.50,
7.25,
7.25,
7.25,
7.00,
7.00,
7.00,
6.50,
6.50,
6.50,
6.50,
6.50,
6.50,
6.25,
6.25,
6.25,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
6.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.00,
7.50,
7.50,
7.50,
7.50,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.00,
8.50,
8.50,
8.50,
8.50,
8.50,
8.50,
8.50,
8.50,
8.50,
8.75,
8.75,
9.00,
10.00,
10.00,
10.00,
10.00,
10.25,
13.50,
15.00,
10.00,
12.25,

]

i=272
while(i>=0):
    print(l[i])
    i-=1

