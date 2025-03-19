#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:29:53 2024

@author: sebinjohn
"""

import cv2
import os

def create_video_from_images(image_folder, output_video, frame_rate=30):
    # Get all image files from the folder
    images = [img for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()  # Ensure the images are in the correct order
    
    # Read the first image to get frame dimensions
    if not images:
        raise ValueError("No images found in the folder.")
    
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))
    
    # Loop through images and write to video
    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)
    
    # Release the video writer object
    video.release()
    print(f"Video saved as {output_video}")

# Example usage
image_folder = '/Users/sebinjohn/gq_proj/Results/Landsat/video_making'
output_video = '/Users/sebinjohn/gq_proj/Results/Landsat/video_making/output_video.mp4'
frame_rate = 5  # Adjust frame rate as needed

create_video_from_images(image_folder, output_video, frame_rate)



image_folder = '/Users/sebinjohn/gq_proj/Results/cl_ndsi/'
output_video = '/Users/sebinjohn/gq_proj/Results/cl_ndsi/output_video.mp4'
frame_rate = 5  # Adjust frame rate as needed

create_video_from_images(image_folder, output_video, frame_rate)


image_folder = '/Users/sebinjohn/gq_proj/Results/edge_detection'
output_video = '/Users/sebinjohn/gq_proj/Results/edge_detection/output_video.mp4'
frame_rate = 5  # Adjust frame rate as needed

create_video_from_images(image_folder, output_video, frame_rate)
