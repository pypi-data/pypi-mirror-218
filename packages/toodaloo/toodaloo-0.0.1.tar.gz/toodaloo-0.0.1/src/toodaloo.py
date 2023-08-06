import requests
import datetime

def send_data_to_toodaloo(message, timestamp, ip_address):
    payload = {
        'message': message,
        'timestamp': timestamp,
        'ip_address': ip_address
    }

    url = 'https://project-1.thibaultjaigu.repl.co'

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for any error status codes
        print("Data sent to Toodaloo successfully!")
    except requests.exceptions.RequestException as err:
        print(f"Failed to send data to Toodaloo: {err}")


class Toodaloo:
    def __init__(self, project_1_url):
        self.project_1_url = project_1_url

    def track_user_message(self, message, ip_address):
        timestamp = datetime.datetime.now().isoformat()
        send_data_to_toodaloo(message, timestamp, ip_address)

    def track_ai_response(self, response, ip_address):
        timestamp = datetime.datetime.now().isoformat()
        send_data_to_toodaloo(response, timestamp, ip_address)


# Initialize the Toodaloo instance with project_1_url
project_1_url = 'https://project-1.thibaultjaigu.repl.co/'
tracker = Toodaloo(project_1_url)
