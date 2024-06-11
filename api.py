from config import API_URL, PARAMETERS, HEADERS
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, HTTPError
import json
import logging

logger = logging.getLogger(__name__)


def get_row_api_data(url: str, parameters: dict, headers: dict) -> dict:
    session = Session()
    session.headers.update(headers)
    data = {}
    try:
        response = session.get(url, params=parameters)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        logger.error(f"Network-related error occurred: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    except HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
    return data


def get_data() -> list:
    data = get_row_api_data(API_URL, PARAMETERS, HEADERS)
    result = []
    if 'data' in data and 'status' in data:
        for item in data['data']:
            if 'name' in item and 'symbol' in item and 'quote' in item and 'USD' in item['quote'] and 'price' in item['quote']['USD']:
                result.append({
                    'name': item['name'],
                    'symbol': item['symbol'],
                    'price': item['quote']['USD']['price'],
                    'timestamp': data['status']['timestamp']
                })
    else:
        logger.error("Data missing essential keys")
    return result
