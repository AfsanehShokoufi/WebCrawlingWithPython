import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import csv
ringList = []
for page_number in range(1, 24):
    url_site = f'https://zar.ir/shop/cat-34-{page_number}.html'
    site = requests.get(url_site)
    soup = BeautifulSoup(site.text, features='html.parser')
    pageContainer = soup.find('div', {'class': 'grid-container'})
    itemContainer = pageContainer.find_all('div', {'class': 'Box'})

    links = []
    title = []
    model = []
    goldWeight = []
    brilliantWeight = []
    brilliantType = []
    colorGrade = []
    clarity = []
    polish = []
    qualityType = []
    guarantyType = []
    standardCode = []
    stoneWeight = []
    price = []

    for item in itemContainer:
        link_url = item.find('a')['href']
        complete_url = urljoin("https://zar.ir/", link_url)
        link_url_get = requests.get(complete_url)
        link_url_parse = BeautifulSoup(link_url_get.text, features='html.parser')
        link_url_parse_ul = link_url_parse.find('div', {'id': 'product-summary-props'})
        titleModel = link_url_parse.find('h1', {'class': 'nostyle h1'})

        title.append(titleModel.get_text(strip=True).split(':')[0].replace('مدل', ''))
        model.append((titleModel.get_text(strip=True).split(':')[1]))
        li_elements = link_url_parse_ul.find_all('li')
        goldWeight.append(li_elements[0].text.split(':')[1])
        brilliantWeight.append(li_elements[1].text.split(':')[1])
        brilliantType.append(li_elements[2].text.split(':')[1])
        colorGrade.append(li_elements[3].text.split(':')[1])
        clarity.append(li_elements[4].text.split(':')[1])
        polish.append(li_elements[5].text.split(':')[1])
        qualityType.append(li_elements[6].text.split(':')[1])
        guarantyType.append(li_elements[7].text.split(':')[1])
        # standardCode.append(int(li_elements[8].text.split(':')[1]))
        stoneWeight.append(li_elements[9].text.split(':')[1])
        price.append(int(li_elements[14].text.split(':')[1].replace('تومان','').replace(',','')))
    # print(polish)
    myDictionary = {
        'Title':title,
        'Model':model,
        'Gold Weight': goldWeight,
        'Brilliant Weight': brilliantWeight,
        'Brilliant Type': brilliantType,
        'Color Grade': colorGrade,
        'Clarity': clarity,
        'Polish': polish,
        'Quality Type': qualityType,
        'Guaranty Type': guarantyType,
        'Standard Code': standardCode,
        'Stone Weight': stoneWeight,
        'Price': price
    }

    df = pd.DataFrame.from_dict(myDictionary)
    ringList.append(df)

    df_merged = pd.concat(ringList, ignore_index=True)
    df_merged.to_csv('FinalOutput.csv', index=False,encoding='utf-8-sig')
