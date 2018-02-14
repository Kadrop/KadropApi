import requests
from bs4 import BeautifulSoup
import dicttoxml
import requests_cache
from datetime import timedelta

expire_after = timedelta(days=1)
requests_cache.install_cache(expire_after=expire_after)

XML_STRING = '<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel>{}</channel></rss>'
AMAZON_PRODUCT_URL = 'https://www.amazon.fr/gp/product/{}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}

s = requests.Session()


def get_amazon_data_from_id(amazon_id):
    url = AMAZON_PRODUCT_URL.format(amazon_id)
    print(url)
    return get_amazon_data_from_url(url=url)


def get_amazon_data_from_url(url):
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    title = clean_html_string(soup.find(id="productTitle").text)
    price = clean_html_string((soup.find(id="priceblock_ourprice") or soup.find(id="priceblock_saleprice")).text)
    image = clean_html_string(soup.find(id="landingImage")["data-old-hires"])

    return {
        "title": title,
        "price": price,
        "image": image,
        "url": url
    }


def format_data_into_xml(res):
    string_with_image = '<url>{}</url >< title >{}< / title >'.format(res["image"], "image")
    res["image"] = {}
    xml_string = dicttoxml.dicttoxml(res, attr_type=False, root=False, ).decode()
    xml_string_with_image = xml_string.format(string_with_image)
    return XML_STRING.format(xml_string_with_image)


def get_xml_from_url(url):
    data, img = get_amazon_data_from_url(url=url)
    return format_data_into_xml(data)


def clean_html_string(string):
    return " ".join(string.split())


if __name__ == "__main__":
    print(get_amazon_data_from_id("B00BWEI3O8"))
