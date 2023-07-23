import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers
import json


def get_headers():
    return Headers(browser="firefox", os="win").generate()


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(html, features='lxml')

all_vac_div = soup.find(id='a11y-main-content')

vac_list = all_vac_div.find_all(class_='vacancy-serp-item__layout')

result_list = []
for vac in vac_list:
    vac_name_tag = vac.find('a', class_='serp-item__title')


    vac_link = vac_name_tag['href']
    vac_html = requests.get(vac_link, headers=get_headers()).text
    vac_desc = BeautifulSoup(vac_html, features='lxml').find(class_='vacancy-description').text
    if 'Django' in vac_desc or 'Flask' in vac_desc:
        vac_name = vac_name_tag.text
        comp_name = vac.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace(u'\xa0', u' ')
        adress = vac.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
        salary_tag = vac.find('span', class_="bloko-header-section-3")
        if salary_tag is None:
            salary = ''
        else:
            salary = salary_tag.text.replace(u'\u202f', u' ')

        result_list.append({
            'name': vac_name,
            'link': vac_link,
            'salary': salary,
            'company': comp_name,
            'adress': adress
        })

with open(r" vacancy_list.json", 'w', encoding='utf-8') as f:
    json.dump(result_list, f, ensure_ascii=False, indent=2)