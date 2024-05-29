from dotenv import load_dotenv
import os

load_dotenv()

API_URL='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PARAMETERS = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}

HEADERS = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.getenv('X-CMC_PRO_API_KEY'),
}

def get_db_url() -> str:
    load_dotenv()
    PG_VARS = 'PG_HOST', 'PG_PORT', 'PG_USER', 'PG_PASSWORD', 'PG_DBNAME'
    credentials = {var: os.environ.get(var) for var in PG_VARS}
    return 'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'.format(**credentials)