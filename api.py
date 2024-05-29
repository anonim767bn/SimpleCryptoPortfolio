from config import API_URL, PARAMETERS, HEADERS
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_api_data(url: str, parameters: dict, headers: dict) -> dict:
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return None

print(json.dumps(get_api_data(API_URL, PARAMETERS, HEADERS)['data'][0]['quote']['USD']['price'], indent=4))
