from Classes.WeatherForecast import WeatherForecast
from Utils.Authorizer import authorizer

@authorizer 
def forecast_weather_by_city(event, context):
    class_ = WeatherForecast()
    methods = {
        "GET": class_.forecast_weather_by_city,
    }
    method_to_run = methods[event['httpMethod']]
    return method_to_run(event)
