import os

# getting the environment variable with default value
log_mode = int(os.environ.get("log_mode", 1))
log_date_time_format = os.environ.get("log_date_format", "%Y-%m-%d %H:%M:%S")
