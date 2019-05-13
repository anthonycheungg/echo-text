from googletrans import Translator

from bot.integrations import Integration


class DefineIntegration(Integration):
    USER_COMMAND_PREFIX = 'translate:'
    FRIENDLY_NAME = 'translate'

    def get_message_to_send(self, query):
        answer = google_translate(message)
        return answer


def google_translate(message):
    translator = Translator()
    answer = translator.translate(str(message))

    if answer.text:
        return f"Translation: {answer.text}"
    else:
        return f"Translation not found for {message}"
