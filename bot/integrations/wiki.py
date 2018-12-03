import wikipedia
from bot.integrations import Integration


class WikiIntegration(Integration):
    USER_COMMAND_PREFIX = 'wiki:'
    FRIENDLY_NAME = 'wikipedia'

    def get_message_to_send(self, query):
        try:
            answer = wikipedia.summary(query)
        except:
            answer = f"{query} could not be found on Wikipedia."
        return answer
