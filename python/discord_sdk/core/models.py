from .enums import ActivityType, ActivityJoinRequestReply, ActivityActionType

class DiscordAssets:
    def __init__(self, largeImage=None, largeImageText=None, smallImage=None, smallImageText=None):
        self.largeImage = largeImage
        self.largeImageText = largeImageText
        self.smallImage = smallImage
        self.smallImageText = smallImageText

class DiscordActivityParty:
    def __init__(self, Id: str, currentSize: int, maxSize: int):
        self.Id = Id
        self.currentSize = currentSize
        self.maxSize = maxSize

class DiscordActivitySecrets:
    def __init__(self, join: str = None, match: str = None, spectate: str = None):
        self.join = join
        self.match = match
        self.spectate = spectate

class DiscordActivity:
    def __init__(
        self,
            type: ActivityType=None,
            name=None,
            state=None,
            details=None,
            start_timestamp=None,
            end_timestamp=None,
            assets: DiscordAssets = None,
            party: DiscordActivityParty = None,
            secrets: DiscordActivitySecrets = None,
            instance=True
        ):
        self.type = type
        self.name = name
        self.state = state
        self.details = details
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        
        ## Class Based ##
        
        self.assets = assets
        self.party = party
        self.secrets = secrets
        
        ## Class Based ##
        
        self.instance = instance

    def to_dict(self):
        
        dType = 0
        dTypeT = ActivityType
        match self.type:
            case dTypeT.Playing: dType = 0
            case dTypeT.Streaming: dType = 1
            case dTypeT.Listening: dType = 2
            case dTypeT.Watching: dType = 3
        
        data = {
            "type": dType,
            "name": self.name,
            "state": self.state,
            "details": self.details,
            "startTimestamp": None,
            "endTimestamp": None,
            "largeImage": None,
            "largeImageText": None,
            "smallImage": None,
            "smallImageText": None,
            "party": {},
            "secrets": {},
            "instance": self.instance
        }

        # timestamps (flat)
        if self.start_timestamp is not None:
            data["startTimestamp"] = int(self.start_timestamp) if self.start_timestamp else None
        if self.end_timestamp is not None:
            data["endTimestamp"] = int(self.end_timestamp) if self.end_timestamp else None
        
        if not data["startTimestamp"]:
            del data["startTimestamp"]
        if not data["endTimestamp"]:
            del data["endTimestamp"]

        # assets
        if self.assets:
            data["largeImage"] = self.assets.largeImage
            data["largeImageText"] = self.assets.largeImageText
            data["smallImage"] = self.assets.smallImage
            data["smallImageText"] = self.assets.smallImageText
        else:
            del data["largeImage"]
            del data["largeImageText"]
            del data["smallImage"]
            del data["smallImageText"]

        # party
        if self.party:
            data["party"] = {
                "id": self.party.Id,
                "currentSize": self.party.currentSize,
                "maxSize": self.party.maxSize
            }
        else:
            del data["party"]

        # secrets
        if self.secrets:
            data["secrets"] = {
                "join": self.secrets.join,
                "match": self.secrets.match,
                "spectate": self.secrets.spectate
            }
            data["secrets"] = {k: v for k, v in data["secrets"].items() if v}
        else:
            del data["secrets"]

        # remove None or empty fields
        return {k: v for k, v in data.items() if v is not None and v != {}}
