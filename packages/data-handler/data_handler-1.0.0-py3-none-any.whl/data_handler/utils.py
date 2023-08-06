"""Utility functions for data handling like:
1. Drawing annotations
2. Getting stats.
3. Removing categories or creating subset of dataset of particular categories.
4. Merging datasets."""

from re import I
from pycocotools.coco import COCO
import json
import os
import cv2
from tqdm import tqdm
from .coco_assistant import coco_assistant
import random
import shutil
import colorsys
from pathlib import Path

def __generate_colors(num_classes):
    # generate distict random colors
    hsv_tuples = [(x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    random.seed(10101)  # Fixed seed for consistent colors across runs.
    random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
    random.seed(None)  # Reset seed to default.
    return colors 

def draw_annotations(image_dir, annotation_file, output_dir):
    """Draw annotations on images with coco annotation file

    Args:
        image_dir (str): Path to input image directory
        annotation_file (str): Path to annotation file
        output_dir (str): Path to output image directory
    """
    random.seed(20)
    font_scale = 1

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    coco = COCO(annotation_file)
    categories = coco.loadCats(coco.getCatIds())
    category_dict = {}
    for category in categories:
        category_dict[category['id']] = category['name']

    colors_list = __generate_colors(max(coco.getCatIds())+1)

    img_ids = coco.getImgIds()
    cat_ids = coco.getCatIds()
    for img_id in tqdm(img_ids, desc='Drawing on Images'):
        img_id_list = [img_id]
        img = coco.loadImgs(img_id_list)
        image = cv2.imread(os.path.join(image_dir, img[0]['file_name']))
        ann_ids = coco.getAnnIds(imgIds=img_id_list, catIds=cat_ids)
        annotation_list = coco.loadAnns(ann_ids)
        for annotation in annotation_list:
            boxes = annotation['bbox']
            boxes[2] = boxes[0] + boxes[2]
            boxes[3] = boxes[1] + boxes[3]
            x0 = int(boxes[0])
            y0 = int(boxes[1])
            x1 = int(boxes[2])
            y1 = int(boxes[3])
            cv2.rectangle(image, (x0, y0), (x1, y1), colors_list[annotation['category_id']], 2)
            (_, _), baseline = cv2.getTextSize(
                category_dict[annotation['category_id']],
                cv2.FONT_HERSHEY_DUPLEX,
                font_scale,
                1)
            cv2.putText(image, category_dict[annotation['category_id']],
                        (x0, y0 - baseline),
                        cv2.FONT_HERSHEY_DUPLEX,
                        font_scale, colors_list[annotation['category_id']], 2)
        cv2.imwrite(os.path.join(output_dir, img[0]['file_name']), image)

def annotation_stats(annotation_file):
    """Print stats like number of instances and number of images in that category

    Args:
        annotation_file (str): coco json annotation file path
    """
    coco = COCO(annotation_file)
    print("\n%-30s %-5s      %-15s %s" % ("Category", "ID", "Instances", "Image Count"))
    for cat_id in coco.getCatIds():
        print("%-30s %-5d ---> %-15d %d" % 
            (coco.cats[cat_id]['name'], cat_id, len(coco.getAnnIds(catIds=[cat_id])), len(coco.getImgIds(catIds=[cat_id]))))

def remove_categories(annotation_file, categories, output_annotation_file, keep_blank_images=True):
    """Remove the categories from the annotation file

    Args:
        annotation_file (str): path to annotation file
        categories (list): list of categories to remove
        output_annotation_file (str): path to output annotation file
        keep_blank_images (bool): keep images with no annotations
    """
    data = json.load(open(annotation_file))
    categories_remove = [category['id'] for category in data['categories'] if category['name'] in categories]
    data['categories'] = [category for category in data['categories'] if category['name'] not in categories]
    category_images_ids = []
    image_ids = []
    annotation_list = []
    for annotation in data['annotations']:
        if annotation['category_id'] in categories_remove:
            category_images_ids.append(annotation['image_id'])
            continue
        image_ids.append(annotation['image_id'])
        annotation_list.append(annotation)
    
    if not keep_blank_images:
        image_ids_remove = list(set(category_images_ids) - set(image_ids))
        data['images'] = [image for image in data['images'] if image['id'] not in image_ids_remove]
    
    data['annotations'] = annotation_list

    with open(output_annotation_file, 'w') as f:
        json.dump(data, f)

def category_subset(image_folder, annotation_file, input_cat, output_folder="categories", max_img_per_label=-1):
    """Subset the annotation file to only include the categories specified

    Args:
        image_folder (str): Path to image folder
        annotation_file (str): Path to annotation file
        input_cat (list): List of categories to include
        output_folder (str): Path to output folder. Defaults to "categories"
        max_img_per_label (int): Maximum number of images per label. Defaults to -1, then all images are included.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(os.path.join(output_folder, "images")):
        os.makedirs(os.path.join(output_folder, "images"))
    if not os.path.exists(os.path.join(output_folder, "annotations")):  
        os.makedirs(os.path.join(output_folder, "annotations")) 

    resim_dir = Path(os.path.join(output_folder, "images"))
    resann_dir = Path(os.path.join(output_folder, "annotations"))
    
    dst_ann = Path(os.path.join(resann_dir, "annotations.json"))
    
    coco = COCO(annotation_file)
    categories = coco.loadCats(coco.getCatIds())
    category_dict = {}
    cat_Ids = []
    for category in categories:
        if category['name'] in input_cat:
            cat_Ids.append(category['id'])
        category_dict[category['name']] = category['id']
    img_id_list = []
    category_list = coco.loadCats(ids=cat_Ids)
    for cat_id in tqdm(cat_Ids, desc='Category data selection'):
        img_ids = coco.getImgIds(catIds=[cat_id])
        if max_img_per_label > 0 and len(img_ids) > max_img_per_label:
            img_ids = [img_ids[i] for i in sorted(
                random.sample(range(len(img_ids)), max_img_per_label))]
        img_id_list = img_id_list + list(set(img_ids) - set(img_id_list))
    images = coco.loadImgs(ids=img_id_list)
    ann_ids = coco.getAnnIds(catIds=cat_Ids, imgIds=img_id_list)
    annotation_list = coco.loadAnns(ann_ids)
    for image in tqdm(images, desc='Copying images'):
        source = os.path.join(image_folder, image['file_name']).replace('\\', '')
        destination = resim_dir / image['file_name'].replace('\\', '')
        shutil.copyfile(source, destination)
    
    coco_data = json.load(open(annotation_file))
    coco_data['categories'] = category_list
    coco_data['annotations'] = annotation_list
    coco_data['images'] = images
    with open(dst_ann, 'w') as outfile:
        json.dump(coco_data, outfile)

def __check_merge_structure(image_folder, annotation_folder):
    """Correct structure of merge if needed

    Args:
        image_folder (str): Path to image folder
        annotation_folder (str): Path to annotation folder
    """
    
    for folder in os.listdir(image_folder):
        path_to_remove = ''
        while True:
            files = os.listdir(os.path.join(image_folder, folder, path_to_remove))
            if len(files) == 1 and os.path.isdir(os.path.join(image_folder, folder, files[0])):
                path_to_remove = os.path.join(path_to_remove, files[0])
            else:
                if path_to_remove != '':
                    for image in os.listdir(os.path.join(image_folder, folder, path_to_remove)):
                        shutil.move(os.path.join(image_folder, folder, path_to_remove, image), os.path.join(image_folder, folder, image))
                    os.rmdir(os.path.join(image_folder, folder, path_to_remove))

                    data = json.load(open(os.path.join(annotation_folder, folder + '.json')))
                    image_list = []
                    for image in data['images']:
                        if not path_to_remove.endswith('/'):
                            path_to_remove = path_to_remove + '/'
                        image['file_name'] = image['file_name'].replace(path_to_remove, '')
                        image_list.append(image)
                    data['images'] = image_list
                    with open(os.path.join(annotation_folder, folder + '.json'), 'w') as outfile:
                        json.dump(data, outfile)
                break
                            
def merge_datasets(image_folder, annotation_folder, output_folder="merged", merge_images=True, duplicate_frames=True):
    """Merge multiple datasets into a single dataset

    Args:
        image_folder (str): Path to image folder
        annotation_folder (str): Path to annotation folder
        output_folder (str): Path to output folder. Defaults to "merged"
        merge_images (bool): Merge images. Defaults to True
        duplicate_frames (bool): Duplicate frames. Defaults to True
    """
    __check_merge_structure(image_folder, annotation_folder)
    coco_obj = coco_assistant.COCO_Assistant(image_folder, annotation_folder)
    coco_obj.merge(output_folder, merge_images, duplicate_frames)

def merge_annotations(image_folder, annotation_folder, output_folder="merged", merge_images=True):
    """Merge multiple annotations of single image into one file.
    
    Args:
        image_folder (str): Path to image folder
        annotation_folder (str): Path to annotation folder
        output_folder (str): Path to output folder. Defaults to "merged"
        merge_images (bool): Merge images. Defaults to True
    """
    __check_merge_structure(image_folder, annotation_folder)
    coco_obj = coco_assistant.COCO_Assistant(image_folder, annotation_folder)
    coco_obj.merge_same(output_folder, merge_images)

if __name__ == "__main__":
    import sys
    __check_merge_structure('/home/vardan/testing/mer/images', '/home/vardan/testing/mer/annotations')
    # draw_annotations(sys.argv[1], sys.argv[2], sys.argv[3])
