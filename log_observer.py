import logging
from flask import jsonify
from logger import setup_logger
from consts import *

logger = setup_logger()


def get_last_n_events(lines, n=1000, keyword=None):
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
    logger.debug(f"Retrieved {len(last_n_lines)} {n} events")
    return last_n_lines


def fetch_from_single_server(filename):
    try:
        with open(filename, "r") as f:
            log_data = f.readlines()
    except:
        return jsonify({"message": "Error reading log file 2"})
    return log_data


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


def fetch_logs_paging(log_file, num_events=None, page=page_default_val, keyword=None):
    # get the total number of lines in the log file
    try:
        with open(log_file) as f:
            total_lines = sum(1 for line in f)
    except:
        return jsonify({"message": "Error reading file"})

    if page == page_default_val and not num_events:
        page = 1

    if not num_events:
        num_events = total_lines

    # calculate the number of pages needed to retrieve the desired number of events
    num_pages = (num_events + page_size - 1) // page_size
    # logger.info("num_pages", num_pages, num_events, int(page))

    remainder = num_events % page_size
    logger.debug(num_events, page)

    if page > num_pages:
        page = page_default_val
        num_events = zero

    if page >= 1 and page <= num_pages:
        start_line = total_lines - (page * page_size)
        num_events = page_size

    elif remainder:
        start_line = total_lines - (page_size * num_pages) + (page_size - remainder)
    elif num_events < 0:
        start_line = zero
        num_events = total_lines  # to make sure start from 0 to all lines
    else:
        # calculate the starting line number for the last page
        start_line = total_lines - (page_size * num_pages)

    # open the log file and seek to the starting line
    with open(log_file, "r") as f:
        seek_to_line(f, start_line)  # seek to line 10

        events = []
        for i in range(num_events):
            line = f.readline()
            if not line:
                break
            events.append(line.strip())

    last_n_lines = get_last_n_events(events, num_events, keyword)

    # return  the last n events

    next_page = None
    if page > 0:
        next_page = page + 1
        if next_page > num_pages:
            next_page = None

    return {
        "events": last_n_lines,
        "total_pages": num_pages,
        "current_page": page,
        "total_lines": total_lines,
        "next_page": next_page,
        "start_line": start_line,
    }
