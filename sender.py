from logger import Logger
from stat_fetcher import StatFetcher
from port_scanner import PortScanner
import serial
import time

'''
    Class that will be used to get the CPU & GPU stats
    from Runner module and then structure it in comma 
    seperated string, convert that string into utf-8
    encoded bytes and then send it to Arduino via Serial 
'''
class Sender():

    ENCODING = 'utf-8'
    DATA_POSTFIX = 'e'

    def __init__(self):
        '''
            self.arduino_communicator: Serial communication with Arduino
            self.runner: Reference to Runner module that fethces the CPU & GPU stats
        '''
        self.log = Logger.get_logger(__name__)
        self.port_scanner = PortScanner()
        self.arduino_communicator = serial.Serial(port=self.port_scanner.get_port_name(), baudrate=115200, timeout=0.1)  
        self.runner = StatFetcher()

    def get_stats(self):
        '''
            Gets the stats from the Runner module it and returns it to the caller
        '''
        if self.runner == None:
            self.log.debug('Creating new reference of Runner class')
            self.runner = StatFetcher()
        return self.runner.get_stats()

    def convert_data_into_bytes(self, data):
        '''
            Converts the fetched stats into encoded bytes
        '''
        self.log.debug(f'converting data: {data} into bytes using encoding: {Sender.ENCODING}')
        return bytes(str(data), Sender.ENCODING)

    def structure_stats(self, stats):
        '''
            Structure the data finalize it in comma separated values
        '''
        structured_data = f'CPU: {stats[StatFetcher.CPU][StatFetcher.TEMPERATURE]} {stats[StatFetcher.CPU][StatFetcher.USAGE]}\nGPU: {stats[StatFetcher.GPU][StatFetcher.TEMPERATURE]} {stats[StatFetcher.GPU][StatFetcher.USAGE]}'                
        self.log.debug(f'Structured data that is to be sent to Arduino: {str(structured_data)}')
        return structured_data
    
    def add_postfix_to_data(self, structured_data):
        """
            Adds postfix 'e' to the structured data so that Arduino can find the end point of the data
        """
        return structured_data + Sender.DATA_POSTFIX
        

    def send_data_to_arduino(self):
        '''
            Send the data to Arudino via Serial
        '''
        try:
            structured_data = self.structure_stats(self.get_stats())
            structured_data = self.add_postfix_to_data(structured_data)
            data = self.convert_data_into_bytes(structured_data)
            self.log.debug(f'Sending data to Arduino: {data}')
            self.arduino_communicator.write(data)
        except:
            self.log.exception('Exception occured while writing the data to Arduino board')
    
    def close_arduino_communicator(self):
        '''
            Close connection to Arduino Serial to stop communication
        '''
        self.log.debug('Closing Arduino board communication')
        self.arduino_communicator.close()
    

if __name__ == '__main__':
    sender = Sender()
    while True:
        sender.send_data_to_arduino()
        time.sleep(1)
