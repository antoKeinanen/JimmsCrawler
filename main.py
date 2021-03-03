import requests
from bs4 import BeautifulSoup


def get_gpus():
    # 3080  https://www.jimms.fi/fi/Product/List/000-1SZ/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-3080?i=100&ob=6
    URL = "https://www.jimms.fi/fi/Product/List/000-1T0/komponentit--naytonohjaimet--geforce-rtx-pelaamiseen--rtx-3090?i=100&ob=6"
    p = requests.get(URL)

    soup = BeautifulSoup(p.content, "html.parser")
    res = soup.find_all(class_="p_col_info")

    col_info = str(res)

    soup = BeautifulSoup(col_info, "html.parser")

    gpus = []
    for a in soup.find_all("a", href=True):
        a = str(a).removeprefix("<a href=\"")
        a = a.split("\"")
        a[0] = "https://www.jimms.fi" + a[0]
        gpus.append(a[0])

    return gpus


def get_stock(url):
    p = requests.get(url)
    soup = BeautifulSoup(p.content, "html.parser")
    res = soup.find(class_="whqty")
    res = str(res).removeprefix("<div class=\"whqty\">")
    res = res.removesuffix(" kpl</div>")
    try:
        res = int(res)
        return [[res, url]]
    except ValueError:
        res = res.removeprefix("yli ")
        res = int(res)
        return [[res, url]]


if __name__ == '__main__':
    gpus = get_gpus()
    i = 0
    for gpu in gpus:
        print(get_stock(gpu)[0])

