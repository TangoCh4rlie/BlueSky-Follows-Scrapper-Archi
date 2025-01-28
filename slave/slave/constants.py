import os
import logging

NEEDED_ENV_VARIABLES = ["SLAVE_ID", "MASTER_URL", "REDIS_HOSTNAME", "OUTPUT_PATH"]
NOT_PRESENT_ENV_VARIABLES = [x for x in NEEDED_ENV_VARIABLES if x not in os.environ]

if len(NOT_PRESENT_ENV_VARIABLES) > 0:
    logging.critical(f"A needed environment variable is not set : {NOT_PRESENT_ENV_VARIABLES}")
    exit(1)

SLAVE_ID = int(os.environ.get("SLAVE_ID"))
MASTER_URL = os.environ.get("MASTER_URL")
REDIS_HOSTNAME = os.environ.get("REDIS_HOSTNAME")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH")

TOTAL_BIT_SIZE = 32
VERTICE_ID_BIT_SIZE = 25