from flask import Flask, render_template
import requests
import time

# Astronomy API credentials and URL
api_key = "Basic MmI0YWMwYTAtMTcyZi00ZjM3LWFlMmMtYWM1ZGQyZjE2ODIzOjc0YmM5NTE3YTk1MWNiN2YzNTUwNzZkNzA4MjhiNWFkNWYwNDRmNDJmN2Y4M2U5NzIwODQwOTk2NTE4YWEzZDJjYTUzOGUxOWM5NzFkNDE0YjY2YzRjZmI4NDE1YjRlZTE0ZTk1ZDU2YTBjYzU5NTJlODdlOTkwYjAzYTk0NGFlZTg2MjFiODdmZDZkZTAwZWMzODA1NTQ5MGIzZjQ4ZDA5MjY2MWNhNjY2ZDIzOTk1Y2YzNmUwOTI5MmUzMzc5OTZmMWQ0NGJmNDdlM2IyNmUzOGQwZmE5YjViZTg2MTM4"
base_url = "https://api.astronomyapi.com/api/v2/bodies/positions"

# User's latitude and longitude
latitude = "40.78742071161268"  # Replace with your latitude
longitude = "-73.96868374977832"  # Replace with your longitude

app = Flask(__name__)


def get_formatted_date():
    now = time.localtime()
    return "{:04d}-{:02d}-{:02d}".format(now.tm_year, now.tm_mon, now.tm_mday)


def get_formatted_time():
    now = time.localtime()
    return "{:02d}:{:02d}:{:02d}".format(now.tm_hour, now.tm_min, now.tm_sec)


def call_astronomy_api():
    now = get_formatted_date()
    current_time = get_formatted_time()
    celestial_body_id = "moon"  # Replace with desired celestial body ID

    url = "{}?longitude={}&latitude={}&elevation=1&from_date={}&to_date={}&time={}".format(
        base_url, longitude, latitude, now, now, current_time
    )

    headers = {
        "Authorization": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        try:
            rows = response_json["data"]["table"]["rows"]
            for body in rows:
                if body["entry"]["id"] == celestial_body_id:
                    horizontal_info = body["cells"][0]["position"]["horizontal"]
                    altitude = horizontal_info["altitude"]["degrees"]
                    azimuth = horizontal_info["azimuth"]["degrees"]
                    return {"altitude": altitude, "azimuth": azimuth}
            else:
                return {"error": "Celestial body not found."}
        except KeyError:
            return {"error": "Failed to parse JSON response."}
    else:
        return {"error": "Error on HTTP request. HTTP code: {}".format(response.status_code)}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_moon_position')
def get_moon_position():
    position = call_astronomy_api()
    if "error" in position:
        return position["error"], 500
    else:
        return render_template('moon_position.html', altitude=position["altitude"], azimuth=position["azimuth"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
