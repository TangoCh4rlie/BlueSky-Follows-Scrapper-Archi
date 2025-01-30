import os
import logging
import math

NEEDED_ENV_VARIABLES = ["SLAVE_ID", "MASTER_URL", "REDIS_HOSTNAME", "OUTPUT_PATH"]
NOT_PRESENT_ENV_VARIABLES = [x for x in NEEDED_ENV_VARIABLES if x not in os.environ]

if len(NOT_PRESENT_ENV_VARIABLES) > 0:
    logging.critical(f"A needed environment variable is not set : {NOT_PRESENT_ENV_VARIABLES}")
    exit(1)

SLAVE_ID : int = int(os.environ.get("SLAVE_ID"))
MASTER_URL : str = os.environ.get("MASTER_URL")
REDIS_HOSTNAME : str = os.environ.get("REDIS_HOSTNAME")
OUTPUT_PATH : str = os.environ.get("OUTPUT_PATH")
MAX_NB_TREATED : int = int(os.environ.get("MAX_NB_TREATED", math.inf))


TOTAL_BIT_SIZE = 32
VERTICE_ID_BIT_SIZE = 25