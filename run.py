import platform
from msl.loadlib import LoadLibrary 

class Runner():

    OS_NOT_FOUND = 'OS_NOT_FOUND'
    WINDOWS = 'WINDOWS'
    LINUX = 'LINUX'
    CPU = 'CPU'
    GPU = 'GPU'
    TEMPERATURE = 'TEMPERATURE'

    def __init__(self):
        '''
            monitor: Reference object to load the data from OpenHardwareMonitorLib.dll
            cpu_hardware: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            gpu_hardware: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            cpu_temp: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            gpu_temp: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
        '''
        self.monitor = None
        self.cpu_hardware = None
        self.gpu_hardware = None
        self.cpu_temp = None
        self.gpu_temp = None

    def get_os(self):
        '''
            Returns what OS this script is currently running on.
            If OS is WINDOWS then libs/OpenHardwareMonitorLib.dll will be used to get the CPU and GPU stats.
            TODO: DOCS Update for LINUX
        '''
        os = platform.system()
        if os.lower() == Runner.WINDOWS.lower():
            return Runner.WINDOWS
        elif os.lower() == Runner.LINUX.lower():
            return Runner.LINUX
        else:
            return Runner.OS_NOT_FOUND
        
    def initialize_openhardwaremonitor(self):
        '''
            Fetches the Hardware reference from OpenHardwareMonitorLib.dll and decompiles it from 32-bit to 64-bit to be embedded in Python version 3.8.10 x64.
        '''
        open_hardware_monitor_lib = LoadLibrary('libs\\OpenHardwareMonitorLib.dll', 'net')
        openHardwareMonitor = open_hardware_monitor_lib.lib.OpenHardwareMonitor.Hardware
        monitor = openHardwareMonitor.Computer()
        monitor.MainboardEnabled = True
        monitor.CPUEnabled = True
        monitor.GPUEnabled = True
        monitor.Open()
        self.monitor = monitor

    def set_temperature_sensors_from_dll(self, monitor):
        '''
            Fetches the sensors references from OpenHardwareMonitorLib.dll for CPU and GPU and sets them at object level.
        '''
        for hardware in monitor.Hardware:
            for sensor in hardware.Sensors:
                if str(sensor.SensorType).lower() == 'temperature':
                    if 'cpu package' in str(sensor.Name).lower():
                        self.cpu_hardware = hardware
                        self.cpu_temp = sensor
                    if 'gpu' in str(sensor.Name).lower():
                        self.gpu_hardware = hardware
                        self.gpu_temp = sensor
    
    def get_stats_win(self):
        '''
            Returns the stats by initializing the relevant objects and using them to get the data.
        '''
        if self.monitor == None:
            self.initialize_openhardwaremonitor()
        
        if (self.cpu_hardware == None) or (self.gpu_hardware == None):
            self.set_temperature_sensors_from_dll(self.monitor)
        
        self.cpu_hardware.Update()
        self.gpu_hardware.Update()
        return {Runner.CPU: {Runner.TEMPERATURE: self.cpu_temp.Value}, 
                Runner.GPU: {Runner.TEMPERATURE: self.gpu_temp.Value}}
    
    def get_stats_linux(self):
        return 'linux'

    def get_stats(self):
        '''
            Common method that uses the methods depending upon the OS and returns the stats
        '''
        current_os = self.get_os()
        if current_os == Runner.WINDOWS:
            return self.get_stats_win()
        elif current_os == Runner.LINUX:
            return self.get_stats_linux()
        else:
            return None

        
# use the below link
# https://stackoverflow.com/questions/3262603/accessing-cpu-temperature-in-python


if __name__ == '__main__':
    runner = Runner()
    for i in range(5):
        print(runner.get_stats())
    

