# Import modules

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as url_req
import unicodedata

# 2018 World Cup Squad - Wikipedia

url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads'

# Read html file from the url, opening up the connection

url_client = url_req(url)
html = url_client.read()
url_client.close()

# Create and open a new file

filename = 'world_cup_2018_players.csv'
f = open(filename, 'w')

# Variable definition

no = ''
pos = ''
player_name = ''
date_of_birth = ''
caps = ''
goals = ''
club = ''
country = ''
headers = []

# HTML Parsing

html_soup = soup(html, "html.parser")
main_container = html_soup.body.find('div', {'id': 'bodyContent'}).find('div', {'id': 'mw-content-text'}).div           # Main Container

# list of all the countries participating in World Cup 2018

list = main_container.findAll('h3')  
country_list = []
for country in list:
    country_list.append(country.span.text)
country_list = country_list[0:32]       # Country List

list = main_container.findAll('table', {'class': 'plainrowheaders'})

# Headers for the csv file

header_list = list[0].tbody.tr.findAll('th')
for header in header_list:
    headers.append((header.text).strip())
headers.append('Country\n'.strip())

head = ', '.join(headers)
f.write(head + '\n')

# Convert latin characters to english

def strip_accents(text):
    text = text.replace(u'\u0142', 'l')
    text = text.replace(u'\u0141', 'L')
    text = text.replace(u'\u0131', 'I')
    nfkd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Get Club

def get_club(text):
    clubs = text.findAll('a')
    return clubs[1].text

# Get Players data

count = 0
for l in list:
    table_list = l.findAll('tr')
    country = country_list[count]
    for table in table_list[1:]:
        detail = table.findAll('td')
        no = detail[0].text
        pos = detail[1].a.text
        date_of_birth = detail[2].text
        caps = detail[3].text
        goals = detail[4].text
        club = get_club(detail[5])
        player_name = table.th.a['title']
        string = no.strip() + ',' + pos.strip() + ',' + strip_accents(player_name.strip()) + ',' + date_of_birth.strip() + ',' + caps.strip() + ',' + goals.strip() + ',' + strip_accents(club.strip()) + ',' + country.strip() + '\n'
        f.write(string)
    count = count + 1


f.close()