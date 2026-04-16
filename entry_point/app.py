from services import ServiceFactory

import config as c


def lambda_handler(event, context):
    sf = ServiceFactory()

    storage_service = sf.get_storage_service()
    history = storage_service.get(c.data_file)

    if 'update_data' in event and parse_bool(event['update_data']):

        scraper_service = sf.get_scraper_service()
        latest_forecast = scraper_service.get_latest_forecast()

        forecast_service = sf.get_forecast_service()
        results = forecast_service.update_forecasts(history, latest_forecast)

        if results != history:
            storage_service.save_or_update(c.data_file, results)
            history = results

    time_service = sf.get_time_service()

    return {
        'forecast': time_service.to_local_time(history),
        'timestamp': time_service.now()
    }


def parse_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")
