from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from bot.integrations import get_all_supported_integrations


app = Flask(__name__)


@app.route('/')
def index():
    return ('<h1> Echo Text </h1> <p> This is the web server for Echo Text.'
            'You can text it at 604 259 1114 </p>')


@app.route('/sms', methods=['POST'])
def sms():
    """
    Use Twilio API to reply to texts
    """
    number = request.form['From']
    message = request.form['Body']
    response = MessagingResponse()

    print("Message obtained by {}:".format(number))
    print("{}".format(message))
    log_message(number, message)

    reply = formulate_reply(message)
    print("Reply: {}".format(reply))
    response.message(reply)
    return str(response)


def formulate_reply(message):
    message = message.lower().strip()
    answer = ""

    for integration in get_all_supported_integrations():
        if integration.USER_COMMAND_PREFIX in message:
            query = remove_from(message, integration.USER_COMMAND_PREFIX)
            try:
                answer = integration().get_message_to_send(query)
            except NotImplementedError:
                answer = f'{integration.USER_COMMAND_PREFIX} is not supported.'

    if message == 'helpme':
        answer = """
        You can use these commands:
        wiki: <article name>
        weather: <city>
        define: <word to define>
        news
        translate: <translate to english>
        """

    if not answer:
        answer = """
        Sorry, I don't understand.

        You can use these commands:
        wiki: <article name>
        weather: <city>
        define: <word to define>
        news
        translate: <translate to english>
        """

    if answer:
        if len(answer) > 1500:
            answer = answer[0:1500] + "..."
    return answer


def remove_from(message, keyword):
    message = message.replace(keyword, '').strip()
    return message


if __name__ == '__main__':
    app.run()
