import requests


class WeatherData:
    def __init__(self):
        self.temperature: int = 0
        self.humidity: int = 0
        self.wind_speed: int = 0

    def set_data(self, temperature, humidity, wind_speed) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

    def get_data(self) -> dict:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
        }


class WeatherConnection:
    def __init__(self, weather_data):
        self.city = "São Paulo"
        self.base_url = "https://wttr.in"
        self.weather_data = weather_data

    def connection(self):
        url = f"{self.base_url}/{self.city}?format=j1"
        try:
            response = requests.get(url)
            response.raise_for_status() 

            data = response.json()

            condition = data["current_condition"][0]
            temp = int(condition["FeelsLikeC"])
            humidity = int(condition["humidity"])
            wind_speed = int(condition["windspeedKmph"])

            self.weather_data.set_data(temp, humidity, wind_speed)
            return self.weather_data.get_data()

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar API: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Erro ao processar os dados recebidos: {e}")
            return None


class WeatherAPI:
    def __init__(self) -> None:
        self.weather_data = WeatherData()
        self.weather_connection = WeatherConnection(self.weather_data)
        self.user_input = None

    @staticmethod
    def run(app):
        app.user_input = input("Your city: ")
        app.weather_connection.city = app.user_input

        connect = app.weather_connection.connection()
        if connect:
            print(f"\033[1;33m🌡️     Temperature: {app.weather_data.temperature}°C\033[0m")
            print(f"\033[1;33m🌬     Wind speed: {app.weather_data.wind_speed} km/h\033[0m")
            print(f"\033[1;33m💧    Humidity: {app.weather_data.humidity}%\033[0m")
        else:
            print("\033[1;31m❌     Failed to retrieve weather data.\033[0m")
