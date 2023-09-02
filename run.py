import platform
from msl.loadlib import LoadLibrary 

class Runner():

    OS_NOT_FOUND = 'OS_NOT_FOUND'
    WINDOWS = 'WINDOWS'
    LINUX = 'LINUX'
    CPU = 'CPU'
    GPU = 'GPU'
    TEMPERATURE = 'TEMPERATURE'
    USAGE = 'USAGE'

    def __init__(self):
        '''
            monitor: Reference object to load the data from OpenHardwareMonitorLib.dll
            cpu_hardware: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            gpu_hardware: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            cpu_temp_sensor: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            gpu_temp_sensor: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            cpu_load_sensor: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
            gpu_load_sensor: Reference object set for the first time of execution to make it usable without the need to fetch it fromm .dll again.
        '''
        self.monitor = None
        self.cpu_hardware = None
        self.gpu_hardware = None
        self.cpu_temp_sensor = None
        self.gpu_temp_sensor = None
        self.cpu_load_sensor = None
        self.gpu_load_sensor = None

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
                        self.cpu_temp_sensor = sensor
                    if 'gpu' in str(sensor.Name).lower():
                        self.gpu_hardware = hardware
                        self.gpu_temp_sensor = sensor
                if str(sensor.SensorType).lower() == 'load':
                    if 'cpu total' in str(sensor.Name).lower():
                        self.cpu_load_sensor = sensor
                    if 'gpu core' in str(sensor.Name).lower():
                        self.gpu_load_sensor = sensor
    
    def get_stats_win(self):
        '''
            Returns the stats by initializing the relevant objects and using them to get the data.
        '''
        if self.monitor == None:
            self.initialize_openhardwaremonitor()
        
        if (self.cpu_hardware == None or self.gpu_hardware == None) or (self.cpu_load_sensor == None or self.gpu_load_sensor == None):
            self.set_temperature_sensors_from_dll(self.monitor)
        
        self.cpu_hardware.Update()
        self.gpu_hardware.Update()
        return {Runner.CPU: {Runner.TEMPERATURE: str(self.cpu_temp_sensor.Value) + 'C', Runner.USAGE: '{value:.1f}%'.format(value = self.cpu_load_sensor.Value)}, 
                Runner.GPU: {Runner.TEMPERATURE: str(self.gpu_temp_sensor.Value) + 'C', Runner.USAGE: '{value:.1f}%'.format(value = self.gpu_load_sensor.Value)}}
    
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