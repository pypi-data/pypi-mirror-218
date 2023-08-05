from datetime import date, timedelta

from .holidays import HOLIDAYS


class InvalidDateError(Exception):
    pass


def is_business_day(date_param):
    date_param = _parse_date(date_param)
    weekend = [5, 6]  # Sat,Sun
    wday = date_param.weekday()
    year = str(date_param.year)

    return not (wday in weekend or date_param in HOLIDAYS[year].values())


def add_business_days(business_days, since):
    since = _parse_date(since)

    last_date = None
    counter = 1
    while business_days > 0:
        last_date = since + timedelta(days=counter)
        counter += 1

        if not is_business_day(last_date):
            continue

        business_days -= 1

    return last_date


def is_past_due(due_date, current_date):
    due_date = _parse_date(due_date)
    current_date = _parse_date(current_date)

    if not is_business_day(due_date):
        due_date = add_business_days(1, due_date)

    return current_date > due_date


def get_holiday(holiday_date):
    date_param = _parse_date(holiday_date)
    year = str(date_param.year)

    holiday_name = None

    for holiday, hdate in HOLIDAYS[year].items():
        if hdate == date_param:
            holiday_name = holiday
            break

    return holiday_name


def _parse_date(param):
    if isinstance(param, date):
        return param

    if not type(param) is str:
        raise InvalidDateError(f"{param} is not a valid date")

    if param.find("/") != -1:
        str_date = "-".join(reversed(param.split("/")))
    else:
        str_date = param

    return date.fromisoformat(str_date)
