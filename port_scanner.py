import subprocess

class PortScanner():

    def __init__(self):
        self.port_name = None

    def get_arduino_connected_port(self):
        ret = subprocess.run("Get-PnpDevice -Class 'Ports' -InstanceId 'USB*' -Status OK | findstr Arduino", capture_output=True, shell=True)
        return ret

if __name__ == '__main__':
    ps = PortScanner()
    data = ps.get_arduino_connected_port()
    print(data)


