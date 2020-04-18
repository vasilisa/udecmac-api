
import multiprocessing
import os 
workers = multiprocessing.cpu_count() * 2 + 1

# Gunicorn doesn't like our import of config, so we wrap it in a funciton.
def from_config_file():
    global bind, accesslog, errorlog, loglevel
    from config import config
    
    errorlog  = config.get("Server Parameters", "logfile")
    loglevels = ["debug", "info", "warning", "error", "critical"]
    loglevel  = loglevels[config.getint("Server Parameters", "loglevel")]
    
from_config_file()

print("Logging to:", errorlog)
