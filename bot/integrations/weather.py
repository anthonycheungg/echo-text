from weather import Unit, Weather
from bot.integrations import Integration


class WeatherIntegration(Integration):
    USER_COMMAND_PREFIX = 'weather:'
    FRIENDLY_NAME = 'weather'

    def get_message_to_send(self, query):
        weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_location(query)

        if location:
            forecasts_array = location.forecast
            answer = construct_forecasts_from_weather_array(forecasts_array,
                                                            query)
        else:
            answer = f"No weather for {query}."

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

