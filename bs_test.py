from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
import requests
from time import sleep

html = """<ul class="list-group">
        <li class="list-group-item">
           <span class="strong">Name</span>
           <span class="pull-right">Piter</span>
        </li>
        <li class="list-group-item">
           <span class="strong">Year</span>
           <span class="pull-right">2017</span>
        </li>
 </ul>"""
html = """<span class="style-item-address__string-wt61A">Новосибирская обл., Новосибирск, Театральная ул., 9А</span>"""


html = open("what.txt", "r", encoding="utf-8").read()

soup = BeautifulSoup(html, 'html.parser')

need = {}


print(soup.find('span', class_="style-item-address__string-wt61A").contents[0])

def parameter_format(s):
    s = s.replace("\n", "")
    s = s.replace("\xa0", " ")
    s = s.replace("\x00", "")
    s = s.replace("&nbsp;", " ")
    return s


for li_tag in soup.find_all('ul', class_="params-paramsList-_awNW"):
    for span_tag in li_tag.find_all('li', class_="params-paramsList__item-_2Y2O"):
        field = parameter_format(span_tag.find('span', class_="styles-module-noAccent-nZxz7").text)
        value = parameter_format(span_tag.contents[-1])
        need[field] = value

price = parameter_format(soup.find('span', class_="styles-module-size_xxxl-A2qfi").contents[0])
print(price)

print(need)
