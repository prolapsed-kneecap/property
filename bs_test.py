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
html = """<span content="5500000" itemprop="price" class="styles-module-size_xxxl-A2qfi" data-marker="item-view/item-price">5&nbsp;500&nbsp;000<span itemprop="priceCurrency" content="RUB" class="styles-module-size_xxxl-A2qfi">&nbsp;₽&nbsp;</span></span>"""

soup = BeautifulSoup(html, 'html.parser')

need = {}


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
