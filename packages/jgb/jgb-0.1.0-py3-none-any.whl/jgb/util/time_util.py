#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import datetime as dt
import time

tz_bj = dt.timezone(dt.timedelta(hours=8))

FMT_DATE = "%Y-%m-%d"
FMT_DATE1 = "%Y/%m/%d"
FMT_DATETIME = "%Y-%m-%d %H:%M:%S"


def format_seconds(st):
    hours, remainder = divmod(st, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, sub_seconds = divmod(remainder, 1)

    s = "{:02}:{:02}:{:02},{:03}".format(int(hours), int(minutes), int(seconds), int(sub_seconds * 1000))
    return s


def now_str():
    return dt.datetime.now().strftime(FMT_DATETIME)


def next_day(date: dt.datetime) -> dt.datetime:
    return date + dt.timedelta(days=1)


def prev_day(date: dt.datetime) -> dt.datetime:
    return date - dt.timedelta(days=1)


def today_obj() -> dt.datetime:
    now = dt.datetime.now(tz=tz_bj)
    return now.replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=None)


def yesterday_obj() -> dt.datetime:
    return prev_day(today_obj())


def now_unix():
    return int(time.mktime(dt.datetime.now().timetuple()))


def now_unix_ms():
    return int(round(time.time() * 1000))


def cvt_str2ts(time_str, str_format=FMT_DATETIME):
    return int(time.mktime(time.strptime(time_str, str_format)))


def cvt_ts2dt(unix_ts):
    return dt.datetime.fromtimestamp(unix_ts)


def cvt_ts2str(unix_ts, str_format=FMT_DATETIME):
    return cvt_ts2dt(unix_ts).strftime(str_format)


def cvt_dt2ts(datetime):
    return time.mktime(datetime.timetuple())


def day_begin_sec(unix_ts):
    today = cvt_ts2dt(unix_ts).date()
    return int(time.mktime(today.timetuple()))


if __name__ == "__main__":
    now = dt.datetime.now()
    timestamp = cvt_str2ts(cvt_ts2str(now_unix()))
    print(timestamp)
    print(cvt_ts2dt(day_begin_sec(timestamp)))
    print(cvt_ts2str(timestamp))

    print(today_obj())
    print(yesterday_obj())
    print(type(today_obj()))
    print(dt.timedelta(days=1).total_seconds())

    print(cvt_dt2ts(dt.date.today()))
