import logging
from flask import jsonify
from logger import setup_logger
from consts import page_size, log_directory

import app
import json


logger = setup_logger()
chunk_size = 1000


def get_last_n_events(lines, n=10, keyword=None):
    """
    Retrieves the last n events from the specified file.

    Args:
        filename (str): The name of the file to read.
        n (int): The number of events to retrieve.

    Returns:
        list: A list of strings representing the last n events in the file.
    """
    if keyword is not None:
        logging.info(f"Filtering events for keyword '{keyword}'")
        lines = [line for line in lines if keyword in line]

    # reverse last n lines
    last_n_lines = lines[-n:][::-1]
    print(f"Retrieved {len(lines)} {n} events")

    logger.info(f"Retrieved {len(last_n_lines)} {n} events")

    """output_file = "./tests/last_n_lines.log"
    with open(output_file, "w") as file:
        file.writelines(last_n_lines)"""

    return last_n_lines


def fetch_from_single_server(filename):
    try:
        with open(filename, "r") as f:
            log_data = f.readlines()
    except:
        return jsonify({"message": "Error reading log file 2"})
    return log_data


def fetch_from_single_server_pagination(filename, page=1):
    try:
        # Determine number of logs to be displayed per page
        logs_per_page = 20

        # Calculate the offset and limit based on the logs per page and current page
        offset = (page - 1) * logs_per_page
        limit = logs_per_page

        # Retrieve the logs from /var/log using the offset and limit
        logs = []
        with open(filename) as f:
            for i, line in enumerate(f):
                if i >= offset and i < offset + limit:
                    logs.append(line.strip())

        # Return the logs as a JSON response
        logger.info(logs)
        return logs

    except Exception as e:
        # Return an error message as a JSON response
        return jsonify({"error": str(e)}), 500


def seek_to_line(file, line_number):
    # Move the file pointer to the beginning of the file
    file.seek(0, 0)

    # Read each line of the file and keep track of the byte offset
    byte_offset = 0
    for i in range(line_number):
        line = file.readline()
        if not line:
            break
        byte_offset += len(line)

    # Move the file pointer to the beginning of the desired line
    file.seek(byte_offset, 0)


def fetch_logs_paging(log_file, num_events, page=None):
    # get the total number of lines in the log file
    total_lines = sum(1 for line in open(log_file))

    # calculate the number of pages needed to retrieve the desired number of events
    num_pages = (num_events + page_size - 1) // page_size

    # calculate the starting line number for the last page
    start_line = total_lines - (page_size * num_pages)

    # Read each line of the file and keep track of the byte offset
    byte_offset = 0

    # open the log file and seek to the starting line
    with open(log_file, "r") as f:
        seek_to_line(f, start_line)  # seek to line 10

        events = []
        for i in range(num_events):
            line = f.readline()
            if not line:
                break
            events.append(line.strip())

    # print the last n events
    # return reversed(events)
    logger.info(events)
    return events
