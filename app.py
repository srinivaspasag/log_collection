from flask import Flask, jsonify, render_template, request
from logger import setup_logger
import log_observer as lp
from consts import log_directory
import os

app = Flask(__name__)
logger = setup_logger()


# Define API endpoint
@app.route("/api/v1/logs")
def get_logs():
    """
    API endpoint to retrieve all logs.

    Returns:
        A JSON response containing the logs.

    Methods:
    GET: Returns all logs.

    Examples:
        To retrieve all logs:
        GET /api/v1/logs

    """
    # Replace with your code to read log file and return data

    files_list = []
    for root, dirs, files in os.walk(log_directory):
        for file in files:
            if file.endswith(".gz") or file.endswith(".bz2") or file.endswith(".zip"):
                continue  # skip compressed files
            # if file.endswith(".log"):
            files_list.extend(files)

    logger.debug("the files list is", files_list)
    return jsonify(files_list)


# Define API endpoint
@app.route("/api/v1/log", methods=["GET"])
def get_log():
    """
    API endpoint to retrieve a log.

    Returns:
        A JSON response containing the logs.

    Methods:
    GET: Returns all logs.

    Examples:
        To retrieve all logs:
        GET /api/v1/log

    """
    # Get the filename and number of events, keyword from the query parameters
    try:
        filename = request.args.get("filename")
    except:
        return jsonify({"message": "file name is required"})
    if not filename:
        return jsonify({"message": "file name is required"})

    try:
        n_str = request.args.get("n")
        if n_str is not None and n_str.isdigit():
            n_events = int(n_str)
        else:
            n_events = 10  # Set a default value if n is not a valid integer
    except:
        return jsonify({"message": "Error reading "})

    keyword = request.args.get("keyword")
    page = request.args.get("page")

    # Get the requested page number from the query parameters
    page = int(request.args.get("page", 1))
    # logger.info(f"Received params: param1={filename}, param2={n_events}")
    file_path = os.path.join(log_directory, filename)

    # log_data = lp.fetch_from_single_server_pagination (file_path)
    log_data = lp.fetch_logs_paging(file_path, n_events, page)

    logger.info(log_data)

    # Call the function to get the last n events from the file
    last_n_lines = lp.get_last_n_events(log_data, n_events, keyword)
    # last_n_lines = []
    # Return the last n events as a JSON response
    return last_n_lines


# Define UI endpoint
@app.route("/api/v1/")
def index():
    """
    UI endpoint for the application.

    Returns:
        The rendered HTML template for the application.

    Methods:
        GET: Returns the rendered HTML template.

    Examples:
        To access the application:
            GET /
    """
    # Render the index.html template with the log data from the API
    """log_data = get_logs().json
    return render_template("index.html", log_data=log_data)"""

    # log_files = os.listdir(log_directory)
    log_files = []
    for root, dirs, files in os.walk(log_directory):
        log_files.extend(files)
    log_links = [f'<a href="/api/v1/logs/{file}">{file}</a>' for file in log_files]
    return render_template("index.html", log_links=log_links)


@app.route("/api/v1/logs/<path:filename>")
def logs(filename):
    # return open(os.path.join(logs_dir, filename)).read()
    log_data = lp.fetch_from_single_server(os.path.join(log_directory, filename))

    # Call the function to get the last n events from the file
    last_n_lines = lp.get_last_n_events(log_data)

    # Return the last n events as a JSON response
    return jsonify(last_n_lines)


# Start server
if __name__ == "__main__":
    """
    Starts the Flask application server.

    Parameters:
        debug (bool): If True, runs the application in debug mode.

    Returns:
        None.
    """
    app.run(debug=True)
