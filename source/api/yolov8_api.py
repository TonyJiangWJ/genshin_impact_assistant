from yolov8.yolov8_predictor import YOLOv8
from source.util import *
import cv2

logger.info(t2t('Creating onnxruntime obj. It may takes a few second.'))


class Yolov8Api:

    def __init__(self, model='assets/Yolov8Models/yuanshen.onnx'):
        self.predictor = YOLOv8(model)

    def predict(self, img):
        return self.predictor.detect_objects(img)

    @staticmethod
    def get_center(box):
        x1, y1, x2, y2 = box
        logger.info(f'box: {x1:.2f}, {y1:.2f} - {x2:.2f}, {y2:.2f}')
        return x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2

    @staticmethod
    def get_area(box):
        x1, y1, x2, y2 = box
        return (x2 - x1) * (y2 - y1)


predictor = Yolov8Api()

logger.info(t2t('Created onnxruntime obj.'))
if __name__ == '__main__':
    image_path = 'H:/Projects/repository/GitHub/genshin_impact_assistant/assets/Yolov8Models/frame_270.jpg'
    img = cv2.imread(image_path)

    # Detect Objects
    results = predictor.predict(img)
    for result in results:
        x1, y1, x2, y2 = result.box
        print(f"find label: {result.label} score: {result.score} box: {x1:.2f}, {y1:.2f} - {x2:.2f}, {y2:.2f}")
