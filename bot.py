# Imports
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Main function
# triggered by a POST request by ngrok
# when an SMS is received, Twilio will send the POST
@app.route('/sms', methods=['POST'])
def sms():
    """
    Use Twilio API to reply to texts
    """
    number = request.form['From']
    message = request.form['Body']      # text from SMS
    response = MessagingResponse()         # init a Twilio response
    print("Message obtained by {}:".format(number))
    print("{}".format(message))
    reply = formulate_reply(message)    # formulate answer to message
    print("Reply: {}".format(reply))
    response.message('Hi\n' + reply)  # text back
    return str(response)


def formulate_reply(message):
    """
    Identify keywords in message and relply accordingly through various APIs
    """
    message = message.lower().strip()  # reformate message
    answer = ""
    # identify keywords
    if "weather" in message:     # for weather requests
        message = remove_from(message, "weather")
        answer = weather_APIrequest(message)
    elif "wolfram" in message:   # for calculations
        message = remove_from(message, "wolfram")
        answer = wolfram_APIrequest(message)
    elif "wiki" in message:      # for wikipedia searches
        message = remove_from(message, "wiki")
        answer = wiki_APIrequest(message)
    # add more features here
    else:
        answer = "hello sir!"
    # limit to 1500 characters
    if len(answer) > 1500:
        answer = answer[0:1500] + "..."
    return answer


def remove_from(message, keyword):
    """
    Strip the message from the keyword
    """
    message = message.replace(keyword, '').strip()
    return message


def weather_APIrequest(message):
    """
    Tell the weather
    """
    pass


def wolfram_APIrequest(message):
    """
    Do math
    """
    # import wolframalpha
    # import os
    # answer = ""
    # # get API key from filename in directory API-keys/wolfram-alpha/
    # APIkey = os.listdir("API-keys/wolfram-alpha")[0]
    # try:
    #     client = wolframalpha.Client(APIkey)
    #     res = client.query(message)
    #     answer = next(res.results).text
    # except:
    #     answer = "No valid query for Wolfram|Alpha"
    # return answer
    pass

def wiki_APIrequest(message):
    """
    Be intellectual ;)
    """
    import wikipedia
    try:
        answer = wikipedia.summary(message)  # get summary from wikipedia
    except:
        # handle problems, that is degeneracy of answers
        answer = "Request was not found using Wikipedia. Be more specific?"
    return answer


if __name__ == '__main__':
    app.run()
