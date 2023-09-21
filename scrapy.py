from decouple import config
import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36",
    "accept": "*/*",
}

URL = config("URL")
CSV_FILE = "softech.csv"


def get_response_data(headers, url):
    response = requests.get(url, headers=headers)
    return response


def content(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    all_data = soup.find_all("div", class_="product-thumb transition")
    laptop_content = []
    for i in all_data:
        laptop_content.append(
            {
                "price": i.find("div", class_="price").get_text().strip(),
                "name": i.find("div", class_="name").get_text().strip(),
                "image": i.find("img", class_="img-responsive").get("data-src"),
                "description": i.find("div", class_="description-small").get_text().strip()
            }
        )
    return laptop_content


def save_csv(laptops: list) -> None:
    with open(CSV_FILE, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Название", "Цена", "Картинка", "Характеристика"])
        for i in laptops:
            writer.writerow([i["name"], i["price"], i['image'], i["description"]])
    print("уусе!!!")


def execute():
    html_content = get_response_data(HEADERS, URL)
    if html_content.status_code == 200:
        laptops = content(html_content.text)
        save_csv(laptops)


execute()
