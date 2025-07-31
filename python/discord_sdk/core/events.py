import logging
import typing as tp

class __Events:
    __hooks: dict[str, dict[str, tp.Callable]] = {}
    
    @classmethod
    def Add(cls, event_name: str, indentifier: str, callback: tp.Callable) -> None:
        if event_name not in cls.__hooks:
            cls.__hooks[event_name] = {}
        
        cls.__hooks[event_name][indentifier] = callback
        logging.debug(f"Hook added: {event_name} [{indentifier}]")
    
    @classmethod
    def Remove(cls, event_name: str, identifier: str) -> None:
        if event_name in cls.__hooks:
            del cls.__hooks[event_name][identifier]
            logging.debug(f"Hook removed: {event_name} [{identifier}]")
    
    @classmethod
    def CallById(cls, event_name: str, identifier: str, *args, **kwargs) -> tp.Any:
        callback = cls.__hooks.get(event_name, {}).get(identifier)
        
        if not callable(callback):
            # logging.warning(f"Hook not found or not callable: {event_name} [{identifier}]")
            return None

        try:
            result = callback(*args, **kwargs)
            logging.debug(f"Hook called: {event_name} [{identifier}]")
            return result
        except Exception as e:
            logging.warning(f"Hook error ({event_name}:{identifier}): {e}")
            return None
    
    @classmethod
    def Call(cls, event_name: str, *args, **kwargs) -> list:
        results = []

        for identifier in cls.__hooks.get(event_name, {}):
            try:
                result = cls.CallById(event_name, identifier, *args, **kwargs)
                results.append(result)
            except Exception as e:
                logging.warning(f"Hook error in Call(): {event_name} [{identifier}] => {e}")

        return results