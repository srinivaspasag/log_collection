import os

# log_directory = "/var/log"
# log_directory = "/tmp"

if os.getenv("LOG_DIRECTORY"):
    log_directory = os.getenv("LOG_DIRECTORY")
else:
    log_directory = "/Users/srinivas/dev/projects/log_collection/test_resources"

if os.getenv("N_EVENTS"):
    number_events = os.getenv("N_EVENTS")
else:
    number_events = None

if os.getenv("N_EVENTS"):
    page_size = os.getenv("PAGE_SIZE")
else:
    page_size = 1000
