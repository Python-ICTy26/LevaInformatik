import typing as tp

import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser: BeautifulSoup) -> tp.List[tp.Dict[str, tp.Any]]:
    """
    Парсит html страничку, выделяет оттуда новости
    для каждой из них создает словарь с параметрами
    заголовок, автор, кол-во комментриев
    Возвращает список подобных словарей
    """
    news_list = []
    titles = parser.findAll("span", {"class": "titleline"})
    sublines = parser.findAll("span", {"class": "subline"})

    for t, s in zip(titles, sublines):
        item = {
            "title": t.find("a").text,
            "author": s.find("a", {"class": "hnuser"}).text,
            "url": t.find("a")["href"],
            "points": int(s.find("span", {"class": "score"}).text.split()[0]),
            "comments": s.findAll("a")[-1].text.split()[0],
        }
        item["comments"] = int(item["comments"]) if item["comments"].isdigit() else 0
        news_list.append(item)

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    """
    Возвращает ссылку на следующую страницу новостей

    На сайте, кнопка, которая содержит в себе эту
    ссылку описана таким html кодом:
        <a href="?p=2" class="morelink" rel="next">More</a>

    Поэтому мы получаем объект типа <a> такой, что
    его класс == morelink и берем у него параметр href

    В  данном случае href будет не полноценной ссылкой,
    а параметром get запроса, поэтому в функции get_news
    он прибавляется к основному адресу сайта
    """
    return parser.find("a", {"class": "morelink"})["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
