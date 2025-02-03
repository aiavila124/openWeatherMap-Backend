from Utils.Response import ApiResponse
from Models.CitiesModel import CitiesModel
from Models.IconsModel import IconsModel
from http import HTTPStatus
from Utils.Tools.TypingTools import EventType
from Helpers.GeneralTools import get_input_data, process_dict_data
from Helpers.BasicHelper import BasicHelper
from Helpers.ProcessSql import ProcessSql
from typing import List
from datetime import datetime

ACTIVE = 1

class WeatherForecast:
    
    def __init__(self):
        self.process_sql = ProcessSql()
        self.bh = BasicHelper()

    def forecast_weather_by_city(self, event: EventType)->ApiResponse:
        
        """
        Retrieves weather forecast for a specified city.

        This function processes an event to extract the city ID, validates the existence 
        of the city, retrieves its geographical data, and then fetches the weather 
        forecast for that location using an external API. The response is processed 
        and returned as an ApiResponse.

        Args:
            event (EventType): The event object containing request data, including 
                the city ID for which the weather forecast is requested.

        Returns:
            ApiResponse: The response object containing the status code and the 
            weather data for the specified city.
        """

        request = get_input_data(event)

        self.bh.validate_if_does_not_exist(
            CitiesModel, 
            {'city_id': int(request['city_id'])},
        )

        city_data = self.process_sql.get_data(
            model=CitiesModel,
            request={
                'city_id': int(request['city_id'])
            },
            all_columns_except=['active', 'created_at', 'updated_at']
        )[0]

        lat = city_data['lat']
        lon = city_data['lng']

        weather = self.bh.open_weather_api(lat, lon)
        response = self.process_event_open_weather_response(weather)

        return ApiResponse(
            status_code=HTTPStatus.OK,
            data=response
        )
    
    def process_event_open_weather_response(self, data: List)->List:

        """
        Process the response from the Open Weather API into a standard format.

        This method takes the response from the Open Weather API and processes it 
        into a standard format which includes the timezone, current weather, 
        and the next 4 days of weather. The response is also translated into 
        Spanish.

        Args:
            data (List): The response from the Open Weather API.

        Returns:
            List: The processed response in a standard format.
        """
        icons_path = self.process_sql.get_data(
            model=IconsModel,
            all_columns_except=['active', 'created_at', 'updated_at']
        )

        icons_path = process_dict_data('code', 'path', icons_path)

        final_data = {
            "timezone":data['timezone'],
            "current": {
                **data['current'],
                "dt": datetime.fromtimestamp(data['current']['dt']).date().isoformat(),
                "sunrise": datetime.fromtimestamp(data['current']['sunrise']).date().isoformat(),
                "sunset": datetime.fromtimestamp(data['current']['sunset']).date().isoformat(),
                "weather": [
                    {
                        **weather,
                        "icon": icons_path[weather['icon']]
                        
                    } for weather in data['current']['weather']
                ]
            },
            "daily": [
                {
                    **row,
                    "dt": datetime.fromtimestamp(row['dt']).date().isoformat(),
                    "sunrise": datetime.fromtimestamp(row['sunrise']).date().isoformat(),
                    "sunset": datetime.fromtimestamp(row['sunset']).date().isoformat(),
                    "moonrise": datetime.fromtimestamp(row['moonrise']).date().isoformat(),
                    "moonset": datetime.fromtimestamp(row['moonset']).date().isoformat(),
                    "summary": self.bh.translate_service(row['summary'], 'ES'),
                    "weather": [
                        {
                            **weather,
                            "icon": icons_path[weather['icon']]
                            
                        } for weather in row['weather']
                    ]
                    
                }
                for row in data['daily']
            ][1:5]
        }

        return final_data
        
        

