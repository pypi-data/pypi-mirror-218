#
# IAidlab.py
# Aidlab-SDK
# Created by Szymon Gesicki on 22.06.2020.
#

class IAidlab:
    """
    The `IAidlab` class is the main interface for interacting with an Aidlab or
    Aidmed One.

    This class provides methods for configuring the device and controlling
    its data synchronization processes. 

    It also stores basic information about the device, like its firmware
    version, serial number, hardware version, and MAC address.

    Attributes:
        firmware_revision (str): The firmware version of the device.
        serial_number (str): The serial number of the device.
        hardware_revision (str): The hardware version of the device.
        address (str): The MAC address of the device.
    """

    firmware_revision: str = ""
    serial_number: str = ""
    hardware_revision: str = ""
    address: str = ""

    def __init__(self, delegate):
        """
        Construct an `IAidlab` instance.

        Args:
            delegate: The object that acts as the delegate for the device.
        """
        self.delegate = delegate

    def set_ecg_filtration_method(self, method):
        """
        Set the ECG filtration method.

        Args:
            method: The filtration method to be used (normal or aggressive).
        """
        self.delegate.set_ecg_filtration_method(method)

    def start_synchronization(self):
        """
        Start data synchronization with the device.
        """
        self.delegate.start_synchronization(self.address)

    def stop_synchronization(self):
        """
        Stop data synchronization with the device.
        """
        self.delegate.stop_synchronization(self.address)
    
    def send(self, command: str):
        """
        Send a command to the device.

        Args:
            command (str): The command to be sent.
        """
        self.delegate.send(self.address, command)

    def disconnect(self):
        """
        Disconnect from the device.
        """
        self.delegate.disconnect(self.address)