# Imports
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from weather import Weather, Unit
from googletrans import Translator

# Custom module
import dictionary

app = Flask(__name__)

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
    reply = formulate_reply(message)    
    print("Reply: {}".format(reply))
    response.message(reply)  
    return str(response)


def formulate_reply(message):
    """
    Identify keywords in message and reply accordingly through various APIs
    """
    message = message.lower().strip()  
    answer = "" 
   
    if "weather:" in message:     
        city = remove_from(message, "weather:")
        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location(city)

        if location:
            forecasts_array = location.forecast
            answer = construct_forecasts_from_weather_array(forecasts_array, city)
        else:
            answer = f"No weather for {city}."

    elif "wiki:" in message:     
        message = remove_from(message, "wiki:")
        answer = wikipedia_request(message)

    elif "translate:" in message:
        message = remove_from(message, "translate:")
        answer = google_translate(message)
    
    elif "define:" in message: 
        query = remove_from(message, "define:")
        answer = dictionary.run(query)

    else:
        answer = """
        Sorry, I don't understand. 

        You can use these commands:
        wiki: <article name>
        weather: <city>
        define: <word to define>
        """
    if answer:
        if len(answer) > 1500:
            answer = answer[0:1500] + "..."
    return answer

def remove_from(message, keyword):
    message = message.replace(keyword, '').strip()
    return message

def wikipedia_request(message):
    import wikipedia
    try:
        answer = wikipedia.summary(message) 
    except:
        # handle problems, that is degeneracy of answers
        answer = f"{message} could not be found on Wikipedia."
    return answer

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
    return answer.text

if __name__ == '__main__':
    app.run()