#
# This file is a part of Typhoon HIL API library.
#
# Typhoon HIL API is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from typhoon.api.device_manager.stub import clstub


class DeviceManagerAPI:
    def __init__(self):
        super().__init__()

    def load_setup(self, file=""):
        """
        Loads HIL setup from file to Control Center.

        Args:
            file (str): Setup description.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.
        """
        return clstub().load_setup(file=file)

    def get_setup_devices(self):
        """
        Get all devices from current HIL setup.

        Returns:
             devices (list): dicts with information for each devices
              {"serial_number": "some_serial", "device_name": "some_device_name",
               "status": "device_stauts"}.

        """
        return clstub().get_setup_devices()

    def get_setup_devices_serials(self):
        """
        Get all devices from current HIL setup.

        Returns:
             devices (list): serial number of each device from setup.

        """
        return clstub().get_setup_devices_serials()

    def get_available_devices(self):
        """
        Get all discovered available devices.

        Returns:
            devices (list): available devices in JSON representation.

        """
        return clstub().get_available_devices()

    def get_detected_devices(self):
        """
        Get all discovered devices.

        Returns:
            devices (list): discovered devices in JSON representation.

        """
        return clstub().get_detected_devices()

    def add_devices_to_setup(self, devices=[]):
        """
        Add devices to active setup.

        Args:
            devices (list): devices to add.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.
        """
        return clstub().add_devices_to_setup(devices=devices)

    def remove_devices_from_setup(self, devices=[]):
        """
        Remove devices from active setup.

        Args:
            devices (list): devices to remove.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.
        """
        return clstub().remove_devices_from_setup(devices=devices)

    def connect_setup(self):
        """
        Activate current selected HIL setup.
        Make all devices in the selected setup inaccessible to others.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.
        """
        return clstub().connect_setup()

    def disconnect_setup(self):
        """
        Deactivate current selected HIL setup.
        Make all devices in the selected setup accessible to others.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.
        """
        return clstub().disconnect_setup()

    def is_setup_connected(self):
        """
        Returns current status of active HIL setup.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.

        """
        return clstub().is_setup_connected()

    def add_discovery_ip_addresses(self, addresses=[]):
        """
        Specify addresses where HIL devices are located if auto discovery
        fails for some reason.

        Args:
            addresses (list): IP addresses where HIL devices are located.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.

        """
        return clstub().add_discovery_ip_addresses(addresses=addresses)

    def remove_discovery_ip_addresses(self, addresses=[]):
        """
        Remove previously added addresses where HIL devices are located
        if auto discovery fails for some reason.

        Args:
            addresses (list): IP addresses which you want to remove.

        Returns:
            status (bool): ``True`` if everything ok, otherwise returns ``False``.

        """
        return clstub().remove_discovery_ip_addresses(addresses=addresses)

    def update_firmware(self, device_to_update, configuration_id=None, force=False):
        """
        Updates the firmware of the selected device.

        Args:
            device_to_update (str): Serial number of the selected device.
            configuration_id (int): sequence number of the configuration.
            force (boolean): Force upload even if desired firmware is the same as
                the one already in HIL device

        """
        return clstub().update_firmware(
            device_to_update=device_to_update,
            configuration_id=configuration_id,
            force=force,
        )

    def sync_firmware(self, device_to_update, configuration_id=None, force=False):
        """
        Updates or rollback the firmware of the selected device.

        Args:
            device_to_update (str): Serial number of the selected device.
            configuration_id (int): sequence number of the configuration.
            force (boolean): Force upload even if desired firmware is the same as
                the one already in HIL device

        """
        return clstub().update_firmware(
            device_to_update=device_to_update,
            configuration_id=configuration_id,
            force=force,
        )

    def get_device_settings(self, device_serial):
        """
        Gets all settings from desired device.
        Args:
            device_serial (str): device serial number.

        Returns:
             settings (dict): {'device_name': 'hil_name',
              'static_ip_address': '', 'netmask': '',
                'gateway': '', 'force_usb': 'False',
                 'heartbeat_timeout': '', 'usb_init_timeout': '',
                  'ssh_enable': 'True'}

        .. note::
             When an empty string is returned as the value of a setting, it means that the setting has a default value.

        """
        return clstub().get_device_settings(device_serial=device_serial)

    def set_device_settings(self, device_serial, settings={}):
        """
        Allows to change all device settings.
        Args:
            device_serial (str): serial number of the desired device.
            settings (dict): device settings by system key (setting name)
             and value (desired values for the previously specified key)
             settings (dict): {'device_name': 'hil_name',
              'static_ip_address': '', 'netmask': '',
                'gateway': '', 'force_usb': 'False',
                 'heartbeat_timeout': '', 'usb_init_timeout': '',
                  'ssh_enable': 'True'}

        .. note::
             When an empty string is passed as a setting value, that setting will be set to the default value.

        """
        return clstub().set_device_settings(
            device_serial=device_serial, settings=settings
        )

    def get_hil_info(self):
        """
        Returns information about all connected HIL devices.

        Returns:
            list: list that contains dictionaries where each dictionary holds
            information about one connected HIL device.

            In case there is no connected HIL devices ``None`` will be returned.

        .. list-table::  Format of one dictionary that holds HIL information.
           :widths: auto
           :header-rows: 1
           :align: left

           * - Dictionary key
             - Meaning
             - Value Type

           * - "device_id"
             - HIL Device ID (0, 1, 2...)
             - int value

           * - "serial_number"
             - HIL Serial number (00404-00-0001, 00402-00-0001...)
             - string value

           * - "configuration_id"
             - HIL Configuration ID (1, 2, 3...)
             - int value

           * - "product_name"
             - HIL Product Name (HIL402, HIL602...)
             - string value

           * - "firmware_release_date"
             - HIL Firmware Release date (in format Y-M-D)
             - string value

           * - "calibration_date"
             - HIL Calibration date (in format Y-M-D). ``None`` will be
               returned if HIL is not calibrated, calibration data is
               wrong or calibration is not supported on connected HIL)
             - string value
        """

        return clstub().get_hil_info()


device_manager = DeviceManagerAPI()
