import re

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
        datetime_el = day.select_one(c.datetime_class)

        if front_type_el and datetime_el:
            front_type = front_type_el.text.strip()
            datetime = re.sub(r"\s+", " ", datetime_el.text.strip())

            results.append((front_type, datetime))

    return {
        'statusCode': 200,
        'body': results
    }
