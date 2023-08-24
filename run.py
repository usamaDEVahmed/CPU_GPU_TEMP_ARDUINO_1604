import platform
from msl.loadlib import LoadLibrary 

class Runner():

    OS_NOT_FOUND = 'OS_NOT_FOUND'
    WINDOWS = 'WINDOWS'
    LINUX = 'LINUX'

    def get_os(self):
        os = platform.system()
        if os.lower() == Runner.WINDOWS.lower():
            return Runner.WINDOWS
        elif os.lower() == Runner.LINUX.lower():
            return Runner.LINUX
        else:
            return Runner.OS_NOT_FOUND
        
    def initialize_openhardwaremonitor(self):
        open_hardware_monitor_lib = LoadLibrary('libs\\OpenHardwareMonitorLib.dll')
        openHardwareMonitor = open_hardware_monitor_lib.lib.Hardware
        handle = openHardwareMonitor.Computer()
        handle.MainboardEnabled = True
        handle.CPUEnabled = True
        handle.GPUEnabled = True
        handle.Open()
        return handle
    
    def get_cpu_temp_win(self):
        return 'win'
    
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
    print(runner.initialize_openhardwaremonitor())