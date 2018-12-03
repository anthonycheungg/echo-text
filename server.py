# Imports
import json

from flask import Flask, request
from googletrans import Translator
from twilio.twiml.messaging_response import MessagingResponse
from weather import Unit, Weather

import dictionary
import news
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

    if "weather:" in message:
        city = remove_from(message, "weather:")
        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location(city)

        if location:
            forecasts_array = location.forecast
            answer = construct_forecasts_from_weather_array(forecasts_array,
                                                            city)
        else:
            answer = f"No weather for {city}."

    elif "translate:" in message:
        message = remove_from(message, "translate:")
        answer = google_translate(message)

    elif "news" in message:
        query = remove_from(message, "news")
        answer = news.run()

    elif message == 'helpme':
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


def construct_forecasts_from_weather_array(forecasts_array, location):
    weather_result = f"Weather for {location} \n"
    for i in forecasts_array:
        if i is not None:
            weather_result += f"Condition: {i.text} \n"
            weather_result += f"Date: {i.date} \n"
            weather_result += f"High: {i.high} C \n"
            weather_result += f"Low: {i.low} C  \n"
            weather_result += '\n'
    return weather_result


def google_translate(message):
    translator = Translator()
    answer = translator.translate(str(message))

    if answer.text:
        return f"Translation: {answer.text}"
    else:
        return f"Translation not found for {message}"


def log_message(number, message):
    with open('responses.json', 'a') as file:
        log = {
            'phone_number': number,
            'message': message
        }
        file.write(json.dumps(log))
        file.close()


if __name__ == '__main__':
    app.run()
