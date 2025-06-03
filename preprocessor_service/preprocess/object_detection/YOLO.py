import numpy as np
import cv2
from ..preprocessor import ImageProcessor

target_shape = [640, 640]


class YOLOv8Preprocessor(ImageProcessor):
    """
    Preprocessor for YOLOv8 model.
    """

    def deserialize(self, image_buffer: bytes) -> np.ndarray:
        """
        Deserializes image buffer to numpy array.

        Args:
            image_buffer: Image buffer to be deserialized.

        Returns:
            Numpy array of the image.
        """
        return cv2.imdecode(
            buf=np.frombuffer(buffer=image_buffer, dtype=np.uint8),
            flags=cv2.IMREAD_COLOR,
        )

    async def preprocess(self, data) -> dict:
        """
        Preprocesses the data for YOLOv8 model

        Args:
            data: Kafka message data to be preprocessed.
        """
        frame_data = self.deserialize(data[1])
        original_shape = frame_data.shape[:2]

        scale = min(target_shape[0] / original_shape[0], target_shape[1] / original_shape[1])
        new_unpad = (int(original_shape[1] * scale + 0.5), int(original_shape[0] * scale + 0.5))
        dw, dh = int((target_shape[1] - new_unpad[0]) / 2), int((target_shape[0] - new_unpad[1]) / 2)

        if original_shape[::-1] != new_unpad:
            frame_data = cv2.resize(frame_data, new_unpad, interpolation=cv2.INTER_LINEAR)

        frame_data = cv2.copyMakeBorder(
            src=frame_data,
            top=dh, bottom=int(dh + 0.5),
            left=dw, right=int(dw + 0.5),
            borderType=cv2.BORDER_CONSTANT,
            value=(114, 114, 114)
        )
        frame_data = np.ascontiguousarray(
            frame_data[..., ::-1].transpose((2, 0, 1))
        )

        return {
            "camera_id": int(data[0].decode("utf-8")),
            "timestamp": data[2][1],
            "frame_shape": frame_data.shape,
            "frame_dtype": str(frame_data.dtype),
            "frame": [frame_data.tobytes()],
        }


class YOLO11Preprocessor(YOLOv8Preprocessor):
    """
    Preprocessor for YOLOv11 model which is the same as YOLOv8.
    """
    pass
