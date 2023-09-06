import logging
import os
import logging.config


class Logger():
        
    LOG_DIR = 'logs'

    @staticmethod
    def get_logger(name):
        
        if not os.path.exists(Logger.LOG_DIR):
            os.mkdir(Logger.LOG_DIR)

        logging.config.fileConfig('log_config.ini')
        return logging.getLogger(name)