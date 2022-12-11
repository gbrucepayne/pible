import asyncio
import logging
import sys
from typing import Sequence

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

_log = logging.getLogger(__name__)

_log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
_log.addHandler(handler)


async def find_all_devices_services():
    scanner = BleakScanner()
    devices: Sequence[BLEDevice] = await scanner.discover(timeout=5.0)
    device_names = [d.name for d in devices]
    # _log.info(f'Found {len(devices)} devices: {device_names}')
    print(f'Found {len(devices)} devices: {device_names}')
    for d in devices:
        try:
            async with BleakClient(d) as client:
                print(f'Device {d.name} services:')
                if client.services is not None:
                    for service in client.services:
                        # _log.info(f'Device {d.name} service: {service}')
                        print(f'\t{service}')
        except Exception as err:
            _log.error(err)


asyncio.run(find_all_devices_services())