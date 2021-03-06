import logging
from logging.handlers import TimedRotatingFileHandler
import os

def createLogDir(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def get_my_logger(log_stream_name,log_dir):
    # define logger object
    logger = logging.getLogger(log_stream_name)
    # set logging level
    logger.setLevel(logging.INFO)
    createLogDir(log_dir)
    # add file handler
    logger_filename = log_dir + log_stream_name
    filehandler = TimedRotatingFileHandler(logger_filename, when='midnight', backupCount=15)
    logger.addHandler(filehandler)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler.setFormatter(formatter)
    # add stream handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)
    return logger
