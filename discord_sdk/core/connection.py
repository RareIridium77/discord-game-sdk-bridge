"""
requirements.txt
aiohttp
json
logging
websockets
"""

import json
import logging
import asyncio
import aiohttp
import websockets

from .events import __Events
from .exceptions import (
    DiscordBridgeError,
    RouteNotAllowedError,
    BridgeConnectionError,
    WebSocketDisconnectedError,
    EventProcessingError
)
from .enums import ActivityJoinRequestReply, ActivityActionType

_available_routes = [
    "/accept_invite",
    "/send_invite",
    "/send_request_reply",
    "/set_activity",
    "/clear_activity",
    "/enable_discord",
    "/disable_discord"
]

async def post(session: aiohttp.ClientSession, url: str, data: dict):
    async with session.post(url, json=data) as response:
        text = await response.text()
        return response.status, text

class __DiscordBridge:
    def __init__(self, clientId: int, host: str = "http://localhost:5000"):
        self.clientId = clientId
        self.host = host.rstrip("/")
        self.session = None
        self.connected = False
    
    async def connect(self):
        try:
            self.session = aiohttp.ClientSession(self.host)
            self.connected = True
        except websockets.exceptions.ConnectionClosedError as e:
            self.connected = False
            logging.error(f"[!] {e}")

    async def _post_route(self, route: str, payload: dict):
        if not self.connected:
            raise BridgeConnectionError("Please run async connect() method before doing things.")
        
        if route not in _available_routes:
            raise RouteNotAllowedError(f"Route '{route}' is not allowed.")

        url = f"{self.host}{route}"
        status, response_text = await post(self.session, url, payload)
        logging.debug(f"[{route}] Status: {status}, Response: {response_text}")
        return status, response_text

    async def enable_discord_bridge(self):
        return await self._post_route("/enable_discord", {})
    
    async def disable_discord_bridge(self):
        return await self._post_route("/disable_discord", {})
        
    async def send_invite(self, user_id: int, content: str, activity_type: ActivityActionType):
        return await self._post_route("/send_invite", {
            "userId": user_id,
            "activityActionType": activity_type,
            "content": content
        })

    async def accept_invite(self, user_id: int):
        return await self._post_route("/accept_invite", {"userId": user_id})

    async def send_request_reply(self, user_id: int, reply: ActivityJoinRequestReply):
        return await self._post_route("/send_request_reply", {
            "userId": user_id,
            "reply": reply
        })

    async def set_activity(self, activity: dict):
        return await self._post_route("/set_activity", activity)

    async def clear_activity(self):
        return await self._post_route("/clear_activity", {})

    async def close(self):
        if self.session:
            await self.session.close()
        else:
            raise DiscordBridgeError("Cannot close, no session.")

class __DiscordService:
    def __init__(self, clientId: int, ws: str = "ws://localhost:5000/ws"):
        self.clientId = clientId
        self.host = ws
    
    async def __loop(self):
        async with websockets.connect(self.host) as websocket:
            logging.debug("Connected to Discord bridge websocket")
            while True:
                try:
                    msg = await websocket.recv()
                    
                    data: dict = json.loads(msg)
                    event_name = data.get('event') or data.get('eventName') or 'unknown'
                    event_data = data.get('data', {})

                    logging.debug(f"[event] {event_name}")
                    logging.debug(f"{json.dumps(event_data, indent=2)}")

                    __Events.Call(event_name, event_data)

                except websockets.exceptions.ConnectionClosed:
                    raise WebSocketDisconnectedError("Connection closed by the server.")
                except json.JSONDecodeError as e:
                    raise EventProcessingError(f"Failed to parse event: {e}")
                except Exception as e:
                    raise EventProcessingError(f"Unexpected error during event processing: {e}")
    
    async def run_service(self, max_retries: int = -1):
        retries = 0
        while max_retries == -1 or retries < max_retries:
            try:
                await self.__loop()
            except WebSocketDisconnectedError as e:
                logging.warning(f"[!] {e}")
                break
            except BridgeConnectionError as e:
                logging.error(f"[!] Bridge connection error: {e}")
                retries += 1
                await asyncio.sleep(3)
            except EventProcessingError as e:
                logging.error(f"[!] {e}")