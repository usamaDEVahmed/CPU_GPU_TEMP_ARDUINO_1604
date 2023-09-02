from run import Runner
import serial
import time

class Sender():

    ENCODING = 'utf-8'

    def __init__(self):
        self.arduino_communicator = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)  
        self.runner = Runner()
        self.data = None

    def get_stats(self):
        if self.runner != None:
            self.runner = Runner()
        return self.runner.get_stats()

    def convert_data_into_bytes(self, data):
        return bytes(str(data), Sender.ENCODING)

    def structure_stats(self, stats):
        structured_data = f'{stats[Runner.CPU][Runner.TEMPERATURE]},{stats[Runner.CPU][Runner.USAGE]},{stats[Runner.GPU][Runner.TEMPERATURE]},{stats[Runner.GPU][Runner.USAGE]}'                
        return structured_data

    def send_data_to_arduino(self):
        structured_data = self.structure_stats(self.get_stats())
        print('[+] Sending data: ' + str(structured_data))
        self.arduino_communicator.write(self.convert_data_into_bytes(structured_data))
    
    def close_arduino_communicator(self):
        self.arduino_communicator.close()
    

if __name__ == '__main__':
    sender = Sender()
    while True:
        sender.send_data_to_arduino()
        time.sleep(1)
