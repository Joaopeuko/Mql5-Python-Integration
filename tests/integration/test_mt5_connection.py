"""Integration test for MetaTrader5 connection.

This module tests the ability to establish a connection with MT5 platform.
"""

import logging
import os
import sys
import time

import MetaTrader5 as mt5  # noqa: N813

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Testing MT5 initialization...")

success = False
for attempt in range(10):
    try:
        if mt5.initialize(
            login=int(os.getenv("MT5_LOGIN")),  # type: ignore[arg-type]
            password=os.getenv("MT5_PASSWORD"),
            server=os.getenv("MT5_SERVER"),
            path=os.getenv("MT5_PATH"),
        ):
            logger.info("MT5 initialized successfully")
            mt5.shutdown()
            success = True
            break
    except (ConnectionError, ValueError, TypeError) as e:
        logger.info(f"Connection error: {e}")
        try:
            mt5.initialize()
        except (ConnectionError, ValueError, TypeError) as e:
            logger.info(f"Attempt {attempt+1}: Not ready yet, sleeping... Error: {e}")
            time.sleep(5)

if not success:
    logger.info("Failed to initialize MT5 after waiting.")
    mt5.shutdown()
