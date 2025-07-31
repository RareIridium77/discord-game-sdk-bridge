"""
Basic exceptions for discord_sdk bridge
"""
class DiscordBridgeError(Exception):
    """Base class for Discord Bridge exceptions."""
    pass

class RouteNotAllowedError(DiscordBridgeError):
    """Raised when attempting to access a disallowed route."""
    pass

class BridgeConnectionError(DiscordBridgeError):
    """Raised when the bridge fails to connect."""
    pass

class WebSocketDisconnectedError(DiscordBridgeError):
    """Raised when the websocket connection is unexpectedly closed."""
    pass

class EventProcessingError(DiscordBridgeError):
    """Raised when an event fails to be processed."""
    pass
