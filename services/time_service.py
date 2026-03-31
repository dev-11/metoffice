from datetime import datetime as dt


class TimeService:
    def __init__(self, timezone):
        self._timezone = timezone

    def to_local_time(self, results):
        return [{**day, "forecasts": self._convert_forecasts(day["forecasts"])} for day in results]

    def _convert_forecasts(self, forecasts):
        return [
            {**f, "observed_at": dt.fromisoformat(f["observed_at"]).astimezone(self._timezone).isoformat()}
            for f in forecasts
        ]

    def now(self):
        return dt.now(self._timezone).isoformat()
