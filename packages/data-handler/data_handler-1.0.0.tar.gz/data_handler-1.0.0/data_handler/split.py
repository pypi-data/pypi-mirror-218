"""Functions to split data into training and validation sets on both coco and yolo formats as well as
    creating a new annotation file for a given subset of images in the folder."""
import json
import os
import random
import shutil

from pathlib import Path
from tqdm import tqdm

random.seed(42)

def annotation_folder(image_folder, annotation_file,  output_annotation_file):
    """Create annotation file for a given subset of images in the folder.
    
    Args:
        image_folder (str): path to the folder containing the images to filter annotations for.
        annotation_file (str): path to the annotation file.
        output_annotation_file (str): path to the output annotation file.
    """
    data = json.load(open(annotation_file))
    annotations = data['annotations']
    images = data['images']
    images_in_use = os.listdir(image_folder)

    image_list = []
    image_id_list = []
    for image in tqdm(images, desc='Creating annotation file for images in folder'):
        if image['file_name'] in images_in_use:
            image_id_list.append(image['id'])
            image_list.append(image)

    annotation_list = []
    for annotation in tqdm(annotations, desc='Annotations for images in folder'):
        if annotation['image_id'] in image_id_list:
            annotation_list.append(annotation)

    data['annotations'] = annotation_list
    data['images'] = image_list
    with open(output_annotation_file, "w") as outfile:
        json.dump(data, outfile)

