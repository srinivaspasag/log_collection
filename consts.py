import os 

# log_directory = "/var/log"
# log_directory = "/tmp"
page_size = 10  # replace with your desired page size
if os.getenv('LOG_DIRECTORY'):
    log_directory = os.getenv('LOG_DIRECTORY')
else:
    log_directory = "/Users/srinivas/dev/projects/log_collection/test_resources"