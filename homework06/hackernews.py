from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    label, _id = request.query.label, request.query.id

    s = session()

    item = s.query(News).filter(News.id == _id).first()

    item.label = label

    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    s = session()

    for i in filter(
        lambda x: s.query(News)
        .filter(News.title == x["title"])
        .filter(News.author == x["author"])
        .first()
        is None,
        get_news("https://news.ycombinator.com/newest", 1),
    ):
        s.add(
            News(
                title=i["title"],
                author=i["author"],
                url=i["url"],
                comments=i["comments"],
                points=i["points"],
            )
        )
    s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
