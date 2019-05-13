import os

from bot.integrations import Integration


class NewsIntegration(Integration):
    USER_COMMAND_PREFIX = 'news:'
    FRIENDLY_NAME = 'news'

    def get_message_to_send(self, query):
        news = NewsAPI()
        top_news = "\n".join(news())

        return top_news


class API():
    def __init__(self):
        pass

    def request(self, url):
        request = r.get(url)

        return request

    def parse_request(self, request, country):
        return [request.json()["articles"][0]["title"], request.json()["articles"][1]["title"], request.json()["articles"][2]["title"], request.json()["articles"][4]["title"], request.json()["articles"][5]["title"]]


class NewsAPI(API):
    apikey = os.environ.get("NEWS_API_TOKEN")

    def __call__(self, country="us"):
        return self.parse_request(self.request(f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={self.apikey}"), country)

