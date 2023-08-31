from run import Runner
import serial

class Sender():

    def __init__(self):
        self.arduino_communicator = serial.Serial(port='COM4', baudrate=115200, timeout=0.1)  
        self.data = None

    def get_stats(self):
        runner = Runner()
        return runner.get_stats()

    def send_data_to_arduino(self):
        data = self.get_stats()

    def structure_data(data):
        structured_data = None
        return structured_data
    
    def close_arduino_communicator(self):
        self.arduino_communicator.close()
    

if __name__ == '__main__':
    print(Sender().structure_data())