import platform

class Runner():

    OS_NOT_FOUND = 'OS_NOT_FOUND'

    def __init__(self):
        self.os_names = ['windows', 'linux']

    def get_os(self):
        os = platform.system()
        for os_name in self.os_names:
            if os.lower() == os_name.lower():
                return os
        
        return Runner.OS_NOT_FOUND

        

if __name__ == '__main__':
    runner = Runner()
    print(runner.get_os())