import asyncio
import logging
from typing import Optional

from bleak import BleakClient
from bleak.backends.device import BLEDevice

from .const import EVENT_CHARACTERISTIC_UUID, STATE_CHARACTERISTIC_UUID, UNPAIRED_API_KEY
from .models import DecoraBLEDeviceState

_LOGGER = logging.getLogger(__name__)



class DecoraBLEDevice():
    def __init__(self):
        self._client = None
        self._device = None
        self._key = None
        self._state = DecoraBLEDeviceState(is_on=False, brightness_level=0)

    async def get_api_key(device: BLEDevice) -> Optional[str]:
        async with BleakClient(device) as client:
            await client.write_gatt_char(EVENT_CHARACTERISTIC_UUID, bytearray([0x22, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]), response=True)
            rawkey = await client.read_gatt_char(EVENT_CHARACTERISTIC_UUID)
            _LOGGER.debug("Raw API key from device: %s", repr(rawkey))

            if rawkey[2:6] != UNPAIRED_API_KEY:
                return bytearray(rawkey)[2:].hex()
            else:
                return None

    async def connect(self, device: BLEDevice, key: str):
        _LOGGER.debug("attempting to connect to %s using %s key", device.address, key)

        if self._client is not None and self._client.is_connected:
            _LOGGER.debug("there is already a client connected, disconnecting...")
            self._client.disconnect()

        self._device = device
        self._key = bytearray.fromhex(key)

        def disconnected(client):
            _LOGGER.debug("Device disconnected %s", device.address)
            self._disconnect_cleanup()

        self._client = BleakClient(device, disconnected_callback=disconnected)

        await self._client.connect()
        await self._unlock()

        _LOGGER.debug("Finished connecting %s", self._client.is_connected)

    async def disconnect(self):
        await self._client.disconnect()

    async def turn_on(self):
        _LOGGER.debug("Turning on...")
        await self._refresh_state()
        await self._write_state(DecoraBLEDeviceState(is_on=True, brightness_level=self._state.brightness_level))

    async def turn_off(self):
        _LOGGER.debug("Turning off...")
        await self._refresh_state()
        await self._write_state(DecoraBLEDeviceState(is_on=False, brightness_level=self._state.brightness_level))

    async def set_brightness_level(self, brightness_level):
        _LOGGER.debug("Setting brightness level to %d...", brightness_level)
        await self._refresh_state()
        await self._write_state(DecoraBLEDeviceState(is_on=self._state.is_on, brightness_level=brightness_level))

    def _disconnect_cleanup(self):
        self._device = None
        self._key = None
        self._client = None
        self._state = DecoraBLEDeviceState(is_on=False, brightness_level=0)

    async def _unlock(self):
        packet = bytearray([0x11, 0x53, *self._key])
        await self._client.write_gatt_char(EVENT_CHARACTERISTIC_UUID, packet, response=True)

    async def _refresh_state(self):
        data = await self._client.read_gatt_char(STATE_CHARACTERISTIC_UUID)
        self._state = DecoraBLEDeviceState(is_on=data[0] == 1, brightness_level=data[1])
        _LOGGER.debug("State updated: %s", self._state)

    async def _write_state(self, state):
        self._state = state
        packet = bytearray([1 if state.is_on else 0, state.brightness_level])
        _LOGGER.debug("Writing state: %s", state)
        await self._client.write_gatt_char(STATE_CHARACTERISTIC_UUID, packet, response=True)
