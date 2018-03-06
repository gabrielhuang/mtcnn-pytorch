import math
import cv2


def keep_largest(boxes):
    if len(boxes)==0:
        return []
    maxi = None
    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        width = x2-x1
        if maxi is None or width>maxi:
            maxi = width
            best_box = box
    return [best_box]

def round_box((x1, y1, x2, y2)):
    '''
    this will floor x1, y1 and ceil x2, y2
    '''
    X1 = int(math.floor(x1))
    Y1 = int(math.floor(y1))
    X2 = int(math.ceil(x2))
    Y2 = int(math.ceil(y2))
    return X1, Y1, X2, Y2


def add_box_margin((x1, y1, x2, y2), percent_width=1.5, percent_height=None, round=True):
    if percent_height is None:
        percent_height = percent_width
    cx = 0.5*(x1+x2)
    cy = 0.5*(y1+y2)
    width = x2-x1
    height = y2-y1
    WIDTH = width * percent_width
    HEIGHT = height * percent_height
    X1 = cx - WIDTH/2.
    X2 = cx + WIDTH/2.
    Y1 = cy - HEIGHT/2.
    Y2 = cy + HEIGHT/2.
    if round:
        X1, Y1, X2, Y2 = round_box((X1, Y1, X2, Y2))
    return X1, Y1, X2, Y2


def crop_pad(img, (x1, y1, x2, y2), pad_value=(0,0,0), resize=None):
    (x1, y1, x2, y2) = round_box((x1, y1, x2, y2))
    width = x2-x1
    height = y2-y1
    padded = cv2.copyMakeBorder(img, height, height, width, width,cv2.BORDER_CONSTANT,value=pad_value)
    cropped = padded[y1+height:y1+2*height, x1+width:x1+2*width].copy()
    if resize is not None:
        cropped = cv2.resize(cropped, resize, interpolation=cv2.INTER_CUBIC)
    return cropped
