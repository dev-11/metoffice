from datetime import datetime, timezone


class ForecastService:
    @staticmethod
    def update_forecast(day, forecast):
        data = forecast["data"]
        if not day["forecasts"] or day["forecasts"][-1]["data"] != data:
            day["forecasts"].append({
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "data": data,
            })
        return day

    def update_forecasts(self, history, new_forecasts):
        results = list(history)

        for f in new_forecasts:
            target_date = f["target_date"]
            day = next((d for d in results if d["target_date"] == target_date), None)
            if day is None:
                day = self.empty_forecast(target_date)
                results.append(day)

            self.update_forecast(day, f)

        return results

    @staticmethod
    def empty_forecast(day):
        return {"target_date": day, "forecasts": []}

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
