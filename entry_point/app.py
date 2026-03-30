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
    scraper_service = sf.get_scraper_service()
    latest_forecast = scraper_service.get_latest_forecast()

    # forecast_service = sf.get_forcast_service()
    # forecast_service.update_forecast(latest_forecast)

    storage_service = sf.get_storage_service()
    is_saved = storage_service.save_or_update(c.data_file, latest_forecast)

    forecasts = storage_service.get(c.data_file) if is_saved else {}

    return {
        'forecast': forecasts,
        'timestamp': dt.now().isoformat()
    }


def parse_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")
