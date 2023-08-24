import platform
import time
from msl.loadlib import LoadLibrary 

class Runner():

    OS_NOT_FOUND = 'OS_NOT_FOUND'
    WINDOWS = 'WINDOWS'
    LINUX = 'LINUX'

    def __init__(self):
        '''
        monitor: Reference object to load the data from OpenHardwareMonitorLib.dll
        '''
        self.monitor = None

    def get_os(self):
        os = platform.system()
        if os.lower() == Runner.WINDOWS.lower():
            return Runner.WINDOWS
        elif os.lower() == Runner.LINUX.lower():
            return Runner.LINUX
        else:
            return Runner.OS_NOT_FOUND
        
    def initialize_openhardwaremonitor(self):
        open_hardware_monitor_lib = LoadLibrary('libs\\OpenHardwareMonitorLib.dll', 'net')
        openHardwareMonitor = open_hardware_monitor_lib.lib.OpenHardwareMonitor.Hardware
        monitor = openHardwareMonitor.Computer()
        monitor.MainboardEnabled = True
        monitor.CPUEnabled = True
        monitor.GPUEnabled = True
        monitor.Open()
        return monitor

    def set_temperature_sensors_from_dll(self, monitor):
        for hardware in monitor.Hardware:
            hardware.Update()
            for sensor in hardware.Sensors:
                if str(sensor.SensorType).lower() == 'temperature':
                    if 'cpu package' in str(sensor.Name).lower():
                        self.cpu_temp_sensor = sensor
                    if 'gpu' in str(sensor.Name).lower():
                        self.gpu_temp_sensor = sensor
                    
    
    def get_cpu_temp_win(self):
        # monitor reference to refer the OpenhardwareMonitorLib.dll is only set for first time of execution.
        # Other times, the set reference is used only.
        if self.monitor == None:
            self.monitor = self.initialize_openhardwaremonitor()
        
        self.set_temperature_sensors_from_dll(self.monitor)
        return (self.cpu_temp_sensor.Value, self.gpu_temp_sensor.Value)
    
    def get_cpu_temp_linux(self):
        return 'linux'

    def get_cpu_temp(self):
        current_os = self.get_os()
        if current_os == Runner.WINDOWS:
            return self.get_cpu_temp_win()
        elif current_os == Runner.LINUX:
            return self.get_cpu_temp_linux()
        else:
            return None

        
# use the below link
# https://stackoverflow.com/questions/3262603/accessing-cpu-temperature-in-python


if __name__ == '__main__':
    runner = Runner()
    while True:
        print(runner.get_cpu_temp())
        time.sleep(2)