from datetime import datetime as dt
from services import ServiceFactory

import config as c


def lambda_handler(event, context):
    # headers = event["params"]["header"]
    sf = ServiceFactory()

    # scrape_data = (
    #     parse_bool(headers[c.scrape_data_header_key])
    #     if c.scrape_data_header_key in headers
    #     else False
    # )
    # if scrape_data:
    ss = sf.get_scraper_service()
    latest_forecast = ss.get_latest_forecast()

    return {
        'forecast': latest_forecast,
        'timestamp': dt.now().isoformat()
    }


def parse_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")
