import io
import base64
import time
from typing import Union
from PIL import Image
import numpy as np
import torch
from torchvision.ops import box_convert
from remove_overlap_object import remove_overlap_new
from create_labled_image_helper import (predict_yolo, int_box_area,
                                        get_parsed_content_icon_phi3v,
                                        get_parsed_content_icon)
from utils import annotate


def get_som_labeled_img(image_source: Union[str, Image.Image],
                        model=None, BOX_TRESHOLD=0.01,
                        output_coord_in_ratio=False, ocr_bbox=None,
                        text_scale=0.4, text_padding=5,
                        draw_bbox_config=None, caption_model_processor=None,
                        ocr_text=[], use_local_semantics=True, iou_threshold=0.9,
                        prompt=None, scale_img=False, imgsz=None, batch_size=128
                        ):
    if isinstance(image_source, str):
        image_source = Image.open(image_source)
    image_source = image_source.convert("RGB")  # for CLIP
    w, h = image_source.size
    if not imgsz:
        imgsz = (h, w)
    xyxy, logits, phrases = predict_yolo(
        model=model,
        image=image_source,
        box_threshold=BOX_TRESHOLD,
        imgsz=imgsz,
        scale_img=scale_img,
        iou_threshold=0.1)
    xyxy = xyxy / torch.Tensor([w, h, w, h]).to(xyxy.device)
    image_source = np.asarray(image_source)
    phrases = [str(i) for i in range(len(phrases))]

    # annotate the image with labels
    if ocr_bbox:
        ocr_bbox = torch.tensor(ocr_bbox) / torch.Tensor([w, h, w, h])
        ocr_bbox = ocr_bbox.tolist()
    else:
        print('no ocr bbox!!!')
        ocr_bbox = None

    ocr_bbox_elem = [
        {
            'type': 'text',
            'bbox': box,
            'interactivity': False,
            'content': txt,
            'source': 'box_ocr_content_ocr'
        }
        for box, txt in zip(ocr_bbox, ocr_text) if int_box_area(box, w, h) > 0
    ]
    xyxy_elem = [
        {
            'type': 'icon',
            'bbox': box,
            'interactivity': True,
            'content': None
        }
        for box in xyxy.tolist() if int_box_area(box, w, h) > 0
    ]
    filtered_boxes = remove_overlap_new(
        boxes=xyxy_elem,
        iou_threshold=iou_threshold,
        ocr_bbox=ocr_bbox_elem
    )
    
    filtered_boxes_elem = sorted(filtered_boxes,
                                 key=lambda x: x['content'] is None)
    # get the index of the first 'content': None
    starting_idx = next((i for i,
                         box in enumerate(filtered_boxes_elem)
                         if box['content'] is None), -1)
    filtered_boxes = torch.tensor([box['bbox'] for box in filtered_boxes_elem])
    print('len(filtered_boxes):', len(filtered_boxes), starting_idx)
    # get parsed icon local semantics
    time1 = time.time()
    if use_local_semantics:
        caption_model = caption_model_processor['model']
        if 'phi3_v' in caption_model.config.model_type:
            parsed_content_icon = get_parsed_content_icon_phi3v(
                filtered_boxes,
                ocr_bbox,
                image_source,
                caption_model_processor
            )
        else:
            parsed_content_icon = get_parsed_content_icon(
                filtered_boxes,
                starting_idx,
                image_source,
                caption_model_processor,
                prompt=prompt,
                batch_size=batch_size
            )
        ocr_text = [f"Text Box ID {i}: {txt}" for i, txt in enumerate(ocr_text)]
        icon_start = len(ocr_text)
        content_icon_ls = []
        for i, box in enumerate(filtered_boxes_elem):
            if box['content'] is None:
                box['content'] = parsed_content_icon.pop(0)
        for i, txt in enumerate(parsed_content_icon):
            content_icon_ls.append(f"Icon Box ID {str(i+icon_start)}: {txt}")
        parsed_content_merged = ocr_text + content_icon_ls
    else:
        ocr_text = [f"Text Box ID {i}: {txt}" for i,
                    txt in enumerate(ocr_text)]
        parsed_content_merged = ocr_text
    print('time to get parsed data:', time.time()-time1)

    filtered_boxes = box_convert(boxes=filtered_boxes,
                                 in_fmt="xyxy", out_fmt="cxcywh")
    phrases = [i for i in range(len(filtered_boxes))]
    # draw boxes
    if draw_bbox_config:
        annotated_frame, label_coordinates = annotate(
            image_source=image_source,
            boxes=filtered_boxes,
            logits=logits,
            phrases=phrases,
            **draw_bbox_config
        )
    else:
        annotated_frame, label_coordinates = annotate(
            image_source=image_source,
            boxes=filtered_boxes,
            logits=logits,
            phrases=phrases,
            text_scale=text_scale,
            text_padding=text_padding
        )
    pil_img = Image.fromarray(annotated_frame)
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('ascii')
    if output_coord_in_ratio:
        label_coordinates = {
            k: [v[0]/w, v[1]/h, v[2]/w,
                v[3]/h] for k, v in label_coordinates.items()
        }
        assert w == annotated_frame.shape[1] and h == annotated_frame.shape[0]
    return encoded_image, label_coordinates, filtered_boxes_elem