def train_validation_coco(folder, annotation_file, combined_folder=None, output_folder=None, validation_percentage=10):
    """split coco data into training and validation

    Args:
        folder (str): path to image folder
        annotation_file (str): path to annotation file
        combined_folder (str, optional): Path to combined folder for training and validation.
            Both will be stored in the same folder with 'train_' and 'val_' names. Defaults to None.
        output_folder (str, optional): Path to parent folder which will have seperate training and validation folders. Defaults to None.
        validation_percentage (int, optional): Percentage of images to put in validation set. Defaults to 10.

    Raises:
        Exception: If both combined_folder and output_folder are None.
    """
    if output_folder is None and combined_folder is None:
        raise Exception('Either output_folder or combined_folder must be specified')
    if output_folder is not None:
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        if not os.path.exists(os.path.join(output_folder, 'train')):
            os.mkdir(os.path.join(output_folder, 'train'))
        if not os.path.exists(os.path.join(output_folder, 'train', 'annotations')):
            os.mkdir(os.path.join(output_folder, 'train', 'annotations'))
        if not os.path.exists(os.path.join(output_folder, 'train', 'images')):
            os.mkdir(os.path.join(output_folder, 'train', 'images'))

        if not os.path.exists(os.path.join(output_folder, 'validation')):
            os.mkdir(os.path.join(output_folder, 'validation'))
        if not os.path.exists(os.path.join(output_folder, 'validation', 'annotations')):
            os.mkdir(os.path.join(output_folder, 'validation', 'annotations'))
        if not os.path.exists(os.path.join(output_folder, 'validation', 'images')):
            os.mkdir(os.path.join(output_folder, 'validation', 'images'))

    data = json.load(open(annotation_file))
    annotations = data['annotations']
    images = data['images']
    image_ids = []
    old_train_list, old_val_list = [], []
    for image in images:
        if image['file_name'].find('val') == -1 or image['file_name'].find('train') == -1:
            image_ids.append(image['id'])
        elif image['file_name'].find('val') != -1:
            old_val_list.append(image['id'])
        elif image['file_name'].find('train') != -1:
            old_train_list.append(image['id'])
    
    random.shuffle(image_ids)
    validation_size = int(len(image_ids) * validation_percentage / 100)
    validation_image_ids = image_ids[:validation_size]
    validation_image_ids.extend(old_val_list)
    train_image_ids = image_ids[validation_size:]
    train_image_ids.extend(old_train_list)

    if output_folder is not None:

        validation_annotation_list, training_annotation_list = [], []
        for annotation in annotations:
            if annotation['image_id'] in validation_image_ids:
                validation_annotation_list.append(annotation)
            elif annotation['image_id'] in train_image_ids:
                training_annotation_list.append(annotation)

        validation_image_list, training_image_list = [], []
        for image in tqdm(images, desc='output folder'):
            if image['id'] in validation_image_ids:
                if image['file_name'].find('val') != -1:
                    shutil.copy(os.path.join(folder, image['file_name']),
                                os.path.join(output_folder, 'validation', 'images', image['file_name']))
                else:
                    adding = 'val_'
                    counter = 1
                    while os.path.exists(os.path.join(folder, adding + image['file_name'])):
                        adding = 'val_' + str(counter) + '_'
                        counter += 1
                    shutil.copy(os.path.join(folder, image['file_name']), 
                                os.path.join(output_folder, 'validation', 'images', adding + image['file_name']))
                    new_image = image.copy()
                    new_image['file_name'] = adding + new_image['file_name']
                validation_image_list.append(new_image)

            elif image['id'] in train_image_ids:
                if image['file_name'].find('train') != -1:
                    shutil.copy(os.path.join(folder, image['file_name']), 
                                os.path.join(output_folder, 'train', 'images', image['file_name']))
                else:
                    adding = 'train_'
                    counter = 1
                    while os.path.isfile(os.path.join(folder, adding + image['file_name'])):
                        adding = 'train_' + str(counter) + '_'
                        counter += 1
                    shutil.copy(os.path.join(folder, image['file_name']),
                                os.path.join(output_folder, 'train', 'images', adding + image['file_name']))
                    new_image = image.copy()
                    new_image['file_name'] = adding + new_image['file_name']
                training_image_list.append(new_image)
        
        data['annotations'] = validation_annotation_list
        data['images'] = validation_image_list
        with open(os.path.join(output_folder, 'validation', 'annotations', 'instances_val.json'), "w") as outfile:
            json.dump(data, outfile)

        data['annotations'] = training_annotation_list
        data['images'] = training_image_list
        with open(os.path.join(output_folder, 'train', 'annotations', 'instances_train.json'), "w") as outfile:
            json.dump(data, outfile)

    if combined_folder is not None:

        if not os.path.exists(combined_folder):
            os.mkdir(combined_folder)
            if not os.path.exists(os.path.join(combined_folder, 'annotations')):
                os.mkdir(os.path.join(combined_folder, 'annotations'))
            if not os.path.exists(os.path.join(combined_folder, 'images')):
                os.mkdir(os.path.join(combined_folder, 'images'))

        image_list = []
        for image in tqdm(images, desc='combined folder'):
            if image['file_name'].find('val') != -1:
                shutil.copy(os.path.join(folder, image['file_name']), 
                            os.path.join(combined_folder, 'images', image['file_name']))
            elif image['file_name'].find('train') != -1:
                shutil.copy(os.path.join(folder, image['file_name']),
                            os.path.join(combined_folder, 'images', image['file_name']))
            else:
                if image['id'] in validation_image_ids:
                    adding = 'val_'
                    counter = 1
                    while os.path.exists(os.path.join(folder, adding + image['file_name'])):
                        adding = 'val_' + str(counter) + '_'
                        counter += 1
                    shutil.copy(os.path.join(folder, image['file_name']), 
                                os.path.join(combined_folder, 'images', adding + image['file_name']))
                    image['file_name'] = adding + image['file_name']
                else:
                    adding = 'train_'
                    counter = 1
                    while os.path.isfile(os.path.join(folder, adding + image['file_name'])):
                        adding = 'train_' + str(counter) + '_'
                        counter += 1
                    shutil.copy(os.path.join(folder, image['file_name']),
                                os.path.join(combined_folder, 'images', adding + image['file_name']))
                    image['file_name'] = adding + image['file_name']
            image_list.append(image)
        data['annotations'] = annotations
        data['images'] = image_list
        with open(os.path.join(combined_folder, 'annotations', 'instances_all.json'), "w") as outfile:
            json.dump(data, outfile)    

