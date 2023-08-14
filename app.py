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
    matchNation = {'kr':"韩国",'cn':'中国','jp':'日本','tw':'中国台湾'}
    csv_data = []
    for tr in data.find_all("tr"):
        tds = tr.find_all('td')
        if len(tds) == 5:
            rank = tds[0].text.strip()
            name = tds[1].text.strip()
            # gender = tds[2].span.text.strip()
            nationality = str(tds[3].img['alt'])
            try:
                  nationality = matchNation[str(tds[3].img['alt'])]
            except:
                  nationality = tds[3].img['alt']
            level = tds[4].text.strip()
            s = {}
            s['rank'] = rank
            s['name'] = name
            s['nationality'] = nationality
            s['level'] = level
            csv_data.append(s)
    return csv_data


@app.route('/')
def main():
    data = work()
    return render_template("index.html",datas = data)
if __name__ == '__main__':
   
    app.run(debug=True)