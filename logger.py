import logging
import os
import logging.config

'''
    Logger class that will be used to log the necessary
    information into logs/app.log file as well as in console
'''
class Logger():
        
    LOG_DIR = 'logs'
    CONFIG_SET = False

    @staticmethod
    def get_logger(name):
        '''
            static method that returns reference to the logger
            after setting the config from log_config.ini file
            and creating the logs/ directry
        '''
        
        if not os.path.exists(Logger.LOG_DIR):
            os.mkdir(Logger.LOG_DIR)
        
        if not Logger.CONFIG_SET:
            logging.config.fileConfig('log_config.ini')
            Logger.CONFIG_SET = True

        return logging.getLogger(name)