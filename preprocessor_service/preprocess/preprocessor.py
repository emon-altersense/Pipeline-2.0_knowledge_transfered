from abc import ABC, abstractmethod


class Preprocessor(ABC):
    """
    Abstract class for defining the preprocessing pipeline.
    """

    @abstractmethod
    def preprocess(self, data):
        """
        Preprocess the data according to the model pipeline.
        """
        return data


class ImageProcessor(Preprocessor, ABC):
    """
    Abstract class for defining the image processing pipeline.
    """

    @abstractmethod
    def deserialize(self, data):
        """
        Convert bytes of image to appropriate image format before processing.
        """
        pass
