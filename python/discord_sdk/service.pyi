from .core import __DiscordService, __DiscordBridge
from .core.models import DiscordActivity
from .core.enums import ActivityActionType, ActivityJoinRequestReply

class DiscordBridge(__DiscordBridge):
    """
    A high-level interface for interacting with the Discord Bridge backend
    using a REST API. Wraps low-level functionality with object-oriented models.
    
    Args:
        clientId (int): Your Discord application's client ID.
        host (str, optional): The base URL of the bridge server. Defaults to "http://localhost:5000".
    """
    ...
    
    async def enable_discord_bridge(self):
        """
        Enables discord SDK.
        """
        ...
    
    async def disable_discord_bridge(self):
        """
        Disables discord SDK
        """
        ...
    
    async def send_invite(self, user_id: int, content: str, activity_type: ActivityActionType):
        """
        Send activity invite to user by user_id
        
        Args:
            user_id (int): discord user id
            content (str): message to send with invite
            activity_type (ActivityActionType): invite activity action type
        
        ActivityActionType:
            Join = 1  
            Spectate
        """
        ...
    
    async def accept_invite(self, user_id: int):
        """
        Accepts activity invite by user id

        Args:
            user_id (int): discord user id
        """
    
    async def send_request_reply(self, user_id: int, reply: ActivityJoinRequestReply):
        """
        Send join request reply to user by id

        Args:
            user_id (int): discord user id
            reply (ActivityJoinRequestReply): Join request reply enum
        
        ActivityJoinRequestReply:
            No  
            Yes  
            Ignore  
        """
        ...
    
    async def set_activity(self, activity: DiscordActivity):
        """
        Sets the current Discord Rich Presence activity.

        Args:
            activity (DiscordActivity): The activity to be shown on the user's Discord profile.

        Returns:
            The response from the bridge server.
        """
        ...
    
    async def clear_activity(self):
        """
        Clear current activity
        """
    
    async def close(self):
        """
        Closes bridge connection
        """
        ...


class DiscordService(__DiscordService):
    """
    A service client that connects to the Discord Bridge WebSocket backend
    and runs in the background to handle Discord events and updates in real-time.

    Args:
        clientId (int): Your Discord application's client ID.
        ws (str, optional): The WebSocket endpoint. Defaults to "ws://localhost:5000/ws".
    """
    ...

    async def run_service_async(self):
        """
        Asynchronously starts the WebSocket service loop.
        """
        ...

    def run_background(self):
        """
        Starts the WebSocket service in a background thread.
        This is useful for non-blocking integration into existing applications.
        """
        ...
