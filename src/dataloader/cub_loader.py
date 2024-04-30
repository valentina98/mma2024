import os
import os.path
import shutil
import sys

import pandas
import wget
import tarfile

from PIL import Image
from tqdm import tqdm

from src import definitions

DOWNLOAD_URL = 'https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz?download=1'
TAR_FILE_PATH = os.path.join(definitions.DOWNLOADS_DIR, 'cub_dataset.tgz')
TEMP_DIR = os.path.join(definitions.DATA_DIR, 'temp')
IMAGES_SIZE = (120, 120)

def download_data(tar_file_path):

    def bar_progress(current, total, _):
        sys.stdout.write("\r" + "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))
        sys.stdout.flush()

    wget.download(DOWNLOAD_URL, bar=bar_progress, out=tar_file_path)


def extract_data(tar_file_path, dataset_dir):
    with tarfile.open(tar_file_path) as file:
        file.extractall(dataset_dir)


def create_csv(images_dir):
    data = []
    for bird_class_id, bird_dir in enumerate(os.listdir(images_dir)):
        bird_type = bird_dir.split('.')[1].replace('_', ' ')
        bird_images = os.listdir(os.path.join(images_dir, bird_dir))
        data += [
            [bird_class_id, bird_type, os.path.join(images_dir, bird_dir, image_name)]
            for image_name in bird_images
        ]
    return pandas.DataFrame(data, columns=['class_id', 'class_name', 'image_path']).reset_index(names='image_id')

def resize_images(images_dir):
    for bird_dir_name in tqdm(os.listdir(images_dir)):
        bird_dir = os.path.join(images_dir, bird_dir_name)
        for image_name in os.listdir(bird_dir):
            image_path = os.path.join(bird_dir, image_name)
            image = Image.open(os.path.join(bird_dir, image_name))
            image.thumbnail(IMAGES_SIZE)
            image.save(image_path)

def load():
    if not os.path.isdir(definitions.DATASET_DIR):
        os.mkdir(definitions.DATASET_DIR)
    shutil.rmtree(definitions.DATA_DIR, ignore_errors=True)
    os.mkdir(definitions.DATA_DIR)
    if not os.path.isdir(definitions.DOWNLOADS_DIR):
        os.mkdir(definitions.DOWNLOADS_DIR)
    if not os.path.isfile(TAR_FILE_PATH):
        print('Downloading CUB dataset from', DOWNLOAD_URL, 'to', TAR_FILE_PATH)
        download_data(TAR_FILE_PATH)
    else:
        print('CUB dataset found at', TAR_FILE_PATH, 'skipping download')
    print('Extracting data')
    extract_data(TAR_FILE_PATH, TEMP_DIR)
    shutil.move(os.path.join(TEMP_DIR, 'CUB_200_2011', 'images'), definitions.IMAGES_DIR)
    shutil.rmtree(TEMP_DIR)
    create_csv(definitions.IMAGES_DIR).to_csv(definitions.DATASET_PATH, index=False)
    print('Writing dataset to', definitions.DATASET_PATH)

def cleanup():
    print('Resizing images')
    resize_images(definitions.IMAGES_DIR)


if __name__ == '__main__':
    load()
    #cleanup()
