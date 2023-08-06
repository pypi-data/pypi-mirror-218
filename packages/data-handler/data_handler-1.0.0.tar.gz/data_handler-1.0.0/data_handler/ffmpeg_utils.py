"""Supports splitting video into frames and combining a folder of images."""
import os
import shutil
import subprocess

from tqdm import tqdm

def split_video_into_frames(video, output_folder):
    """Split a video into frames.
    
    Args:
        video: path to the video file.
        output_folder: path to the output folder.
    """
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    process = subprocess.Popen(["ffmpeg", "-i", video, os.path.join(output_folder, "out%06d.jpg")], stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)

def combine_image_folders(folder, output_folder):
    """Combine all image folders in a given folder into a single folder with individual folder
    names as the prefix to each file.

    Args:
        folder (str): path to folder containing image folders
        output_folder (str): path to output folder
    """
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    for f in tqdm(os.listdir(folder), desc="Combining image folders"):
        if os.path.isdir(os.path.join(folder, f)):
            for g in os.listdir(os.path.join(folder, f)):
                if g.endswith((".jpg", ".png", "jpeg")):
                    shutil.copy(os.path.join(folder, f, g), os.path.join(output_folder, f + "_" + g))

if __name__ =='__main__':
    import sys
    combine_image_folders(sys.argv[1], sys.argv[2])
