#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:05:55 2024

@author: sebinjohn
"""

import glob
import cv2
import os

images=glob.glob("/Users/sebinjohn/gq_proj/Results/before and after relocation/*/2*.png")

def create_video(images, video_name, fps=1):
    # Get all the images from the folder
 
    images.sort()  # Ensure the images are in the correct order

    # Read the first image to get dimensions
    first_image = cv2.imread(os.path.join(images[0]))
    height, width, _ = first_image.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # 'H264' for high-quality .mp4
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))
    # Iterate over the images and write them into the video
    for image in images:
        img = cv2.imread((image))
        video.write(img)

    # Release the video writer object
    video.release()

    print(f"Video {video_name} has been created successfully.")


video_name = '/Users/sebinjohn/gq_proj/Results/before and after relocation/output_video.mp4'  # Name of the output video file
create_video(images, video_name)
