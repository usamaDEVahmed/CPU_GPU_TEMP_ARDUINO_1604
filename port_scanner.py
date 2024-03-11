from logger import Logger
import subprocess
import re

'''
    Class that will be used to scan all of the 
    USB ports and will looks for the one to which
    Arduino board has been connected and will
    return that specific port's name
'''
class PortScanner():

    ERROR_RESPONSE = "'Get-PnpDevice' is not recognized as an internal or external command"
    WIN_REGEX = 'COM[0-9]'

    def __init__(self):
        self.port_name = None
        self.log = Logger.get_logger(__name__)

    def get_arduino_connected_port(self):
        '''
            Runs the Powershell command for win10 to fetch the USB port's name 
            to which Arduino board is connected
        '''
        command = "Get-PnpDevice -Class 'Ports' -InstanceId 'USB*' -Status OK | findstr CH340"
        self.log.debug(f'Running command to find Arduino board\'s port name: {command}')
        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, shell=True, check=True)
            self.log.debug(f'Result captured: {str(result)}')
        except subprocess.CalledProcessError as e:
            self.log.error('Exception occured.', exc_info=True)
            raise LookupError('No output returned. Please check the command or check Arduino connectivity')
        else:
            if PortScanner.ERROR_RESPONSE in str(result.stderr):
                self.log.error('Look like Arduino board is not connected to the PC at all')
                raise LookupError('Plesae check if Arduino is connected to any USB port')
        return result
    
    def get_port_name(self):
        '''
            Returns the decoded port name to string from the data in result of the powershell command
        '''
        try:
            command_stdout = self.get_arduino_connected_port()
            port_name = re.search(PortScanner.WIN_REGEX, command_stdout.stdout.decode().strip())
            if len(port_name.group(0)) != 0:
                self.log.debug(f'Found Arduino board connected to port: {str(port_name.group(0))}')
                return str(port_name.group(0))
            self.log.error('Did not find Arduino board connected to any port')
            return None
        except LookupError as e:
            self.log.error(f'Lookup Error occuured: {e}')
            exit()
    