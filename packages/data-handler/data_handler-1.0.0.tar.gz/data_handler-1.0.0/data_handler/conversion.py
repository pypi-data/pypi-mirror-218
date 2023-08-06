"""Functions to convert between coco to yolo format and vice versa"""

import json
import os
import shutil
from pathlib import Path

import cv2
import numpy as np
import yaml
from pycocotools.coco import COCO
from tqdm import tqdm


def __clip_coords(boxes, shape):
    # Clip bounding xyxy bounding boxes to image shape (height, width)
    boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, shape[1])  # x1, x2
    boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, shape[0])  # y1, y2

def __xyxy2xywhn(x, w=640, h=640, clip=False, eps=0.0):
    # Convert nx4 boxes from [x1, y1, x2, y2] to [x, y, w, h] normalized where xy1=top-left, xy2=bottom-right
    if clip:
        __clip_coords(x, (h - eps, w - eps))  # warning: inplace clip
    y = np.copy(x)
    y[:, 0] = ((x[:, 0] + x[:, 2]) / 2) / w  # x center
    y[:, 1] = ((x[:, 1] + x[:, 3]) / 2) / h  # y center
    y[:, 2] = (x[:, 2] - x[:, 0]) / w  # width
    y[:, 3] = (x[:, 3] - x[:, 1]) / h  # height
    return y

def __xywhn2xyxy(x, w=640, h=640, padw=0, padh=0):
    # Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = np.copy(x)
    y[:, 0] = w * (x[:, 0] - x[:, 2] / 2) + padw  # top left x
    y[:, 1] = h * (x[:, 1] - x[:, 3] / 2) + padh  # top left y
    y[:, 2] = w * (x[:, 0] + x[:, 2] / 2) + padw  # bottom right x
    y[:, 3] = h * (x[:, 1] + x[:, 3] / 2) + padh  # bottom right y
    y = [float(f"{a:.2f}") for a in y[0]]
    return y

def coco_to_yolo(annotation_file, output_folder, images_folder=None):

    """ Converts coco annotatation format to yolo format along with input_data.yml required in training.

    Args:
        annotation_file (str): coco json file path
        output_folder (str): output folder path to save yolo format files
        images_folder (str): original images folder to copy images to yolo output folder.
            Defaults to None. If None, images will not be copied.
    """

    coco = COCO(annotation_file)
    output_folder = Path(output_folder)
    (output_folder / 'labels').mkdir(parents=True, exist_ok=True)
    labels = output_folder / 'labels'

    names = [x["name"] for x in coco.loadCats(coco.getCatIds())]
    with open(output_folder / 'input_data.yaml', 'w') as f:
        yaml.dump({'download': '',
                   'names': names,
                   'nc': len(names),
                   'train': '',
                   'val': ''}, f)

    if images_folder is not None:
        images_folder = Path(images_folder)
        input_images = os.listdir(images_folder)
        (output_folder / 'images').mkdir(parents=True, exist_ok=True)
        images = output_folder / 'images'
        for image in tqdm(input_images):
            shutil.copy(images_folder / image, images / image)

    for cid, cat in enumerate(names):
        catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=catIds)
        for im in tqdm(coco.loadImgs(imgIds), desc=f'Class {cid + 1}/{len(names)} {cat}'):
            width, height = im["width"], im["height"]
            path = Path(im["file_name"])  # image filename
            try:
                with open(labels / path.with_suffix('.txt').name, 'a') as file:
                    annIds = coco.getAnnIds(imgIds=im["id"], catIds=catIds, iscrowd=None)
                    for a in coco.loadAnns(annIds):
                        if a["iscrowd"] == 1:
                            continue
                        x, y, w, h = a['bbox']  # bounding box in xywh (xy top-left corner)
                        x, y, w, h = float(x), float(y), float(w), float(h)
                        xyxy = np.array([x, y, x + w, y + h])[None]  # pixels(1,4)
                        x, y, w, h = __xyxy2xywhn(xyxy, w=width, h=height, clip=True)[0]  # normalized and clipped
                        file.write(f"{cid} {x:.5f} {y:.5f} {w:.5f} {h:.5f}\n")
            except Exception as e:
                print(e)

def yolo_to_coco(yolo_folder, coco_json, confidence=False):

    """ Converts yolo format to coco format along with input_data.yml required in training.

    Args:
        yolo_folder (str): yolo format folder path
        coco_json (str): coco json file path
    """

    yolo_folder = Path(yolo_folder)
    labels = yolo_folder / 'labels'
    images = yolo_folder / 'images'

    names = yaml.load(open(yolo_folder / 'input_data.yaml'), Loader=yaml.loader.SafeLoader)['names']
    categories = [{'supercategory': 'none', 'id': i + 1, 'name': names[i]} for i in tqdm(range(len(names)), desc='Categories')]

    images_coco = []
    images_dict = {}
    for image_id, image in enumerate(tqdm(os.listdir(images), desc='Images')):
        img = cv2.imread(str(images / image))
        height, width, _ = img.shape
        images_coco.append({'id': image_id + 1, 'file_name': image, 'height': height, 'width': width})
        len_ext = len(image.split('.')[-1]) + 1
        images_dict[image[:-len_ext]] = image_id + 1

    annotations = []
    annotation_id = 1
    for label in tqdm(os.listdir(labels), desc='annotations'):
        label_path = labels / label
        for ext in ['.jpg', '.png', '.jpeg']:
            img = cv2.imread(str(images / label)[:-len(ext)] + ext)
            if img is not None:
                height, width = img.shape[:2]
                break
        if img is None:
            raise Exception(f'Image not found for label: {label}')
        with open(label_path, 'r') as file:
            for line in file:
                line = line.strip().split()
                x, y, w, h = float(line[1]), float(line[2]), float(line[3]), float(line[4])
                x1, y1, x2, y2 = __xywhn2xyxy(np.array([x, y, w, h])[None], w=width, h=height)
                w, h = x2 - x1, y2 - y1
                out_dict = {
                    'id': annotation_id,
                    'image_id': images_dict[label[:-4]],
                    'bbox': [x1, y1, w, h],
                    'category_id': int(line[0]) + 1,
                    'segmentation': [],
                    'area': float(f"{w * h:.4f}"),
                    'iscrowd': 0,
                    'attributes': {'occluded': False}}
                if confidence:
                    out_dict['confidence'] = float(line[5])
                annotations.append(out_dict)
                annotation_id += 1

    coco = {'images': images_coco, 'categories': categories, 'annotations': annotations}
    with open(coco_json, 'w') as f:
        json.dump(coco, f)


if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser(description='Convert coco annotation to yolo format')
    # parser.add_argument('--annotation_file', type=str, required=True, help='coco json file path')
    # parser.add_argument('--output_folder', type=str, help='output folder path to save yolo format files')
    # parser.add_argument('--input_folder', type=str, default=None, help='original images folder or yolo folder')
    # parser.add_argument('--use', type=str, default='coco_to_yolo', help='convert to yolo or coco')
    # args = parser.parse_args()
    # if args.use == 'coco_to_yolo':
    #     coco_to_yolo(args.annotation_file, args.output_folder, args.input_folder)
    # elif args.use == 'yolo_to_coco':
    #     yolo_to_coco(args.input_folder, args.annotation_file)
    coco_to_yolo('annotations/merged.json', 'out')

