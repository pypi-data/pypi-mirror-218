import aiohttp
import websockets
import asyncio
import signal
import json
from datetime import datetime
from .const import *
from .helpers import *
import logging

_logger = logging.getLogger(__name__)

'''
This class is for interaction with the new local API currently only the Micra exposes
'''
class LMLocalAPI:

    @property
    def local_port(self):
        return self._local_port
    
    @property
    def local_ip(self):
        return self._local_ip
    
    @property
    def brew_active(self):
        return self._status[BREW_ACTIVE]
    
    @property
    def brew_active_duration(self):
        return self._status[BREW_ACTIVE_DURATION]

    def __init__(self, local_ip, local_bearer, local_port=8081):
        self._local_ip = local_ip
        self._local_port = local_port
        self._local_bearer = local_bearer

        # init local variables
        self._full_config = None
        self._timestamp_last_websocket_msg = None

        self._status = {}

        self._status[BREW_ACTIVE] = False
        self._status[BREW_ACTIVE_DURATION] = 0


    '''
    Get current config of machine from local API
    '''
    async def local_get_config(self):
        headers = {"Authorization": f"Bearer {self._local_bearer}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"http://{self._local_ip}:{self._local_port}/api/v1/config") as response:
                if response.status == 200:
                    return await response.json()
                
    async def websocket_connect(self, callback=None):
        headers = {"Authorization": f"Bearer {self._local_bearer}"}
        async for websocket in websockets.connect(f"ws://{self._local_ip}:{self._local_port}/api/v1/streaming", extra_headers=headers):
            try:
                # Close the connection when receiving SIGTERM.
                loop = asyncio.get_running_loop()
                loop.add_signal_handler(
                    signal.SIGTERM, loop.create_task, websocket.close())

                # Process messages received on the connection.
                async for message in websocket:
                    await self.handle_websocket_message(message)
                    if callback:
                        callback(self._status)
            except websockets.ConnectionClosed:
                await asyncio.sleep(20)  # wait 20 seconds before trying to reconnect
                continue
            except Exception as e:
                _logger.error(f"Error during websocket connection: {e}")
                await asyncio.sleep(20)
                continue

    async def handle_websocket_message(self, message):
        try:
            self._timestamp_last_websocket_msg = datetime.now()
            message = json.loads(message)
            unmapped_msg = False

            if type(message) is dict:
                if 'MachineConfiguration' in message:
                    # got machine configuration
                    self._status["machineConfiguration"] = json.loads(message["MachineConfiguration"])
                elif "SystemInfo" in message:
                    self._status["systemInfo"] = json.loads(message["SystemInfo"])
                else:
                    unmapped_msg = True

            elif type(message) is list:
                if "KeepAlive" in message[0]:
                    return
                elif "SteamBoilerUpdateTemperature" in message[0]:
                    self._status["steamTemperature"] = message[0]["SteamBoilerUpdateTemperature"]
                elif "CoffeeBoiler1UpdateTemperature" in message[0]:
                    self._status["coffeeTemperature"] = message[0]["CoffeeBoiler1UpdateTemperature"]
                elif "Sleep" in message[0]:
                    self._status["powerOn"] = False
                    self._status["sleepCause"] = message[0]["Sleep"]
                elif "WakeUp" in message[0]:
                    self._status["powerOn"] = True
                    self._status["wakeupCause"] = message[0]["WakeUp"]
                elif "MachineStatistics" in message[0]:
                    self._status["statistics"] = json.loads(message[0]["MachineStatistics"])
                elif "BrewingUpdateGroup1Time" in message[0]:
                    self._status[BREW_ACTIVE] = True
                    self._status[BREW_ACTIVE_DURATION] = message[0]["BrewingUpdateGroup1Time"]
                elif "BrewingSnapshotGroup1" in message[0]:
                    self._status[BREW_ACTIVE] = False
                    self._status["brewingSnapshot"] = json.loads(message[0]["BrewingSnapshotGroup1"])
                else:
                    unmapped_msg = True
            else:
                unmapped_msg = True

            if unmapped_msg:
                _logger.warn(f"Unmapped message from La Marzocco WebSocket, please report to dev: {message}")

        except Exception as e:
            _logger.error(f"Error during handling of websocket message: {e}")