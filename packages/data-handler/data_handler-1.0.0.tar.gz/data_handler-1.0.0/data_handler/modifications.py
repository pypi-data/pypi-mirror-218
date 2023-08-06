"""Functions to do modifications on the dataset like removing small annotations,
    applying augmentations, RATT, or using SimCLR to generate diverse data and removing redundant data."""
import json
import os
import random
import shutil
import subprocess

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

def remove_small_annotations(annotation_file, output_annotation_file, categories, category_ratios):
    """Removes annotations that are smaller than the specified ratio compared to the image size

    Args:
        annotation_file (str): path to the annotation file
        output_annotation_file (str): path to the output annotation file
        categories (list of strings): list of categories to remove annotations from.
        category_ratios (list of float): list of categories ratios to use as threshold.

        Example for sb2:
        categories = ['fire', 'smoke', 'person', 'person_with_head_gear', 'person_with_helmet', 'person_with_hardhat', # first is none as ids start from 1
        'backpack', 'handbag', 'suitcase', 'laptop', 'cell_phone', 'car', 'truck', 'motorcycle', 'bicycle', 'bus',
        'person_with_gloves', 'person_with_safety_googles', 'safety_vest', 'forklift', 'atm', 'helmet']
        category_ratios = [0, 0.0015, 0.0015, 0.0015, 0.0003, 0.0003, 0.0003,
        0.00075, 0.00075, 0.00075, 0.0003, 0.00015, 0.0015, 0.003, 0.0012, 0.0012, 0.003,
        0.00015, 0.00015, 0.00075, 0.0015, 0.0015, 0.0003]
    """
    data = json.load(open(annotation_file))
    images = data['images']
    annotations = data['annotations']
    categories_dict = {}
    for cat in data['categories']:
        if cat['name'] in categories:
            categories_dict[cat['id']] = [category_ratios[categories.index(cat['name'])], 0, cat['name']]

    image_dict = {}
    for image in images:
        image_dict[image['id']] = (image['width'] * image['height'], image['file_name'])

    annotation_list = []
    for annotation in tqdm(annotations):
        if annotation['category_id'] in categories_dict.keys() and annotation['area'] < image_dict[annotation['image_id']][0] * categories_dict[annotation['category_id']][0]:
            categories_dict[annotation['category_id']][1] += 1
        else:
            annotation_list.append(annotation)

    data['annotations'] = annotation_list
    with open(output_annotation_file, 'w') as f:
        json.dump(data, f)

    print('categories removed')
    for val in categories_dict.values():
        print("%s: %d" % (val[2], val[1]))

