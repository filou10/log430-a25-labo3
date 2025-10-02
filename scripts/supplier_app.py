"""
Supplier Stock-Checking Application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import logging
import signal
import sys

from endpoint_tester import EndpointTester


ENDPOINT_URL = "http://store_manager:5000/stocks/graphql-query"

TEST_PAYLOAD = '{"query":"{ product(productId: \\"1\\") { id name sku quantity price } }","variables":{}}'
INTERVAL_SECONDS = 10
TIMEOUT_SECONDS = 10
MAX_RETRIES = 3

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("endpoint_calls.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    logger.info("Received interrupt signal")
    sys.exit(0)


# App entrypoint
if __name__ == "__main__":
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Create and run the tester
    caller = EndpointTester(
        url=ENDPOINT_URL,
        payload=TEST_PAYLOAD,
        interval=INTERVAL_SECONDS,
        timeout=TIMEOUT_SECONDS,
        max_retries=MAX_RETRIES,
        logger=logger,
    )

    try:
        caller.run()
    except KeyboardInterrupt:
        caller.stop()
    finally:
        logger.info("Script terminated")
