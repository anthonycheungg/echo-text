import requests as r

class API():
    def __init__(self):
        pass

    def request(self, url):
        request = r.get(url)

        return request

    def parse_request(self, request, country):
        return [request.json()["articles"][0]["title"], request.json()["articles"][1]["title"], request.json()["articles"][2]["title"], request.json()["articles"][4]["title"], request.json()["articles"][5]["title"]]


class NewsAPI(API):
    apikey = "e8f9338f21294de983fe006aaa4e4742"

    def __call__(self, country="us"):
        return self.parse_request(self.request(f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={self.apikey}"), country)

def run():

    news = NewsAPI()

    # top_news = "\n".join(news()['articles'])

    top_news = "\n".join(news())

    return top_news