def visualize_small_annotations(image_folder, annotation_file, categories, category_ratios, category_colors=None):
    """Visualizes annotations that are smaller than the specified ratio compared to the image size

    Args:
        image_folder (str): path to the folder containing the images
        annotation_file (str): path to the annotation file
        categories (list of str): list of categories to remove annotations from.
        category_ratios (list of float): list of categories ratios to use as threshold.
        category_colors (list of tuples, optional): list of color tuples to use for drawing on image per category. Defaults to None.

        Example for sb2:
        cats = ['fire', 'smoke', 'person', 'person_with_head_gear', 'person_with_helmet', 'person_with_hardhat', # first is none as ids start from 1
        'backpack', 'handbag', 'suitcase', 'laptop', 'cell_phone', 'car', 'truck', 'motorcycle', 'bicycle', 'bus',
        'person_with_gloves', 'person_with_safety_googles', 'safety_vest', 'forklift', 'atm', 'helmet']
        category_ratios = [0.0015, 0.0015, 0.0015, 0.0003, 0.0003, 0.0003, # first is zero as ids start from 1
            0.00075, 0.00075, 0.00075, 0.0003, 0.00015, 0.0015, 0.003, 0.0012, 0.0012, 0.003,
            0.00015, 0.00015, 0.00075, 0.0015, 0.0015, 0.0003]
        r, g, b, y = (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255)
        category_colors = [b, b, g, r, r, r,
            b, b, b, b, b, y, y, y, y, y,
            r, r, r, y, y, r]
    """
    data = json.load(open(annotation_file))
    images = data['images']
    annotations = data['annotations']
    categories_dict = {}
    category_colors = category_colors if category_colors is not None else [(0, 0, 255)] * len(categories)
    for cat in data['categories']:
        if cat['name'] in categories:
            categories_dict[cat['id']] = (category_ratios[categories.index(cat['name'])],
                                          cat['name'],
                                          category_colors[categories.index(cat['name'])])
    image_dict = {}
    for image in images:
        image_dict[image['id']] = (image['width'] * image['height'], image['file_name'])

    for annotation in annotations:
        if annotation['category_id'] in categories_dict.keys() and annotation['area'] < image_dict[annotation['image_id']][0] * categories_dict[annotation['category_id']][0]:
    
            img = cv2.imread(os.path.join(image_folder, image_dict[annotation['image_id']][1]))
            bbox = annotation['bbox']
            h, w = img.shape[:2]
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), categories_dict[annotation['category_id']][2], 2)
            cv2.putText(img, categories_dict[annotation['category_id']][1], (int(w/2), int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, categories_dict[annotation['category_id']][2], 1)
            
            if max(h, w) > 1024:
                ratio = 1024 / max(h, w)
                img = cv2.resize(img, None, fx = ratio, fy = ratio)
            cv2.imshow('image', img)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()

def simclr_train(folder, checkpoint='trained_simclr.ckpt', batch_size=8, input_size=64, epochs=100):
    """Trains a SimCLR model
    
    Args:
        folder (str): path to the folder containing the images
        checkpoint (str, optional): path to the checkpoint file to save the model. Defaults to 'trained_simclr.ckpt'.
        batch_size (int, optional): batch size to use for training. Defaults to 8. Use as big as possible.
        input_size (int, optional): size of the input image. Defaults to 64. Use as big as possible.
        epochs (int, optional): number of epochs to train the model. Defaults to 100.
    """
    import lightly

    if checkpoint[-5:] != '.ckpt':
        print('checkpoint must be a .ckpt file')
        return
    ckpt = lightly.train_embedding_model(input_dir=folder, loader={'batch_size': batch_size}, collate={'input_size': input_size}, trainer={'max_epochs': epochs})
    os.rename(ckpt, checkpoint)

def simclr_generate_data(folder, num_cluster, output_folder, checkpoint='whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth', batch_size=16, input_size=256):
    """Generates data for a SimCLR model using KMeans clustering to pick the most representative images
    
    Args:
        folder (str): path to the folder containing the images
        num_cluster (int): number of clusters to use for KMeans clustering. Per cluster one image is chosen hence size is equal to num_clusters.
        output_folder (str): path to the folder to save the generated data.
        checkpoint (str, optional): path to the checkpoint file to load the model. Defaults to 'whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth'.
        batch_size (int, optional): batch size to use for inference. Defaults to 16.
        input_size (int, optional): size of the input image. Defaults to 256.
    """

    import lightly
    from sklearn.cluster import KMeans

    if not os.path.isfile(checkpoint):
        import wget
        print('checkpoint not found, downloading')
        wget.download('https://storage.googleapis.com/models_boris/whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth')
    embeddings, _, filenames = lightly.embed_images(checkpoint, input_dir=folder, collate={'input_size': input_size}, loader={'batch_size': batch_size})

    df = pd.DataFrame(embeddings)
    X = df.to_numpy()

    clusters = min(num_cluster, len(os.listdir(folder)))
    Kmean = KMeans(n_clusters=clusters, max_iter=500)
    Kmean.fit(X)
    centers = Kmean.cluster_centers_
    res = list(Kmean.predict(X))

    Dict = {}
    for i in range(clusters):
        Dict[i] = [10**6, '']

    for x, cluster, filename in zip(X, res, filenames):
        # print(x, centers[cluster], filename)
        val = sum([(i - j)**2 for i, j in zip(x, centers[cluster])]) ** 0.5
        if Dict[cluster][0] > val:
            Dict[cluster] = [val, filename]

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for _, filename in Dict.values():
        shutil.copy(os.path.join(folder, filename), os.path.join(output_folder, filename))

def simclr_remove_same_data(folder, output_folder, files_removed_folder=None, distance=0.9985, checkpoint='whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth', batch_size=16, input_size=256):
    """Removes similar images from a folder using cosing distance
    
    Args:
        folder (str): path to the folder containing the images
        output_folder (str): path to the folder to save the distinct data.
        files_removed_folder (str, optional): path to the folder to save the removed images. Saved only is some value passed. Defaults to None.
        distance (float, optional): distance to use for cosine distance. Defaults to 0.9985.
        checkpoint (str, optional): path to the checkpoint file to load the model. Defaults to 'whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth'.
        batch_size (int, optional): batch size to use for inference. Defaults to 16.
        input_size (int, optional): size of the input image. Defaults to 256."""
    import lightly
    from sklearn.metrics.pairwise import cosine_similarity

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    if files_removed_folder is not None and not os.path.exists(files_removed_folder):
        os.mkdir(files_removed_folder)

    if not os.path.isfile(checkpoint):
        import wget
        print('checkpoint not found, downloading')
        wget.download('https://storage.googleapis.com/models_boris/whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth')
    embeddings, _, filenames = lightly.embed_images(checkpoint, input_dir=folder, collate={'input_size': input_size}, loader={'batch_size': batch_size})

    df = pd.DataFrame(embeddings)
    res = cosine_similarity(df)
    files_to_use = []
    files_not_to_use = []
    Dict = {}
    for i, row in enumerate(tqdm(res)):
        if i in files_not_to_use:
            continue
        files_to_use.append(i)
        for j in range(i+1, len(row)):
            if i != j and row[j] >= distance:
                files_not_to_use.append(j)
                if i not in Dict.keys():
                    Dict[i] = [(j, row[j])]
                else:
                    Dict[i].append((j, row[j]))

    files_not_to_use = list(set(files_not_to_use))
    files_to_use = list(set(files_to_use))

    print('Number of files removed:', len(files_not_to_use))

    if files_removed_folder is not None:
        for i in files_not_to_use:
            shutil.copy(os.path.join(folder, filenames[i]), os.path.join(files_removed_folder, filenames[i]))
    for i in files_to_use:
        shutil.copy(os.path.join(folder, filenames[i]), os.path.join(output_folder, filenames[i]))

def ratt(annotation_file, output_annotation_file, random_percentage=5, max_num_per_image=6, category_size={}):
    """Generates random annotations for a some percentage of the dataset
    
    Args:
        annotation_file (str): path to the annotation file.
        output_annotation_file (str): path to the output annotation file.
        random_percentage (int, optional): percentage of the dataset to generate random annotations. Defaults to 5.
        max_num_per_image (int, optional): maximum number of random annotations per image. Defaults to 6.
        category_size (dict, optional): dictionary containing the minimum and maximum width and height of each annotation. Defaults to {}.
            Example: {'person': [50, 100, 150, 350]} # minimum width, maximum width, minimum height, maximum height
    """
    data = json.load(open(annotation_file))
    images = data['images']
    annotations = data['annotations']
    categories = data['categories']
    image_ids = []
    widths = []
    heights = []
    for image in images:
        if random.random() > (1 - random_percentage / 100) and image['file_name'].find('val') == -1:
            image_ids.append(image['id'])
            widths.append(image['width'])
            heights.append(image['height'])
    print('Number of images selected for random annotations:', len(image_ids))

    max_id = 0
    annotation_list = []
    for annotation in annotations:
        max_id = max(annotation['id'], max_id)
        if annotation['image_id'] not in image_ids:
            annotation_list.append(annotation)

    category_dict = {}
    category_ids = []
    for category in categories:
        if category['name'] in category_size.keys():
            category_dict[category['id']] = category_size[category['name']]
        category_ids.append(category['id'])

    for width, height, image_id in zip(widths, heights, image_ids):
        for i in range(random.randint(0, max_num_per_image)):
            max_id += 1
            category = random.choice(category_ids)
            x0 = random.randint(0, width)
            y0 = random.randint(0, height)
            if category not in category_dict.keys():
                width_x = random.randint(50, width - 50)
                height_y = random.randint(50, height - 50)
            else:
                width_x = random.randint(max(category_dict[category][0], 0), min(category_dict[category][1], width))
                height_y = random.randint(max(category_dict[category][2]), min(category_dict[category][3], height))

            if x0 + width_x > width - 1:
                if random.random() > 0.5:
                    x0 = width - width_x - 1
                else:
                    width_x = width - x0 - 1

            if y0 + height_y > height - 1:
                if random.random() > 0.5:
                    y0 = height - height_y - 1
                else:
                    height_y = height - y0 - 1
            
            
            Dict = {
                        "id": max_id,
                        "image_id": image_id,
                        "category_id": category,
                        "segmentation": [],
                        "area": width_x * height_y,
                        "bbox": 
                        [
                            x0,
                            y0,
                            width_x,
                            height_y
                        ],
                        "iscrowd": 0,
                        "attributes": 
                        {
                            "occluded": False
                        }
                    }   
            annotation_list.append(Dict)
    data['annotations'] = annotation_list
    with open(output_annotation_file, "w") as outfile:
        json.dump(data, outfile)

def __check_occurrence(key, Dict):
    if key in Dict.keys():
        return Dict[key]
    Dict = {
        'GaussianBlur': 0.35,
        'CLAHE': 0.35,
        'GlassBlur': 0.35,
        'Equalize': 0.35,
        'ISONoise': 0.35,
        'MotionBlur': 0.35,
        'Posterize': 0.35,
        'RandomBrightnessContrast': 0.35,
        'GaussNoise': 0.35,
        'ImageCompression': 0.35,
        'ChannelShuffle': 0.15,
        'RandomToneCurve': 0.35,
        'RGBShift': 0.35,
        'FDA': 0.15
        }
    return Dict[key]

def augment(folder, annotation_file, output_folder, image_percentage=50, prob_dict={
    'GaussianBlur': 0.35,
    'CLAHE': 0.35,
    'GlassBlur': 0.35,
    'Equalize': 0.35,
    'ISONoise': 0.35,
    'MotionBlur': 0.35,
    'Posterize': 0.35,
    'RandomBrightnessContrast': 0.35,
    'GaussNoise': 0.35,
    'ImageCompression': 0.35,
    'ChannelShuffle': 0.15,
    'RandomToneCurve': 0.35,
    'RGBShift': 0.35,
    'FDA': 0.15
}):
    """Augments the dataset with some random transformations

    Args:
        folder (str): path to the folder containing the images.
        annotation_file (str): path to the annotation file.
        output_folder (str): path to the output folder.
        image_percentage (int, optional): percentage of the dataset to augment. These many images will be duplicated and augmented. Defaults to 50. 
        prob_dict (dict, optional): dictionary containing the probabilities of each augmentation being applied. If any augmentation is not specified in dictionary these default values will be used for that.
        Defaults to {'GaussianBlur': 0.35,
                     'CLAHE': 0.35,
                     'GlassBlur': 0.35, 
                     'Equalize': 0.35,
                     'ISONoise': 0.35,
                     'MotionBlur': 0.35, 
                     'Posterize': 0.35, 
                     'RandomBrightnessContrast': 0.35, 
                     'GaussNoise': 0.35, 
                     'ImageCompression': 0.35, 
                     'ChannelShuffle': 0.15, 
                     'RandomToneCurve': 0.35, 
                     'RGBShift': 0.35, 
                     'FDA': 0.15}.
    """
    import albumentations as A
    import wget

    if not os.path.exists('fda_target_images'):
        os.mkdir('fda_target_images')
    wget.download('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkhfbtiVKOKUsR5QAJl33QPaSlve-I7YHraw&usqp=CAU', out='fda_target_images/one.jpg')
    wget.download('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0z3NrgPhY8Vpn-RWG7Kl7PcAxejMsBpO-Hg&usqp=CAU', out='fda_target_images/two.jpg')

    data = json.load(open(annotation_file))
    categories = data['categories']
    images = data['images']
    annotations = data['annotations']

    cat_dict = {}
    for category in categories:
        cat_dict[category['id']] = category['name']

    image_dict = {}
    for image in images:
        image_dict[image['id']] = image['file_name']

    albumentation = {}
    for image in images:
        albumentation[image_dict[image['id']]] = []

    for annotation in annotations:
        bbox = annotation['bbox']
        bbox.append(cat_dict[annotation['category_id']])
        albumentation[image_dict[annotation['image_id']]].append(bbox)

    sample_images = list(albumentation.keys())
    image_id = 1
    annotation_id = 1
    image_dict = []
    annotation_dict = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(os.path.join(output_folder, 'images')):
        os.makedirs(os.path.join(output_folder, 'images'))
    if not os.path.exists(os.path.join(output_folder, 'annotations')):
        os.makedirs(os.path.join(output_folder, 'annotations'))
    
    for image in tqdm(sample_images, desc='Augmenting images'):
        img = cv2.imread(os.path.join(folder, image))
        height, width = img.shape[:2]
        bbox_label = albumentation[image]

        for i, bbox_lab in enumerate(bbox_label):
            if bbox_lab[0] + bbox_lab[2] > width:
                bbox_label[i][2] = width - bbox_lab[0]
            if bbox_lab[1] + bbox_lab[3] > height:
                bbox_label[i][3] = height - bbox_lab[1]

        file_name = image
        cv2.imwrite(os.path.join(output_folder, 'images', file_name), img)

        image_dict.append({"id": image_id, "width": width, "height": height, "file_name": file_name, "license": 0, "flickr_url": "", "coco_url": "", "date_captured": 0})
        for bbox_lab in bbox_label:
            bbox = bbox_lab[:-1]
            class_name = bbox_lab[-1]
            area = bbox_lab[2] * bbox_lab[3]
            category_id = next(item for item in categories if item['name'] == class_name)['id']
            annotation_dict.append({"id": annotation_id, "image_id": image_id, "category_id": category_id, "segmentation": [], "area": area, "bbox": bbox, "iscrowd": 0, "attributes": {"occluded": False}})
            annotation_id += 1
        image_id += 1

        transform = A.Compose([
            A.GaussianBlur(blur_limit=(5, 7), sigma_limit=1, p=__check_occurrence('GaussianBlur', prob_dict)),
            A.CLAHE(clip_limit=6.0, tile_grid_size=(12, 12), p=__check_occurrence('CLAHE', prob_dict)),
            A.GlassBlur(sigma=0.7, max_delta=2, iterations=1, p=__check_occurrence('GlassBlur', prob_dict)),
            A.Equalize(p=__check_occurrence('Equalize', prob_dict)),
            A.ISONoise(color_shift=(0.015, 0.06), intensity=(0.15, 0.6), p=__check_occurrence('ISONoise', prob_dict)),
            A.MotionBlur(blur_limit=(5, 9), p=__check_occurrence('MotionBlur', prob_dict)),
            A.Posterize(p=__check_occurrence('Posterize', prob_dict)),
            A.RandomBrightnessContrast(brightness_limit=[0, 0.25], contrast_limit=[0, 0.25], p=__check_occurrence('RandomBrightnessContrast', prob_dict)),
            A.GaussNoise(var_limit=(15, 55), p=__check_occurrence('GaussNoise', prob_dict)),
            A.ImageCompression(quality_lower=10, quality_upper=25, p=__check_occurrence('ImageCompression', prob_dict)),
            A.ChannelShuffle(p=__check_occurrence('ChannelShuffle', prob_dict)),
            A.RandomToneCurve(scale=0.9, p=__check_occurrence('RandomToneCurve', prob_dict)),
            A.RGBShift(p=__check_occurrence('RGBShift', prob_dict)),
            A.FDA(['fda_target_images/one.jpg', 'fda_target_images/two.jpg'], beta_limit=0.05, p=__check_occurrence('FDA', prob_dict))
        ], bbox_params=A.BboxParams(format='coco'))

        if random.random() > (1 - image_percentage / 100) and file_name.find('val') == -1:
            try:
                random.seed(random.randint(0, 5000))
                transformed = transform(image=img, bboxes=bbox_label)
                transformed_image = transformed['image']
                transformed_bboxes = transformed['bboxes']
                file_name = image[:-4] + '_aug' + image[-4:]
                cv2.imwrite(os.path.join(output_folder, 'images', file_name), transformed_image)
                t_h, t_w = transformed_image.shape[:2]
                image_dict.append({"id": image_id, "width": t_w, "height": t_h, "file_name": file_name, "license": 0, "flickr_url": "", "coco_url": "", "date_captured": 0})

                for bbox_lab in transformed_bboxes:
                    bbox = bbox_lab[:-1]
                    class_name = bbox_lab[-1]
                    area = bbox_lab[2] * bbox_lab[3]
                    category_id = next(item for item in categories if item['name'] == class_name)['id']
                    annotation_dict.append({"id": annotation_id, "image_id": image_id, "category_id": category_id, "segmentation": [], "area": area, "bbox": bbox, "iscrowd": 0, "attributes": {"occluded": False}})
                    annotation_id += 1

                image_id += 1
            except:
                pass

    coco_annotation = {'categories': categories,
                       'images': image_dict,
                       'annotations': annotation_dict}

    with open(os.path.join(output_folder, 'annotations', 'annotation.json'), 'w') as outfile:
        json.dump(coco_annotation, outfile)


def __visualize_bbox(img, bbox, class_name, thickness=2):
    """Visualizes a single bounding box on the image"""
    BOX_COLOR = (255, 0, 0) # Blue
    TEXT_COLOR = (255, 255, 255) # White
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=BOX_COLOR, thickness=thickness)

    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(
        img,
        text=class_name,
        org=(x_min, y_min - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35,
        color=TEXT_COLOR,
        lineType=cv2.LINE_AA,
    )
    return img


def __visualize(image, bboxes):
    img = image.copy()
    for bbox in (bboxes):
        img = __visualize_bbox(img, bbox[:-1], bbox[-1])
    return img

def visualize_augment(folder, annotation_file, prob_dict={
    'GaussianBlur': 0.35,
    'CLAHE': 0.35,
    'GlassBlur': 0.35,
    'Equalize': 0.35,
    'ISONoise': 0.35,
    'MotionBlur': 0.35,
    'Posterize': 0.35,
    'RandomBrightnessContrast': 0.35,
    'GaussNoise': 0.35,
    'ImageCompression': 0.35,
    'ChannelShuffle': 0.15,
    'RandomToneCurve': 0.35,
    'RGBShift': 0.35,
    'FDA': 0.15
}):
    """Visualizes the augmented images

    Args:
        folder (str): The folder where the images are stored
        annotation_file (str): Path to the annotation file
        prob_dict (dict, optional): dictionary containing the probabilities of each augmentation being applied. If any augmentation is not specified in dictionary these default values will be used for that.
        Defaults to {'GaussianBlur': 0.35,
                     'CLAHE': 0.35,
                     'GlassBlur': 0.35, 
                     'Equalize': 0.35,
                     'ISONoise': 0.35,
                     'MotionBlur': 0.35, 
                     'Posterize': 0.35, 
                     'RandomBrightnessContrast': 0.35, 
                     'GaussNoise': 0.35, 
                     'ImageCompression': 0.35, 
                     'ChannelShuffle': 0.15, 
                     'RandomToneCurve': 0.35, 
                     'RGBShift': 0.35, 
                     'FDA': 0.15}.
    """

    import albumentations as A
    import wget

    if not os.path.exists('fda_target_images'):
        os.mkdir('fda_target_images')
    if not os.path.isfile('fda_target_images/one.jpg'):
        wget.download('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkhfbtiVKOKUsR5QAJl33QPaSlve-I7YHraw&usqp=CAU', out='fda_target_images/one.jpg')
    if not os.path.isfile('fda_target_images/two.jpg'):
        wget.download('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0z3NrgPhY8Vpn-RWG7Kl7PcAxejMsBpO-Hg&usqp=CAU', out='fda_target_images/two.jpg')

    data = json.load(open(annotation_file))
    categories = data['categories']
    images = data['images']
    annotations = data['annotations']

    cat_dict = {}
    for category in categories:
        cat_dict[category['id']] = category['name']

    image_dict = {}
    for image in images:
        image_dict[image['id']] = image['file_name']

    albumentation = {}
    for image in images:
        albumentation[image_dict[image['id']]] = []

    for annotation in annotations:
        bbox = annotation['bbox']
        bbox.append(cat_dict[annotation['category_id']])
        albumentation[image_dict[annotation['image_id']]].append(bbox)

    sample_images = list(albumentation.keys())
    
    for image in sample_images:
        img = cv2.imread(os.path.join(folder, image))
        height, width = img.shape[:2]
        bbox_label = albumentation[image]

        for i, bbox_lab in enumerate(bbox_label):
            if bbox_lab[0] + bbox_lab[2] > width:
                bbox_label[i][2] = width - bbox_lab[0]
            if bbox_lab[1] + bbox_lab[3] > height:
                bbox_label[i][3] = height - bbox_lab[1]

        transform = A.Compose([
            A.GaussianBlur(blur_limit=(5, 7), sigma_limit=1, p=__check_occurrence('GaussianBlur', prob_dict)),
            A.CLAHE(clip_limit=6.0, tile_grid_size=(12, 12), p=__check_occurrence('CLAHE', prob_dict)),
            A.GlassBlur(sigma=0.7, max_delta=2, iterations=1, p=__check_occurrence('GlassBlur', prob_dict)),
            A.Equalize(p=__check_occurrence('Equalize', prob_dict)),
            A.ISONoise(color_shift=(0.015, 0.06), intensity=(0.15, 0.6), p=__check_occurrence('ISONoise', prob_dict)),
            A.MotionBlur(blur_limit=(5, 9), p=__check_occurrence('MotionBlur', prob_dict)),
            A.Posterize(p=__check_occurrence('Posterize', prob_dict)),
            A.RandomBrightnessContrast(brightness_limit=[0, 0.25], contrast_limit=[0, 0.25], p=__check_occurrence('RandomBrightnessContrast', prob_dict)),
            A.GaussNoise(var_limit=(15, 55), p=__check_occurrence('GaussNoise', prob_dict)),
            A.ImageCompression(quality_lower=10, quality_upper=25, p=__check_occurrence('ImageCompression', prob_dict)),
            A.ChannelShuffle(p=__check_occurrence('ChannelShuffle', prob_dict)),
            A.RandomToneCurve(scale=0.9, p=__check_occurrence('RandomToneCurve', prob_dict)),
            A.RGBShift(p=__check_occurrence('RGBShift', prob_dict)),
            A.FDA(['fda_target_images/one.jpg', 'fda_target_images/two.jpg'], beta_limit=0.05, p=__check_occurrence('FDA', prob_dict))
        ], bbox_params=A.BboxParams(format='coco'))

        random.seed(random.randint(0, 5000))
        transformed = transform(image=img, bboxes=bbox_label)
        transformed_image = transformed['image']
        transformed_bboxes = transformed['bboxes']
        augmented = __visualize(transformed_image, transformed_bboxes)
        cv2.imshow('original', img)
        cv2.imshow('augmented', augmented)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    visualize_small_annotations('/home/vardan/Desktop/testing/annotations.json', '/home/vardan/Desktop/testing/images', ['person'], [0.01])