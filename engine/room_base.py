"""Room base class for MindMaze. All rooms implement `enter(ctx) -> bool`."""
from abc import ABC, abstractmethod

class Room(ABC):
    @abstractmethod
    def enter(self, ctx) -> bool:
        """Run the room. Return True if escaped, else False."""
        raise NotImplementedError
