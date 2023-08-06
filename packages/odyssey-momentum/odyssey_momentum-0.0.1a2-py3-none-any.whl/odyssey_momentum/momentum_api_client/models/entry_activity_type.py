from enum import Enum


class EntryActivityType(str, Enum):
    SCREENSHOT = "screenshot"
    STAKE = "stake"
    VIDEO = "video"
    WORLD_CREATED = "world_created"

    def __str__(self) -> str:
        return str(self.value)
