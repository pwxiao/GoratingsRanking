from bs4 import BeautifulSoup
import requests


url = "https://www.goratings.org/zh/players/1313.html"
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

# 创建BeautifulSoup对象
soup = BeautifulSoup(html, 'html.parser')

# 找到<table>标签
table = soup.find('table')

# 遍历<table>的所有<tr>标签
for row in table.find_all('tr'):
    # 找到当前行的<th>和<td>标签
    cells = row.find_all(['th', 'td'])
    column = cells[0].text.strip()
    value = cells[1].text.strip()
    
    # 打印列名和值
    print(column, value)