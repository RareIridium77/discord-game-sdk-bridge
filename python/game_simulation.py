import time
import asyncio
import random

### Discord SDK ###

from discord_sdk import DiscordBridge
from discord_sdk.models import DiscordActivity, DiscordAssets, DiscordActivityParty, DiscordActivitySecrets
from discord_sdk.enums import ActivityType

### Discord SDK ###

client_id = 1234567891234567890 # YOU DISCORD APPLICATION CLIENT ID

GAME_LEVELS = [
    ("Sante Mari - Under Attack", "level_santemari", "Sante Mari"),
    ("Gas Station - Final Fight", "level_gasstation", "Gas Station"),
    ("Airport - Night Raid", "level_airport", "Airport"),
]

MAX_PLAYERS = 8

def pseudoLog(*args):
    print("[GAME]", *args)

class GameActivity:
    def __init__(self, bridge: DiscordBridge):
        self.bridge = bridge
        self.start_time = time.time()

        self.activity = DiscordActivity(
            type=ActivityType.Playing,
            name="My Game",
            details="Initializing...",
            state="",
            start_timestamp=self.start_time,
            assets=DiscordAssets(
                largeImage="game_logo",
                largeImageText="My Game"
            ),
            party=None,  # None in menu
            instance=True
        )

        self.player_count = 1

    async def update_activity(self):
        await self.bridge.set_activity(self.activity)

    def set_menu(self, label="Main Menu"):
        pseudoLog("Entered menu:", label)
        self.activity.details = "In Menu"
        self.activity.state = label
        self.activity.assets.smallImage = None
        self.activity.assets.smallImageText = None
        self.activity.party = None

    def set_level(self, level_name, image_key, image_text):
        pseudoLog("Starting level:", level_name)
        self.activity.details = "Playing"
        self.activity.state = level_name
        self.activity.assets.smallImage = image_key
        self.activity.assets.smallImageText = image_text
        self.activity.party = DiscordActivityParty(
            Id="rf-party-123",
            currentSize=self.player_count,
            maxSize=MAX_PLAYERS
        )

    def simulate_player_join(self):
        if self.activity.party and self.player_count < MAX_PLAYERS:
            self.player_count += 1
            self.activity.party.currentSize = self.player_count
            pseudoLog(f"Player joined: {self.player_count}/{MAX_PLAYERS}")

async def game_simulation(activity: GameActivity):
    while True:
        activity.set_menu()
        await activity.update_activity()
        await asyncio.sleep(random.uniform(3, 5))

        level = random.choice(GAME_LEVELS)
        activity.player_count = 1  # reset party size
        activity.set_level(*level)
        await activity.update_activity()

        for _ in range(random.randint(2, 5)):
            await asyncio.sleep(random.uniform(2, 4))
            activity.simulate_player_join()
            await activity.update_activity()

        await asyncio.sleep(random.uniform(6, 8))

async def main():
    bridge = DiscordBridge(client_id)
    
    await bridge.connect()
    await bridge.enable_discord_bridge() ## Enable discord sdk
    
    activity = GameActivity(bridge)

    pseudoLog("Connected to Discord")
    await activity.update_activity()

    try:
        await game_simulation(activity)
    finally:
        pseudoLog("Exiting game...")
        await bridge.clear_activity()
        await bridge.disable_discord_bridge()
        await bridge.close()

if __name__ == "__main__":
    asyncio.run(main())