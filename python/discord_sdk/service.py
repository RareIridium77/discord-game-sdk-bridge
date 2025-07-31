from .core import __DiscordService, __DiscordBridge
from .core.models import DiscordActivity

class DiscordBridge(__DiscordBridge):
    def __init__(self, clientId, host = "http://localhost:5000"):
        super().__init__(clientId, host)
    
    async def set_activity(self, activity: DiscordActivity):
        data = activity.to_dict()
        return await super().set_activity(data)

import asyncio
import threading

class DiscordService(__DiscordService):
    def __init__(self, clientId: int, ws: str = "ws://localhost:5000/ws"):
        super().__init__(clientId, ws)
        self._thread = None
        self._loop = None

    async def run_service_async(self):
        return await super().run_service()

    def run_background(self):
        def _runner():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self.run_service_async())

        self._thread = threading.Thread(target=_runner, daemon=True)
        self._thread.start()
