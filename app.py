from flask import Flask,request,render_template
import os
from bs4 import BeautifulSoup
import requests


app = Flask(__name__,template_folder='templates')

def work():
    url = "https://www.goratings.org/zh/"
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    data = BeautifulSoup(html, 'html.parser')
    genderColor = {'♂':"color:#0295FF",'♀':'color:#FE0097'}
    
    csv_data = []
    for tr in data.find_all("tr"):
        tds = tr.find_all('td')
        if len(tds) == 5:
            rank = tds[0].text.strip()
            name = tds[1].text.strip()
            link = tds[1].a['href'].replace('..','https://www.goratings.org/')
            gender = tds[2].span.text.strip()
            nationality = str(tds[3].img['alt'])
            # try:
            #       nationality = matchNation[str(tds[3].img['alt'])]
            # except:
            nationality = tds[3].img['alt']
            level = tds[4].text.strip()
            s = {}
            s['gender'] = gender
            s['genderColor'] = genderColor[gender]
            s['rank'] = rank
            s['name'] = name
            s['link'] = link
            s['nationality'] = nationality
            s['level'] = level
            csv_data.append(s)
    return csv_data



def processDetail(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text


    soup = BeautifulSoup(html_content, 'html.parser')
    genderColor = {'♂':"color:#0295FF",'♀':'color:#FE0097'}
    table = soup.find('table')
    l = []
    for row in table.find_all('tr'):
        cells = row.find_all(['th', 'td'])
        value = cells[1].text.strip()
        l.append(value)

    
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
    list = [d for d in list if d]
    return list,l


@app.route('/showDetail')
def showDetail():

    link = request.args.get('link')
    list,total = processDetail(link)
    return render_template('detail.html',lists=list,total=total)
    # return list


@app.route('/')
def main():
    data = work()
    return render_template("index.html",datas = data)

if __name__ == '__main__':
   
    app.run(debug=True)