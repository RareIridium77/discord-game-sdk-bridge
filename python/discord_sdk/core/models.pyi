from typing import Optional
from .enums import ActivityType

class DiscordAssets:
    """Visual assets for a Discord Rich Presence activity, including image keys and hover texts."""
    
    largeImage: Optional[str]
    largeImageText: Optional[str]
    smallImage: Optional[str]
    smallImageText: Optional[str]

    def __init__(
        self,
        largeImage: Optional[str] = ...,
        largeImageText: Optional[str] = ...,
        smallImage: Optional[str] = ...,
        smallImageText: Optional[str] = ...
    ) -> None: ...


class DiscordActivityParty:
    """Information about a party the user is in, including party ID and size."""
    
    Id: str
    currentSize: int
    maxSize: int

    def __init__(self, Id: str, currentSize: int, maxSize: int) -> None: ...


class DiscordActivitySecrets:
    """Secrets used to enable join/spectate functionality via Discord invites."""
    
    join: Optional[str]
    match: Optional[str]
    spectate: Optional[str]

    def __init__(
        self,
        join: Optional[str] = ...,
        match: Optional[str] = ...,
        spectate: Optional[str] = ...
    ) -> None: ...


class DiscordActivity:
    """
    Represents the full Discord Rich Presence activity.
    Includes name, state, timestamps, assets, party, and secrets.
    """
    
    type: Optional[ActivityType]
    name: Optional[str]
    state: Optional[str]
    details: Optional[str]
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    assets: Optional[DiscordAssets]
    party: Optional[DiscordActivityParty]
    secrets: Optional[DiscordActivitySecrets]
    instance: bool

    def __init__(
        self,
        type: Optional[ActivityType] = ...,
        name: Optional[str] = ...,
        state: Optional[str] = ...,
        details: Optional[str] = ...,
        start_timestamp: Optional[int] = ...,
        end_timestamp: Optional[int] = ...,
        assets: Optional[DiscordAssets] = ...,
        party: Optional[DiscordActivityParty] = ...,
        secrets: Optional[DiscordActivitySecrets] = ...,
        instance: bool = ...
    ) -> None: ...

    def to_dict(self) -> dict: ...
