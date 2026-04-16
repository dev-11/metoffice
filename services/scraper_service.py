import re
from datetime import datetime as dt

import bs4
import requests
import config as c


class ScraperService:
    def get_latest_forecast(self):
        page = requests.get(c.medical_meteorology_url)

        soup = bs4.BeautifulSoup(page.text, "html.parser")

        days = soup.select(c.anchor)

        results = []
        for day in days:
            front_type_el = day.select_one(c.front_type_class)
            date_el = day.select_one(c.date_class)
            temp_min_el = day.select_one(c.temp_min_class)
            temp_max_el = day.select_one(c.temp_max_class)

            if front_type_el and date_el and temp_max_el and temp_min_el:
                front_type = re.sub(r"\s+", " ", front_type_el.text.strip())
                date = re.sub(r"\s+", " ", date_el.text.strip())
                temp_max = re.sub(r"\s+", " ", temp_max_el.text.strip())
                temp_min = re.sub(r"\s+", " ", temp_min_el.text.strip())

                datetime = self.parse(date)

                results.append({
                    'target_date': datetime,
                    'data': {
                        'front_type': front_type,
                        'temp_min': temp_min,
                        'temp_max': temp_max,
                    }
                })

        return results

    @staticmethod
    def parse(date):
        month, day, day_of_week = date.split(' ')
        month = c.month_map[month]
        day = int(day[:-2])

        current_year = dt.now().year

        datetime = dt(current_year, month, day)
        return datetime.isoformat()
