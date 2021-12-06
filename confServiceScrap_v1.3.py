from bs4 import BeautifulSoup
import requests, csv
import pandas as pd

URL = "https://conference-service.com/conferences/acoustics.html"
responseBS4 = requests.get(URL)
responseBS4

page = BeautifulSoup(responseBS4.text, 'html.parser')
allEvents=page.find_all('div', attrs={'class':'evnt'})
len(allEvents)

section = []
for element in allEvents:
    temp=[]
    link = element.find('a', attrs={'class':'external_link'})
    eventName = element.find('div', attrs={'class': 'conflist_value conflist_title'})
    dateLocation = element.find('div', attrs={'class':'dates_location'}).next_element
    try:   
        temp.append(dateLocation.string)
        temp.append(eventName.string)
        temp.append(link.string)
    except:
        temp.append('ND')
    section.append(temp)
    #len(section)

##rearrange and clean
arr = []
for val in section:
    temp = val[0].split('â\x80¢')
    temp.append(val[1])
    temp.append(val[2])
    arr.append(temp)

HEADER = ['Date', 'Place', 'Event Name', 'Link']
DATA = arr
with open('conf_service.csv', 'w', encoding='utf-8', newline='') as cvsfile:
    rows = csv.writer(cvsfile)
    rows.writerow(HEADER)
    for row in DATA:
        rows.writerow(row)
read_file = pd.read_csv('conf_service.csv')
read_file.to_excel('confService_events.xlsx', index=None, header=True)


