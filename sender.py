from run import Runner
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

    def __init__(self):
        '''
            self.arduino_communicator: Serial communication with Arduino
            self.runner: Reference to Runner module that fethces the CPU & GPU stats
        '''
        self.arduino_communicator = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)  
        self.runner = Runner()

    def get_stats(self):
        '''
            Gets the stats from the Runner module it and returns it to the caller
        '''
        if self.runner != None:
            self.runner = Runner()
        return self.runner.get_stats()

    def convert_data_into_bytes(self, data):
        '''
            Converts the fetched stats into encoded bytes
        '''
        return bytes(str(data), Sender.ENCODING)

    def structure_stats(self, stats):
        '''
            Structure the data finalize it in comma separated values
        '''
        structured_data = f'{stats[Runner.CPU][Runner.TEMPERATURE]},{stats[Runner.CPU][Runner.USAGE]},{stats[Runner.GPU][Runner.TEMPERATURE]},{stats[Runner.GPU][Runner.USAGE]}'                
        return structured_data

    def send_data_to_arduino(self):
        '''
            Send the data to Arudino via Serial
        '''
        structured_data = self.structure_stats(self.get_stats())
        print('[+] Sending data: ' + str(structured_data))
        self.arduino_communicator.write(self.convert_data_into_bytes(structured_data))
    
    def close_arduino_communicator(self):
        '''
            Close connection to Arduino Serial to stop communication
        '''
        self.arduino_communicator.close()
    

if __name__ == '__main__':
    sender = Sender()
    while True:
        sender.send_data_to_arduino()
        time.sleep(1)
