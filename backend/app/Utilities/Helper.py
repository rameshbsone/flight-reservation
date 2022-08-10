#!/usr/bin/env python3

from datetime import date, datetime, timedelta

from loguru import logger
from typing import Any

from app.Utilities import Constants
from fastapi import HTTPException


def CurrentDateTime(date_format="%Y-%m-%d %H:%M:%S"):
    _curr = datetime.now()
    _curr = datetime.strftime(_curr, date_format)
    return _curr


def CurrentDate(date_format="%Y-%m-%d"):
    _today = date.today()
    _currDate = datetime.strftime(_today, date_format)
    return _currDate

def RaiseHttpException(code: int, message: str, source: str, data: Any):
    dict_error = dict(source = source, error = message)
    if data is not None:
        logger.error(data)
    raise HTTPException(status_code = code, detail = dict_error)        


