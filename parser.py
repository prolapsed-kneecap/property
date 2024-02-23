import os
import random

from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter
import requests
from time import sleep

# from requests_ip_rotator import ApiGateway

# os.environ['AWS_ACCESS_KEY_ID'] = 'HHHAWLUB6FRW5000000'
# os.environ['AWS_SECRET_ACCESS_KEY'] = '0000KOuXmS00qVx+o1Ok/r000UgAGz9xd2000000'
# os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'

base_url = "https://www.avito.ru"
url = "https://www.avito.ru/all/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&p=6"

# gateway = ApiGateway(base_url)
# gateway.start()

proxy = {
    "https": 'https://74.235.186.115:3128',
    "http": 'https://35.233.244.31:3128'
}

# session = requests.session()
# # Tor uses the 9050 port as the default socks port
# session.proxies = {'http': 'socks5://127.0.0.1:9050',
#                    'https': 'socks5://127.0.0.1:9050'}
# print(session.get("http://httpbin.org/ip").text)

connect_list = ["US Central", "US East", "US West", "Canada East", "Canada West"]


def windscribe_random(action, connect_list=None):
    # Connect
    windscribe_cli_path = r"C:\\Program Files\\Windscribe\\windscribe-cli.exe"
    if connect_list is not None:
        location = random.choice(connect_list)
        location = "US Central"
        print(location)
        output = os.popen(f'"{windscribe_cli_path}" {action} {location}').read()
        print(output)

        # Write Log
        # log = os.path.join(os.getcwd(), "windscribe-log.txt")
        # log_datetime = f"{datetime.now():%Y-%m-%d %H:%M:%S} {output}"
        # log_datetime2 = "\n".join(["", log_datetime])
        # if os.path.isfile(log):
        # with open(log, "a") as f:
        # f.write(log_datetime2)
        # else:
        # with open(log, "w") as f:
        # f.write(log_datetime)
    else:
        os.popen(f'"{windscribe_cli_path}" {action}')


def make_session():
    windscribe_random("connect", connect_list)
    s = requests.Session()
    s.mount('https://', HTTP20Adapter())
    return s
    # session = requests.session()
    # # Tor uses the 9050 port as the default socks port
    # session.proxies = {'http': 'socks5://127.0.0.1:9050',
    #                    'https': 'socks5://127.0.0.1:9050'}
    # return session


# def get_tor_session():
#     session = requests.session()
#     # Tor uses the 9050 port as the default socks port
#     session.proxies = {'http': 'socks5://127.0.0.1:9050',
#                        'https': 'socks5://127.0.0.1:9050'}
#     return session


def make_request(s, q="Москва"):
    # return s.get(url + f"&q={q}")
    print(url + f"&q={q}")
    return s.get(url + f"&q={q}")


s = make_session()
# q = input("Город: ")
request = make_request(s)

in_file = set()


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


def parse(r):
    ck = 0

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
        location = parameter_format(params_bs.find('span', class_="style-item-address__string-wt61A").contents[0])
        param_value["Расположение"] = location
        for li_tag in params_bs.find_all('ul', class_="params-paramsList-_awNW"):
            for span_tag in li_tag.find_all('li', class_="params-paramsList__item-_2Y2O"):
                field = parameter_format(span_tag.find('span', class_="styles-module-noAccent-nZxz7").text)
                value = parameter_format(span_tag.contents[-1])
                param_value[field] = value
        return param_value

    out = open("moscow.txt", "r+", encoding="utf-8")

    for i in out.readlines():
        in_file.add(i)

    def link_in_file(l):
        return l in in_file

    def update_session():
        s = make_session()

    # what = open("what.txt", "w+", encoding="utf-8")

    def write_link_and_params(l, params, f=False):
        # if not link_in_file(l):
        out.write(str(l) + "\n")
        out.write(str(params) + "\n")

    def parse_link(link, f=False):
        if f:
            update_session()
        try:
            in_file.add(link)
            s.proxies.update()
            print(link)
            print(get_params_by_link(link))
            write_link_and_params(link, get_params_by_link(link))
            print("Written successfully!")
        except:
            print(bs.find("title").text)
            parse_link(link, True)

    links = get_links(r)[1:]
    print(r)
    for link in links:
        if not link_in_file(link):
            parse_link(link)

    # print("каво")
    # print(bs.prettify(encoding="utf-8"))
    # what.write(str(bs.prettify(encoding="utf-8")))
    # print("каво")
    return -1


while True:
    while request.status_code == 429:
        print("Ошибка 429")
        sleep(300)
        s = make_session()
        request = make_request(s)
    parse(request)
    # try:
    #     parse(request)
    # except:
    #     print("Пустые параметры!")
    #     # s = make_session()
    #     # request = make_request(s)
    #     continue
