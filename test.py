from bs4 import BeautifulSoup
import requests


url = "https://www.goratings.org/zh/"
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
data = BeautifulSoup(html, 'html.parser')
matchNation = {'kr':"韩国",'cn':'中国','jp':'日本','tw':'中国台湾'}
csv_data = []
for tr in data.find_all("tr"):
    tds = tr.find_all('td')
    if len(tds) == 5:
        rank = tds[0].text.strip()
        name = tds[1].text.strip()
        link = tds[1].a['href']
            # gender = tds[2].span.text.strip()
        nationality = str(tds[3].img['alt'])
            # try:
            #       nationality = matchNation[str(tds[3].img['alt'])]
            # except:
        nationality = tds[3].img['alt']
        level = tds[4].text.strip()
        s = {}
        s['link'] = link
        s['rank'] = rank
        s['name'] = name
        s['nationality'] = nationality
        s['level'] = level
        csv_data.append(s)
print(csv_data)