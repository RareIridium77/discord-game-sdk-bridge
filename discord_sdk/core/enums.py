from enum import Enum

class ActivityType(Enum):
    """
    The type of activity being set for Discord Rich Presence.  
    
    ActivityType:  
        Playing = 0  
        Streaming = 1  
        Listening = 2  
        Watching = 3  
    """
    Playing = 0,
    Streaming = 1
    Listening = 2
    Watching = 3

class ActivityActionType(Enum):
    """
    ActivityActionType:  
        Join = 1  
        Spectate
    """
    Join = 1
    Spectate = 2

class ActivityJoinRequestReply(Enum):
    """
    ActivityJoinRequestReply:  
        No  
        Yes  
        Ignore  
    """
    No = 0
    Yes = 1
    Ignore = 2
    