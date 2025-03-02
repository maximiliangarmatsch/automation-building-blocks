def box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def intersection_area(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    return max(0, x2 - x1) * max(0, y2 - y1)


def IoU(box1, box2, return_max=True):
    intersection = intersection_area(box1, box2)
    union = box_area(box1) + box_area(box2) - intersection
    if box_area(box1) > 0 and box_area(box2) > 0:
        ratio1 = intersection / box_area(box1)
        ratio2 = intersection / box_area(box2)
    else:
        ratio1, ratio2 = 0, 0
    if return_max:
        return max(intersection / union, ratio1, ratio2)
    else:
        return intersection / union


def get_optimal_label_pos(text_padding, text_width, text_height, 
                          x1, y1, x2, y2, detections, image_size):
    """
    check overlap of text and background detection box
    """

    def get_is_overlap(detections, text_background_x1, text_background_y1,
                       text_background_x2, text_background_y2, image_size):
        is_overlap = False
        for i in range(len(detections)):
            detection = detections.xyxy[i].astype(int)
            if IoU([text_background_x1, text_background_y1, text_background_x2,
                    text_background_y2], detection) > 0.3:
                is_overlap = True
                break
        # check if the text is out of the image
        if (
            text_background_x1 < 0 or
            text_background_x2 > image_size[0] or
            text_background_y1 < 0 or
            text_background_y2 > image_size[1]
        ):
            is_overlap = True
        return is_overlap
    # if pos == 'top left':
    text_x = x1 + text_padding
    text_y = y1 - text_padding

    text_background_x1 = x1
    text_background_y1 = y1 - 2 * text_padding - text_height

    text_background_x2 = x1 + 2 * text_padding + text_width
    text_background_y2 = y1
    is_overlap = get_is_overlap(detections, text_background_x1,
                                text_background_y1, text_background_x2,
                                text_background_y2, image_size)
    if not is_overlap:
        return (text_x, text_y, text_background_x1, text_background_y1,
                text_background_x2, text_background_y2)
    # elif pos == 'outer left':
    text_x = x1 - text_padding - text_width
    text_y = y1 + text_padding + text_height

    text_background_x1 = x1 - 2 * text_padding - text_width
    text_background_y1 = y1

    text_background_x2 = x1
    text_background_y2 = y1 + 2 * text_padding + text_height
    is_overlap = get_is_overlap(detections, text_background_x1,
                                text_background_y1, text_background_x2,
                                text_background_y2, image_size)
    if not is_overlap:
        return (text_x, text_y, text_background_x1,
                text_background_y1, text_background_x2,
                text_background_y2)

    # elif pos == 'outer right':
    text_x = x2 + text_padding
    text_y = y1 + text_padding + text_height

    text_background_x1 = x2
    text_background_y1 = y1

    text_background_x2 = x2 + 2 * text_padding + text_width
    text_background_y2 = y1 + 2 * text_padding + text_height

    is_overlap = get_is_overlap(detections, text_background_x1,
                                text_background_y1, text_background_x2,
                                text_background_y2, image_size)
    if not is_overlap:
        return (text_x, text_y, text_background_x1, text_background_y1,
                text_background_x2, text_background_y2)

    # elif pos == 'top right':
    text_x = x2 - text_padding - text_width
    text_y = y1 - text_padding

    text_background_x1 = x2 - 2 * text_padding - text_width
    text_background_y1 = y1 - 2 * text_padding - text_height

    text_background_x2 = x2
    text_background_y2 = y1

    is_overlap = get_is_overlap(detections, text_background_x1,
                                text_background_y1, text_background_x2,
                                text_background_y2, image_size)
    if not is_overlap:
        return (text_x, text_y, text_background_x1, text_background_y1,
                text_background_x2, text_background_y2)

    return (text_x, text_y, text_background_x1, text_background_y1,
            text_background_x2, text_background_y2)
