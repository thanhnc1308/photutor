from datetime import datetime, timedelta


def subtract_days(date, days):
    return date - timedelta(days=days)


def format_date(date, format_string="%m/%d/%Y"):
    return date.strftime(format_string)


def parse_date(date_str, format_string='%d/%m/%Y'):
    return datetime.strptime(date_str, format_string)
