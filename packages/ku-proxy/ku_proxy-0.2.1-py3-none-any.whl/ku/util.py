import logging, os
os.system('color')
from typing import Optional

class CustomFormatter(logging.Formatter):    
    
    grey = '\u001b[34m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\u001b[31m'
    reset = '\x1b[0m'    

    def __init__(self, fmt, primary: Optional[str] = blue):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: primary + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%m/%d/%Y %I:%M:%S %p')
        return formatter.format(record)
