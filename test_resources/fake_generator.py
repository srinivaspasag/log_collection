import datetime
import test_resources.conftest as c

# create a file with timestamp attached to its name
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")


def generate_data(lines):
    # open the file in write mode
    path = "./test_resources/"
    filename = f"log_{lines}.txt"
    filepath = path + filename
    with open(filepath, "w") as file:
        # write 10,000 messages with timestamps
        for i in range(lines):
            # now = datetime.datetime.now()
            # file.write(f"{now} - This is message number {i+1}\n")
            file.write(f"This is message number {i+1}\n")

    return filename
