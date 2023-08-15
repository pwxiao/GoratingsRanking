import requests
from bs4 import BeautifulSoup

def processDetail(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text


    soup = BeautifulSoup(html_content, 'html.parser')
    genderColor = {'♂':"color:#0295FF",'♀':'color:#FE0097'}


    table_rows = soup.find_all('tr')

    list=[]
    for row in table_rows:
        dict={}
        columns = row.find_all('td')
        if len(columns) >= 9:
            date = columns[0].text.strip()
            rating = columns[1].text.strip()
            color = columns[2].text.strip()
            result = columns[3].text.strip()
            player_name = columns[4].find('a').text.strip()
            player_rating = columns[5].text.strip()
            player_gender = columns[6].span.text.strip()
            player_nationality = columns[7].img['alt']
            game_link = columns[8].find('a')['href']
            dict['Date'] = date
            dict['Rating'] = rating 
            dict['Color'] = color
            dict['Result'] = result
            dict['PlayName'] = player_name
            dict['PlayerRating'] = player_rating
            dict['PlayGender'] = player_gender
            dict['PlayGenderColor'] = genderColor[player_gender]
            dict['PlayNation'] = player_nationality
            dict['GameLink'] = game_link
        list.append(dict)

    return list
    

print(processDetail('https://www.goratings.org//zh/players/1313.html'))