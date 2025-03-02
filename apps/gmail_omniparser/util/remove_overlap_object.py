from typing import List
import torch


def box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def intersection_area(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    return max(0, x2 - x1) * max(0, y2 - y1)


def IoU(box1, box2):
    intersection = intersection_area(box1, box2)
    union = box_area(box1) + box_area(box2) - intersection + 1e-6
    if box_area(box1) > 0 and box_area(box2) > 0:
        ratio1 = intersection / box_area(box1)
        ratio2 = intersection / box_area(box2)
    else:
        ratio1, ratio2 = 0, 0
    return max(intersection / union, ratio1, ratio2)


def is_inside(box1, box2, threshold):
    intersection = intersection_area(box1, box2)
    ratio1 = intersection / box_area(box1)
    return ratio1 > threshold


def remove_overlap(boxes, iou_threshold, ocr_bbox=None):
    assert ocr_bbox is None or isinstance(ocr_bbox, List)
    boxes = boxes.tolist()
    filtered_boxes = []
    if ocr_bbox:
        filtered_boxes.extend(ocr_bbox)
    # print('ocr_bbox!!!', ocr_bbox)
    for i, box1 in enumerate(boxes):
        is_valid_box = True
        for j, box2 in enumerate(boxes):
            # keep the smaller box
            if (i != j and IoU(box1, box2) >
                    iou_threshold and box_area(box1) >
                    box_area(box2)):
                is_valid_box = False
                break
        if is_valid_box:
            # add the following 2 lines to include ocr bbox
            if ocr_bbox:
                # only add the box if it does not overlap with any ocr bbox
                if not any(IoU(box1, box3) > iou_threshold and
                           not is_inside(box1, box3, 0.95)
                           for k, box3 in enumerate(ocr_bbox)):
                    filtered_boxes.append(box1)
            else:
                filtered_boxes.append(box1)
    return torch.tensor(filtered_boxes)


def remove_overlap_new(boxes, iou_threshold, ocr_bbox=None):
    assert ocr_bbox is None or isinstance(ocr_bbox, List)
    # boxes = boxes.tolist()
    filtered_boxes = []
    if ocr_bbox:
        filtered_boxes.extend(ocr_bbox)
    # print('ocr_bbox!!!', ocr_bbox)
    for i, box1_elem in enumerate(boxes):
        box1 = box1_elem['bbox']
        is_valid_box = True
        for j, box2_elem in enumerate(boxes):
            # keep the smaller box
            box2 = box2_elem['bbox']
            if i != j and IoU(box1, box2) > iou_threshold and box_area(box1) > box_area(box2):
                is_valid_box = False
                break
        if is_valid_box:
            if ocr_bbox:
                # keep yolo boxes + prioritize ocr label
                box_added = False
                ocr_labels = ''
                for box3_elem in ocr_bbox:
                    if not box_added:
                        box3 = box3_elem['bbox']
                        if is_inside(box3, box1, 0.80):  # ocr inside icon
                            # box_added = True
                            # delete the box3_elem from ocr_bbox
                            try:
                                # gather all ocr labels
                                ocr_labels += box3_elem['content'] + ' '
                                filtered_boxes.remove(box3_elem)
                            except Exception as e:
                                continue
                            # break
                        elif is_inside(box1, box3, 0.80):
                            box_added = True
                            break
                        else:
                            continue
                if not box_added:
                    if ocr_labels:
                        filtered_boxes.append({'type': 'icon',
                                               'bbox': box1_elem['bbox'],
                                               'interactivity': True,
                                               'content': ocr_labels,
                                               'source': 'box_yolo_content_ocr'
                                               })
                    else:
                        filtered_boxes.append({'type': 'icon',
                                               'bbox': box1_elem['bbox'],
                                               'interactivity': True,
                                               'content': None,
                                               'source':
                                               'box_yolo_content_yolo'
                                               })
            else:
                filtered_boxes.append(box1)
    return filtered_boxes  # torch.tensor(filtered_boxes)