def train_validation_yolo(folder, output_folder, validation_percentage=10):
    """ split yolo data into training and validation

    Args:
        folder (str): path to folder containing yolo data
        output_folder (str): path to folder to save split data
        validation_percentage (int): percentage of data to use for validation
    """

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    if not os.path.exists(os.path.join(output_folder, 'train')):
        os.mkdir(os.path.join(output_folder, 'train'))
    if not os.path.exists(os.path.join(output_folder, 'train', 'labels')):
        os.mkdir(os.path.join(output_folder, 'train', 'labels'))
    if not os.path.exists(os.path.join(output_folder, 'train', 'images')):
        os.mkdir(os.path.join(output_folder, 'train', 'images'))

    if not os.path.exists(os.path.join(output_folder, 'val')):
        os.mkdir(os.path.join(output_folder, 'val'))
    if not os.path.exists(os.path.join(output_folder, 'val', 'labels')):
        os.mkdir(os.path.join(output_folder, 'val', 'labels'))
    if not os.path.exists(os.path.join(output_folder, 'val', 'images')):
        os.mkdir(os.path.join(output_folder, 'val', 'images'))

    data = []
    for img in os.listdir(os.path.join(folder, 'images')):
        if img.find('val') == -1 and img.find('train') == -1:
            data.append(img)
            
    random.shuffle(data)
    validation_size = int(len(data) * validation_percentage / 100)
    validation_data = data[:validation_size]
    training_data = data[validation_size:]

    for img in tqdm(os.listdir(os.path.join(folder, 'images')), desc='Copying images'):
        if img.find('val') != -1:
            shutil.copy(os.path.join(folder, 'images', img),
                        os.path.join(output_folder, 'val', 'images', img))
            if  os.path.exists(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt')):
                shutil.copy(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt'),
                            Path(os.path.join(output_folder, 'val', 'labels', img)).with_suffix('.txt'))
        elif img.find('train') != -1:
            shutil.copy(os.path.join(folder, 'images', img),
                        os.path.join(output_folder, 'train', 'images', img))
            if  os.path.exists(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt')):
                shutil.copy(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt'),
                            Path(os.path.join(output_folder, 'train', 'labels', img)).with_suffix('.txt'))
        elif img in validation_data:
            adding = 'val_'
            counter = 1
            while os.path.isfile(os.path.join(folder, 'images', adding + img)):
                adding = 'val_' + str(counter) + '_'
                counter += 1
            shutil.copy(os.path.join(folder, 'images', img),
                        os.path.join(output_folder, 'val', 'images', adding + img))
            if  os.path.exists(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt')):
                shutil.copy(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt'),
                            Path(os.path.join(output_folder, 'val', 'labels', adding + img)).with_suffix('.txt'))
        elif img in training_data:
            adding = 'train_'
            counter = 1
            while os.path.isfile(os.path.join(folder, 'images', adding + img)):
                adding = 'train_' + str(counter) + '_'
                counter += 1
            shutil.copy(os.path.join(folder, 'images', img),
                        os.path.join(output_folder, 'train', 'images', adding + img))
            if  os.path.exists(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt')):
                shutil.copy(Path(os.path.join(folder, 'labels', img)).with_suffix('.txt'),
                            Path(os.path.join(output_folder, 'train', 'labels', adding + img)).with_suffix('.txt'))

    if os.path.exists(os.path.join(folder, 'input_data.yaml')):
        shutil.copy(os.path.join(folder, 'input_data.yaml'),
                    os.path.join(output_folder, 'input_data.yaml'))

if __name__ == '__main__':
    import sys
    train_validation_yolo('/home/vardan/Desktop/testing/yolo', '/home/vardan/Desktop/testing/yoloout', 20)