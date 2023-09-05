import logging
import logging.config


class Logger():
        
    @staticmethod
    def get_logger(name):
        logging.config.fileConfig('log_config.json')
        return logging.getLogger(name)