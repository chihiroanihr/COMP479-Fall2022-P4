import time
import threading
import logging
from os import path, makedirs

# Time statements.
# This is done before anything else to enable timestamp logging at every step
def get_time():
    return time.strftime('%H:%M:%S')

def get_full_time():
    return time.strftime('%H:%M:%S, %A %b %Y')

def get_time_log():
    return time.strftime('%H-%M-%S')

def get_time_float():
    return int(time.time())

# Get current working directory of spidy
# WORKING_DIR = path.dirname(path.abspath(__file__))
WORKING_DIR = path.realpath('.')
PACKAGE_DIR = path.dirname(path.realpath(__file__))

# Create log file for logging
try:
    makedirs(WORKING_DIR + '/logs')  # Attempts to make the logs directory
    makedirs(WORKING_DIR + '/saved')  # Attempts to make the saved directory
except OSError:
    pass  # Assumes only OSError wil complain if /logs already exists

def create_logger(name, err_log_file):
    LOGGER = logging.getLogger(name)
    LOGGER.setLevel(logging.DEBUG)

    # create file handler
    handler = logging.FileHandler(err_log_file)
    # minimum level logged: DEBUG (0)
    handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to handler
    handler.setFormatter(formatter)

    # add ch to logger
    LOGGER.addHandler(handler)

    return LOGGER

log_mutex = threading.Lock()

def open_log(log_file_name):
    LOG_FILE = open(log_file_name, 'w+', encoding='utf-8', errors='ignore')

    return LOG_FILE

def write_log(log_file, operation, message, package='spidy', status='INFO', worker=0):
    """
    Writes message to both the console and the log file.

    Operations:
      INIT
      CRAWL
      SCRAPE
      SAVE
      LOG
      ERROR

    STATUSES:
      INFO
      ERROR
      INPUT

    PACKAGES:
      spidy
      reppy
      bs4

    Worker 0 = Core
    """
    global log_mutex
    with log_mutex:
        now = get_time()
        message = '[{0}] [{1}] [WORKER #{2}] [{3}] [{4}]: {5}'\
                  .format(now, package, str(worker), operation, status, message)
        print(message)
        if not log_file.closed:
            log_file.write('\n' + message)