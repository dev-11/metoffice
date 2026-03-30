from datetime import datetime as dt
from datetime import timezone
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

    # [
    #     {
    #         "front_type": "Nincs front",
    #         "date": "2026-03-30T00:00:00"
    #     },
    #     {
    #         "front_type": "Nincs front",
    #         "date": "2026-03-31T00:00:00"
    #     }
    # ]

    result = record_forecast([], latest_forecast[0]["target_date"], latest_forecast[0]["front_type"])

    # [
    #     {
    #         "target_date": "2026-03-31",
    #         "forecasts": [
    #             {"observed_at": "2026-03-30T08:00:00Z", "front_type": "cold_front"},
    #             {"observed_at": "2026-03-30T14:00:00Z", "front_type": "warm_front"},
    #             {"observed_at": "2026-03-31T08:00:00Z", "front_type": "no_front"}
    #         ]
    #     }
    # ]

    # forecast_service = sf.get_forcast_service()
    # forecast_service.update_forecast(latest_forecast)

    # storage_service = sf.get_storage_service()
    # is_saved = storage_service.save_or_update(c.data_file, latest_forecast)
    #
    # forecasts = storage_service.get(c.data_file) if is_saved else {}

    return {
        'forecast': result,
        'timestamp': dt.now().isoformat()
    }


def record_forecast(history: list, target_date: str, front_type: str, observed_at: str = None):
    """Add a forecast snapshot if the front_type has changed."""
    if observed_at is None:
        observed_at = dt.now(timezone.utc).isoformat()

    day = next((d for d in history if d["target_date"] == target_date), None)

    if day is None:
        day = {"target_date": target_date, "forecasts": []}
        history.append(day)

    last = day["forecasts"][-1] if day["forecasts"] else None
    if last is None or last["front_type"] != front_type:
        day["forecasts"].append({"observed_at": observed_at, "front_type": front_type})

    return history


def parse_bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")
