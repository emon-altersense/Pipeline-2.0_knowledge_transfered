from abc import ABC, abstractmethod


class Producer(ABC):
    """
    Abstract class for a Producer Source.
    """

    @abstractmethod
    def connect(self):
        """
        Connect to the Producer Source
        """
        raise NotImplementedError("Must be implemented by subclasses")

    @abstractmethod
    def produce(self, data):
        """
        Produce data to the connected source
        """
        raise NotImplementedError("Must be implemented by subclasses")

    def disconnect(self):
        """
        Disconnect from the Producer Source.

        This method is optional. Can be implemented by subclasses if requires.
        """
        pass
