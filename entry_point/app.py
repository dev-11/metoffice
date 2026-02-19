import re
from datetime import datetime as dt

import bs4
import requests
import config as c


def lambda_handler(event, context):

    page = requests.get(c.medical_meteorology_url)

    soup = bs4.BeautifulSoup(page.text, "html.parser")

    days = soup.select(c.anchor)

    results = []
    for day in days:
        front_type_el = day.select_one(c.front_type_class)
        date_el = day.select_one(c.date_class)

        if front_type_el and date_el:
            front_type = front_type_el.text.strip()
            date = re.sub(r"\s+", " ", date_el.text.strip())

            datetime = parse(date)

            results.append({'front_type': front_type, 'date': datetime})

    return {
        'forecast': results,
        'timestamp': dt.now().isoformat()
    }


def parse(date):
    month, day, day_of_week = date.split(' ')
    month = c.month_map[month]
    day = int(day[:-2])

    current_year = dt.now().year

    datetime = dt(current_year, month, day)
    return datetime.isoformat()
