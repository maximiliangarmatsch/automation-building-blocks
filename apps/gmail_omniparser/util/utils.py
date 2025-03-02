from typing import Tuple, List, Union
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO
# %matplotlib inline
from matplotlib import pyplot as plt
import easyocr
from paddleocr import PaddleOCR
import torch
from torchvision.ops import box_convert
import supervision as sv
import torchvision.transforms as T
from util.box_annotator import BoxAnnotator
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from transformers import AutoProcessor, AutoModelForCausalLM
reader = easyocr.Reader(['en'])
paddle_ocr = PaddleOCR(lang='en', use_angle_cls=False, use_gpu=False,
                       show_log=False, max_batch_size=1024, use_dilation=True,
                       det_db_score_mode='slow', rec_batch_num=1024)


def get_caption_model_processor(model_name, model_name_or_path=None,
                                device=None):
    if not device:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model = None
    processor = None
    if model_name_or_path is None:
        if model_name == "blip2":
            model_name_or_path = "Salesforce/blip2-opt-2.7b"
        elif model_name == "florence2":
            model_name_or_path = "microsoft/Florence-2-base"
    # Load the appropriate model and processor
    if model_name == "blip2":
        processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
        if device == 'cpu':
            model = Blip2ForConditionalGeneration.from_pretrained(
                model_name_or_path, device_map=None, torch_dtype=torch.float32)
        else:
            model = Blip2ForConditionalGeneration.from_pretrained(
                model_name_or_path, device_map=None,
                torch_dtype=torch.float16).to(device)
    elif model_name == "florence2":
        processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base",
                                                  trust_remote_code=True)
        if device == 'cpu':
            model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                         torch_dtype=torch.float32,
                                                         trust_remote_code=True)
        else:
            model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                                         torch_dtype=torch.float16,
                                                         trust_remote_code=True).to(device)

    if model is not None:
        model = model.to(device)    
    return {'model': model, 'processor': processor}


def get_yolo_model(model_path):
    model = YOLO(model_path)
    return model


def load_image(image_path: str) -> Tuple[np.array, torch.Tensor]:
    transform = T.Compose(
        [
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image_source = Image.open(image_path).convert("RGB")
    image = np.asarray(image_source)
    image_transformed, _ = transform(image_source, None)
    return image, image_transformed


def annotate(image_source: np.ndarray, boxes: torch.Tensor,
             logits: torch.Tensor, phrases: List[str], text_scale: float,
             text_padding=5, text_thickness=2, thickness=3) -> np.ndarray:
    h, w, _ = image_source.shape
    boxes = boxes * torch.Tensor([w, h, w, h])
    xyxy = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
    xywh = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xywh").numpy()
    detections = sv.Detections(xyxy=xyxy)
    labels = [f"{phrase}" for phrase in range(boxes.shape[0])]
    box_annotator = BoxAnnotator(text_scale=text_scale, text_padding=text_padding,
                                 text_thickness=text_thickness, thickness=thickness)
    annotated_frame = image_source.copy()
    annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections,
                                             labels=labels, image_size=(w, h))

    label_coordinates = {f"{phrase}": v for phrase, v in zip(phrases, xywh)}
    return annotated_frame, label_coordinates


def predict(model, image, caption, box_threshold, text_threshold):
    model, processor = model['model'], model['processor']
    device = model.device

    inputs = processor(images=image, text=caption,
                       return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        box_threshold=box_threshold,  # 0.4,
        text_threshold=text_threshold,  # 0.3,
        target_sizes=[image.size[::-1]]
    )[0]
    boxes, logits, phrases = results["boxes"], results["scores"], results["labels"]
    return boxes, logits, phrases


def get_xywh(input_data):
    x, y, w, h = (input_data[0][0], input_data[0][1],
                  input_data[2][0] - input_data[0][0],
                  input_data[2][1] - input_data[0][1])
    x, y, w, h = int(x), int(y), int(w), int(h)
    return x, y, w, h


def get_xyxy(input_data):
    x, y, xp, yp = input_data[0][0], input_data[0][1], input_data[2][0], input_data[2][1]
    x, y, xp, yp = int(x), int(y), int(xp), int(yp)
    return x, y, xp, yp


def get_xywh_yolo(input_data):
    x, y, w, h = (input_data[0], input_data[1],
                  input_data[2] - input_data[0], input_data[3] - input_data[1])
    x, y, w, h = int(x), int(y), int(w), int(h)
    return x, y, w, h


def check_ocr_box(image_source: Union[str, Image.Image], display_img=True,
                  output_bb_format='xywh', goal_filtering=None, easyocr_args=None,
                  use_paddleocr=False):
    if isinstance(image_source, str):
        image_source = Image.open(image_source)
    if image_source.mode == 'RGBA':
        # Convert RGBA to RGB to avoid alpha channel issues
        image_source = image_source.convert('RGB')
    image_np = np.array(image_source)
    w, h = image_source.size
    if use_paddleocr:
        if easyocr_args is None:
            text_threshold = 0.5
        else:
            text_threshold = easyocr_args['text_threshold']
        result = paddle_ocr.ocr(image_np, cls=False)[0]
        coord = [item[0] for item in result if item[1][1] > text_threshold]
        text = [item[1][0] for item in result if item[1][1] > text_threshold]
    else:  # EasyOCR
        if easyocr_args is None:
            easyocr_args = {}
        result = reader.readtext(image_np, **easyocr_args)
        coord = [item[0] for item in result]
        text = [item[1] for item in result]
    if display_img:
        opencv_img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        bb = []
        for item in coord:
            x, y, a, b = get_xywh(item)
            bb.append((x, y, a, b))
            cv2.rectangle(opencv_img, (x, y), (x+a, y+b), (0, 255, 0), 2)
        #  matplotlib expects RGB
        plt.imshow(cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB))
    else:
        if output_bb_format == 'xywh':
            bb = [get_xywh(item) for item in coord]
        elif output_bb_format == 'xyxy':
            bb = [get_xyxy(item) for item in coord]
    return (text, bb), goal_filtering
