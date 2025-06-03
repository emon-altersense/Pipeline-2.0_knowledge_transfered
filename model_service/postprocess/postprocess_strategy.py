from abc import ABC, abstractmethod


class PostprocessorStrategy(ABC):
    """
    Strategy Pattern for Postprocessing data.
    """

    @abstractmethod
    def postprocess(self, data):
        """
        Post processes the output.
        """
        raise NotImplementedError("Must be implemented by subclasses")

    def business_logic(self):
        """
        Business logic for the post processor.

        This method is optional. Can be implemented by subclasses if requires.
        """
        pass
