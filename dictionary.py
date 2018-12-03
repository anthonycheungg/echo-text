import os

import requests as r


class API():
    def __init__(self):
        pass

    def request(self, url):
        request = r.get(url)

        return request

    def parse_request(self, request, word):
        try:
            return request.json()[0]["shortdef"]
        except:
            return [f"Sorry, word: '{word}' was not found."]


class MerriamWebster(API):
    apikey = os.environ.get("DICTIONARY_API_TOKEN")

    def __call__(self, word):
        """
        Pass 'word' as the word you want to find.
        """
        return self.parse_request(self.request(
            "https://www.dictionaryapi.com/api/v3/"
            f"references/collegiate/json/{word}?key={self.apikey}"), word)


def run(word):

    dictionary = MerriamWebster()

    blacklist = "/\\.{}()[]<>.,?~1234567890*&^%$#@!`~'\"-_=+|:;"

    for char in blacklist:
        if char in word:
            return "That is not a word, please try with a real word."
            break

    definition = "\n\t\t".join(dictionary(word))

    return f"\n\t{word}:\n\t\t{definition}\n"
