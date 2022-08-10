from typing import Callable
from fastapi import FastAPI
from app.Utilities import Constants

from loguru import logger
import sqlite3
import configparser


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        ReadConfiguration()
    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        pass
    return stop_app

def ReadConfiguration():
    cfg = configparser.ConfigParser()
    config_file = f"{Constants.CLIENT_FOLDER_PATH}/app.env"
    logger.info(config_file)
    cfg.read(config_file)

    # [APP]
    Constants.NPCI_API_ROOT_URL = cfg[Constants.CONFIG_APP]["NPCI_API_ROOT_URL"]
    Constants.NPCI_API_VERSION = cfg[Constants.CONFIG_APP]["NPCI_API_VERSION"]
    Constants.NPCI_API_URN = cfg[Constants.CONFIG_APP]["NPCI_API_URN"]
    Constants.NPCI_GET_TRANSACTIONS_LIST = cfg[Constants.CONFIG_APP]["NPCI_GET_TRANSACTIONS_LIST"]
    Constants.NPCI_FETCH_TRANSACTION = cfg[Constants.CONFIG_APP]["NPCI_FETCH_TRANSACTION"]
    Constants.NPCI_RAISE_COMPLAINT = cfg[Constants.CONFIG_APP]["NPCI_RAISE_COMPLAINT"]
    Constants.NPCI_CHECK_TRANSACTION_STATUS = cfg[Constants.CONFIG_APP]["NPCI_CHECK_TRANSACTION_STATUS"]
    Constants.CALL_NPCI_API = cfg[Constants.CONFIG_APP]["CALL_NPCI_API"]
    Constants.CALL_NPCI_API = (str.lower(Constants.CALL_NPCI_API) == "true")
    logger.info(Constants.CALL_NPCI_API)
    Constants.UDIR_RESPONSE_TIMEOUT = cfg[Constants.CONFIG_APP]["UDIR_RESPONSE_TIMEOUT"]
    Constants.UDIR_RESPONSE_TIMEOUT = int(Constants.UDIR_RESPONSE_TIMEOUT)
    Constants.SIGN_KEY_FILE = cfg[Constants.CONFIG_APP]["SIGN_KEY_FILE"]
    Constants.SIGN_CERTIFICATE_FILE = cfg[Constants.CONFIG_APP]["SIGN_CERTIFICATE_FILE"]
    Constants.API_PORT = cfg[Constants.CONFIG_APP]["API_PORT"]
    Constants.API_PORT = int(Constants.API_PORT)
    Constants.AUTH_SERVICE = cfg[Constants.CONFIG_APP]["AUTH_SERVICE"]
    logger.info("Before print")
    logger.info(Constants.AUTH_SERVICE)
    Constants.LOGGER_SERVICE = cfg[Constants.CONFIG_APP]["LOGGER_SERVICE"]
    logger.info(Constants.LOGGER_SERVICE)
    Constants.BROKER_SERVICE = cfg[Constants.CONFIG_APP]["BROKER_SERVICE"]
    logger.info(Constants.BROKER_SERVICE)
    logger.info("After print")
