import platform

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
    
    def get_cpu_temp_win(self):
        pass
    
    def get_cpu_temp_linux(self):
        pass

    def get_gpu_temp(self):
        pass
        

if __name__ == '__main__':
    runner = Runner()
    print(runner.get_os())