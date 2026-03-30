import copy
from datetime import datetime, timezone


class ForecastService:
    @staticmethod
    def update_forecast(history, forecast):
        target_date = forecast["target_date"]
        front_type = forecast["front_type"]

        day = history.setdefault(target_date, {"target_date": target_date, "forecasts": []})
        if not day["forecasts"] or day["forecasts"][-1]["front_type"] != front_type:
            day["forecasts"].append({
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "front_type": front_type,
            })

        return day

    def update_forecasts(self, history, new_forecasts):
        results = copy.deepcopy(history)
        for f in new_forecasts:
            self.update_forecast(results, f)
        return results

    @staticmethod
    def current_forecast(history, target_date):
        forecasts = history.get(target_date)
        return forecasts[-1] if forecasts else None

    @staticmethod
    def did_change(history, target_date: str):
        return len(history.get(target_date, [])) > 1

    @staticmethod
    def change_count(history: dict, target_date: str):
        return max(0, len(history.get(target_date, [])) - 1)
