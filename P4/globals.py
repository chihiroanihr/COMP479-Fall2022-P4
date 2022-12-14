import time
from os import path, makedirs

# Time statements.
# This is done before anything else to enable timestamp logging at every step
def get_time():
    return time.strftime('%H:%M:%S')

def get_full_time():
    return time.strftime('%H:%M:%S, %A %b %Y')

START_TIME = int(time.time())
START_TIME_LONG = get_time()

# Get current working directory of spidy
WORKING_DIR = path.realpath('.')
PACKAGE_DIR = path.dirname(path.realpath(__file__))

# Create log file for logging
try:
    makedirs(WORKING_DIR + '/logs')  # Attempts to make the logs directory
    makedirs(WORKING_DIR + '/saved')  # Attempts to make the saved directory
except OSError:
    pass  # Assumes only OSError wil complain if /logs already exists

# Log location
LOG_FILE_NAME = path.join('logs', 'log_{0}.txt'.format(START_TIME))

# Error log location
ERR_LOG_FILE = path.join('logs', 'error_log_{0}.txt'.format(START_TIME))

log_mutex = threading.Lock()

def open_log():
    LOG_FILE = open(LOG_FILE_NAME, 'w+', encoding='utf-8', errors='ignore')

    return LOG_FILE

def write_log(log_file, operation, message, package='spidy', status='INFO', worker=0):
    """
    Writes message to both the console and the log file.

    Operations:
      INIT
      CRAWL
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