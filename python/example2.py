import time
import uuid

import asyncio

### Discord SDK ###

from discord_sdk import DiscordBridge, Events
from discord_sdk.models import DiscordActivity, DiscordAssets, DiscordActivityParty, DiscordActivitySecrets
from discord_sdk.enums import ActivityType
from discord_sdk.service import DiscordService

### Discord SDK ###

client_id = 1234567891234567890 # YOU DISCORD APPLICATION CLIENT ID

## Only Discord Service will run Events.Call ##

# Example event
def on_join(data):
    print(">>> Join event:", data)

Events.Add("join", "handle_join", on_join)

## Only Discord Service will run Events.Call ##

async def main():
    bridge = DiscordBridge(client_id)
    await bridge.connect()
    await bridge.enable_discord_bridge()
    
    activity = DiscordActivity(
        ActivityType.Playing,
        state="Im doing good",
        details="Fuck you",
        start_timestamp=time.time(),
        assets=DiscordAssets(
            smallImage="gm_construct",
            smallImageText="gm_construct"
        ),
        party=DiscordActivityParty(
            Id=str(uuid.uuid4()),
            currentSize=5,
            maxSize=16
        ),
        secrets=DiscordActivitySecrets(
            join=str(uuid.uuid4())
        ),
        instance=False
    )
    
    response = await bridge.set_activity(activity)
    print(response)
    await bridge.close()
    
    service = DiscordService(client_id)
    service.run_service()
    
asyncio.run(main())