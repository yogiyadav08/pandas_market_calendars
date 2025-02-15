import datetime

import pandas as pd
import pytz

from pandas_market_calendars.calendars.bmf import BMFExchangeCalendar


def test_time_zone():
    assert BMFExchangeCalendar().tz == pytz.timezone("America/Sao_Paulo")


def test_2020_holidays_skip():
    # 2020-07-09 - skipped due to covid
    # 2020-11-20 - skipped due to covid
    holidays = BMFExchangeCalendar().holidays().holidays
    for date in ["2019-07-09", "2019-11-20", "2021-07-09", "2021-11-20"]:
        assert pd.Timestamp(date, tz="UTC").to_datetime64() in holidays
    for date in ["2020-07-09", "2020-11-20"]:
        assert pd.Timestamp(date, tz="UTC").to_datetime64() not in holidays


def test_post_2022_regulation_change():
    # Regional holidays no longer observed: January 25th, July 9th, November 20th
    holidays = BMFExchangeCalendar().holidays().holidays

    for year in [2017, 2018, 2019, 2021]:  # skip 2020 due to test above
        for month, day in [(1, 25), (7, 9), (11, 20)]:
            assert (
                pd.Timestamp(datetime.date(year, month, day), tz="UTC").to_datetime64()
                in holidays
            )

    for year in range(2022, 2040):
        for month, day in [(1, 25), (7, 9), (11, 20)]:
            assert (
                pd.Timestamp(datetime.date(year, month, day), tz="UTC").to_datetime64()
                not in holidays
            )
