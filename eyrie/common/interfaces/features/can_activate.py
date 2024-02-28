from abc import (
    ABC,
    abstractmethod,
)


class CanActivate(ABC):
    """
    Interface defining the `can_activate()` function that must be implemented
    by a guard.  Return value indicates whether or not the current request is
    allowed to proceed.
    """

    @abstractmethod
    def can_activate(self):
        pass
