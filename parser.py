from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
import requests
from time import sleep

#from requests_ip_rotator import ApiGateway

# os.environ['AWS_ACCESS_KEY_ID'] = 'HHHAWLUB6FRW5000000'
# os.environ['AWS_SECRET_ACCESS_KEY'] = '0000KOuXmS00qVx+o1Ok/r000UgAGz9xd2000000'
# os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

base_url = "https://www.avito.ru"
url = "https://www.avito.ru/all/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p=2"

# gateway = ApiGateway(base_url)
# gateway.start()

proxy = {
    "https": 'https://74.235.186.115:3128',
    "http": 'https://35.233.244.31:3128'
}

s = requests.Session()
s.mount('https://', HTTP20Adapter())
request = s.get(url)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def parse(r):
    def get_bs_by_request(r):
        return BeautifulSoup(r.text, "html.parser")

    bs = get_bs_by_request(r)

    def get_links(r):
        return [base_url + i["href"] for i in
                bs.find_all("a", class_="styles-module-root-QmppR styles-module-root_noVisited-aFA10")]

    def parameter_format(s):
        s = s.replace("\n", "")
        s = s.replace("\xa0", " ")
        s = s.replace("\x00", "")
        return s

    def get_params_by_link(l):
        params_request = s.get(l)
        params_bs = get_bs_by_request(params_request)
        param_value = {}
        price = parameter_format(params_bs.find('span', class_="styles-module-size_xxxl-A2qfi").contents[0])
        param_value["Цена"] = price
        for li_tag in params_bs.find_all('ul', class_="params-paramsList-_awNW"):
            for span_tag in li_tag.find_all('li', class_="params-paramsList__item-_2Y2O"):
                field = parameter_format(span_tag.find('span', class_="styles-module-noAccent-nZxz7").text)
                value = parameter_format(span_tag.contents[-1])
                param_value[field] = value
        return param_value

    out = open("data.txt", "r+", encoding="utf-8")

    in_file = set()
    for i in out.readlines():
        in_file.add(i)

    def link_in_file(l):
        return l in in_file

    def write_link_and_params(l, params):
        if not link_in_file(l):
            out.write(str(l) + "\n")
            out.write(str(params) + "\n")

    links = get_links(r)[1:]
    print(r)
    for link in links:
        s.proxies.update()
        print(link)
        print(get_params_by_link(link))
        write_link_and_params(link, get_params_by_link(link))
    print("Written successfully!")


while True:
    while request.status_code == 429:
        print("Ошибка 429")
        sleep(180)
        request = s.get(url)
    try:
        parse(request)
    except:
        break

