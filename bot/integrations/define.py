import dictionary
from bot.integrations import Integration


class DefineIntegration(Integration):
    USER_COMMAND_PREFIX = 'define:'
    FRIENDLY_NAME = 'define'

    def get_message_to_send(self, query):
        answer = dictionary.run(query)
        return answer
