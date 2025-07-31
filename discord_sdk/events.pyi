from typing import Any, Callable

class Events:
    """
    Events for DiscordService.

    You can register, remove and call hooks dynamically.
    Each hook is identified by a unique string identifier and grouped by event names.

    Example usage:
        Events.Add("on_ready", "my_module", callback)
        Events.Remove("on_ready", "my_module")
    """

    @classmethod
    def Add(cls, event_name: str, identifier: str, callback: Callable) -> None:
        """
        Register a new event callback.

        :param event_name: The name of the event.
        :param identifier: Unique identifier for the callback (e.g., module name).
        :param callback: Callable that will be invoked when the event is fired.
        """
        ...

    @classmethod
    def Remove(cls, event_name: str, identifier: str) -> None:
        """
        Remove a previously registered callback.

        :param event_name: The name of the event.
        :param identifier: The identifier used when adding the callback.
        """
        ...