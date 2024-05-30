from config import API_URL, PARAMETERS, HEADERS
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_row_api_data(url: str, parameters: dict, headers: dict) -> dict:
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return {}

def get_data() -> dict:
    data = get_row_api_data(API_URL, PARAMETERS, HEADERS)
    result = []
    for i in range(len(data['data'])):
        result.append({
            'name' : data['data'][i]['name'],
            'symbol' : data['data'][i]['symbol'],
            'price' : data['data'][i]['quote']['USD']['price'],
            'timestamp' : data['status']['timestamp']
        })
    return result



# print(get_row_api_data(API_URL, PARAMETERS, HEADERS)['status'])
print(json.dumps(get_data(), indent=2))
