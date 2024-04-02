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
    
    

def missing_month(data):
    for i in range(1, len(data) - 1):
        month1 = int(data[i][0][0:2])
        year1 = int(data[i][0][3:])
        month2 = int(data[i + 1][0][0:2])
        year2 = int(data[i + 1][0][3:])
        rate = data[i+1][1]

        diff_month = month1 - month2
        diff_yr = year1 - year2
        
        if diff_yr > 0:
            flag=0
            for j in range(12 + diff_month - 1):
                month1 -= 1
                if month1 >0:
                    if flag==0:
                        data.insert(i + 1 + j, [f"{month1:02d}-{year1}", rate])
                    else:
                        data.insert(i + 1 + j, [f"{month1:02d}-{year2}", rate])
                            
                else:
                    month1+=12
                    flag=1
            
                    data.insert(i + 1 + j, [f"{month1:02d}-{year2}", rate])
        else:
            for j in range(diff_month - 1):
                month1-=1
                data.insert(i + 1 + j, [f"{month1:02d}-{year1}", rate])

    return data

data_repo=missing_month(data_copy)
print_data(data_repo)