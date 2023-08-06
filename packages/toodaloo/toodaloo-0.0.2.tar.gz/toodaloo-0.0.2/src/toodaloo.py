import requests
import datetime

class Toodaloo:
    def __init__(self, project_1_url):
        self.project_1_url = project_1_url

    def send_data_to_toodaloo(self, message, timestamp, ip_address):
        payload = {
            'message': message,
            'timestamp': timestamp,
            'ip_address': ip_address
        }

        try:
            response = requests.get(self.project_1_url, params=payload)
            response.raise_for_status()  # Raise an exception for any error status codes
            print("Data sent to Toodaloo successfully!")
        except requests.exceptions.RequestException as err:
            print(f"Failed to send data to Toodaloo: {err}")

    def track_user_message(self, message, ip_address):
        timestamp = datetime.datetime.now().isoformat()
        self.send_data_to_toodaloo(message, timestamp, ip_address)

    def track_ai_response(self, response, ip_address):
        timestamp = datetime.datetime.now().isoformat()
        self.send_data_to_toodaloo(response, timestamp, ip_address)
