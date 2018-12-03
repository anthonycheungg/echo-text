class Integration():
    USER_COMMAND_PREFIX = None
    FRIENDLY_NAME = None

    def get_message_to_send(self, query):
        raise NotImplementedError


def get_all_supported_integrations():
    from bot.integrations.define import DefineIntegration
    from bot.integrations.wiki import WikiIntegration

    return (
        DefineIntegration,
        WikiIntegration
    )
