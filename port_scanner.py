import subprocess
import re

class PortScanner():

    ERROR_RESPONSE = "'Get-PnpDevice' is not recognized as an internal or external command"
    WIN_REGEX = 'COM[0-9]'

    def __init__(self):
        self.port_name = None

    def get_arduino_connected_port(self):
        command = "Get-PnpDevice -Class 'Ports' -InstanceId 'USB*' -Status OK | findstr Arduino"
        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, shell=True, check=True)
        except subprocess.CalledProcessError:
            raise LookupError('No output returned. Please check the command or check Arduino connectivity')
        else:
            if PortScanner.ERROR_RESPONSE in str(result.stderr):
                raise LookupError('Plesae check if Arduino is connected to any USB port')
        return result
    
    def get_port_name(self):
        command_stdout = self.get_arduino_connected_port()
        port_name = re.search(PortScanner.WIN_REGEX, command_stdout.stdout.decode().strip())
        return str(port_name.group(0))
    

