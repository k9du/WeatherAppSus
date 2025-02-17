import sys
import requests
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

load_dotenv()

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENPOLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
OPENWA_KEY = os.getenv('OPENWA_KEY')


class CitySearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("City Search")
        self.setGeometry(200, 200, 300, 250)
        self.setStyleSheet("font-size: 15px;")

        layout = QVBoxLayout()

        self.label = QLabel("Enter city name:")
        layout.addWidget(self.label)

        self.city_input = QLineEdit()
        layout.addWidget(self.city_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_city)
        layout.addWidget(self.search_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def search_city(self):
        city_name = self.city_input.text().strip()
        if not city_name:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        weather_data = self.get_weather(city_name)
        if weather_data is None:
            QMessageBox.critical(self, "Error", f"City '{city_name}' not found in OpenWeatherMap.")
            return

        # Extract lat/lon from weather data
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]

        air_quality_data = self.get_air_quality(lat, lon)

        if air_quality_data is None:
            QMessageBox.critical(self, "Error", f"No air quality data found for '{city_name}'.")
            return

        # Build result text
        result_text = f"Results for {city_name}:\n"
        if weather_data:
            temp = weather_data["main"]["temp"] - 273.15
            description = weather_data["weather"][0]["description"]
            result_text += f"🌡 Temperature: {temp:.1f}°C\n☁️ Weather: {description}\n"
        else:
            result_text += "❌ Weather data not found.\n"

        if air_quality_data:
            aqi_value = air_quality_data["list"][0]["main"]["aqi"] 
            pm2_5_value = air_quality_data["list"][0]["components"]["pm2_5"]
            result_text += f"🌬 Air Quality (1-5): {aqi_value}\n 🦠 PM2.5: {pm2_5_value}"
        else:
            result_text += "❌ Air quality data not found.\n"

        self.result_label.setText(result_text)

    def get_weather(self, city_name):
        response = requests.get(f"{OPENWEATHER_URL}?q={city_name}&appid={OPENWA_KEY}")
        return response.json() if response.status_code == 200 else None

    def get_air_quality(self, lat, lon):
        response = requests.get(f"{OPENPOLLUTION_URL}?lat={lat}&lon={lon}&appid={OPENWA_KEY}")
        return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CitySearchApp()
    window.show()
    sys.exit(app.exec())

