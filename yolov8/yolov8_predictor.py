import time
import cv2
import numpy as np
import onnxruntime

from yolov8.utils import xywh2xyxy, nms, draw_detections, yuanshen


class DetectResult:
    def __init__(self, box, score, class_id, label):
        self.box = box
        self.score = score
        self.class_id = class_id
        self.label = label


class YOLOv8:

    def __init__(self, path, conf_thres=0.7, iou_thres=0.5):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres

        # Initialize model
        self.initialize_model(path)

    def initialize_model(self, path):
        self.session = onnxruntime.InferenceSession(path,
                                                    providers=['CUDAExecutionProvider',
                                                               'CPUExecutionProvider'])
        # Get model info
        self.get_input_details()
        self.get_output_details()

    def detect_objects(self, image):
        input_tensor = self.prepare_input(image)

        # Perform inference on the image
        outputs = self.inference(input_tensor)

        self.boxes, self.scores, self.class_ids = self.process_output(outputs)
        result = []
        for box, score, cls_id in zip(self.boxes, self.scores, self.class_ids):
            result.append(DetectResult(box, score, cls_id, yuanshen[cls_id]))
        return result

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]

        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize input image
        input_img = cv2.resize(input_img, (self.input_width, self.input_height))

        # Scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
        # input_tensor = input_img[np.newaxis, :, :, :].astype(np.ubyte)

        return input_tensor

    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.session.run(self.output_names, {self.input_names[0]: input_tensor})

        print(f"Inference time: {(time.perf_counter() - start) * 1000:.2f} ms")
        return outputs

    def process_output(self, output):
        predictions = np.squeeze(output[0]).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_threshold, :]
        scores = scores[scores > self.conf_threshold]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        indices = nms(boxes, scores, self.iou_threshold)
        print('indices: %s' % str(indices))

        return boxes[indices], scores[indices], class_ids[indices]

    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        return boxes

    def rescale_boxes(self, boxes):

        # Rescale boxes to original image dimensions
        input_shape = np.array([self.input_width, self.input_height, self.input_width, self.input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])
        return boxes

    def draw_detections(self, image, draw_scores=True, mask_alpha=0.4):
        for idx in range(len(self.class_ids)):
            cls = self.class_ids[idx]
            score = self.scores[idx]
            print(f"classId: {cls} score: {score}")
        return draw_detections(image, self.boxes, self.scores,
                               self.class_ids, mask_alpha)

    def get_input_details(self):
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

    def get_output_details(self):
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]


if __name__ == '__main__':
    # from imread_from_url import imread_from_url

    model_path = 'H:/Projects/repository/GitHub/genshin_impact_assistant/assets/Yolov8Models/yuanshen.onnx'

    # Initialize YOLOv8 object detector
    yolov8_detector = YOLOv8(model_path, conf_thres=0.7, iou_thres=0.3)

    image_path = 'H:/Projects/repository/GitHub/genshin_impact_assistant/assets/Yolov8Models/frame_270.jpg'
    img = cv2.imread(image_path)

    # Detect Objects
    results = yolov8_detector.detect_objects(img)
    for result in results:
        x1, y1, x2, y2 = result.box
        print(f"find label: {result.label} score: {result.score} box: {x1:.2f}, {y1:.2f} - {x2:.2f}, {y2:.2f}")
    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)
    height, width = combined_img.shape[:2]
    cv2.imshow("Output", combined_img)
    cv2.waitKey(0)
    results = yolov8_detector.detect_objects(img)
