from abc import ABC, abstractmethod


class Consumer(ABC):
    """
    Abstract class for a Consumer Source.
    """

    @abstractmethod
    def connect(self):
        """
        Connect to the Consumer source.
        """
        raise NotImplementedError("Must be implemented by subclasses")

    @abstractmethod
    def consume(self):
        """
        Consumes data from the connected source.
        """
        raise NotImplementedError("Must be implemented by subclasses")

    def disconnect(self):
        """
        Disconnect from the Consumer source.

        This method is optional. Can be implemented by subclasses if requires.
        """
        pass
