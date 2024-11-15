#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:01:52 2024

@author: sebinjohn
"""

import cv2
import os
from pdf2image import convert_from_path
import numpy as np
from PIL import Image

# Function to resize the image while maintaining aspect ratio
def resize_image_to_video_size(img, video_size):
    img_width, img_height = img.size
    video_width, video_height = video_size
    
    # Calculate the scaling factor to maintain aspect ratio
    scale_x = video_width / img_width
    scale_y = video_height / img_height
    scale = min(scale_x, scale_y)
    
    # New size based on scaling
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    
    # Resize the image
    img_resized = img.resize((new_width, new_height))
    
    # Create a new blank image (video_size) and paste the resized image on it (centered)
    new_img = Image.new("RGB", video_size, (255, 255, 255))  # White background
    offset_x = (video_width - new_width) // 2
    offset_y = (video_height - new_height) // 2
    new_img.paste(img_resized, (offset_x, offset_y))
    
    return new_img

# Function to convert PDFs to video
def pdf_to_video(pdf_folder, output_video_path, frame_rate=1, video_size=(1920, 1080)):
    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    pdf_files.sort()
    # Initialize VideoWriter to write the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use 'XVID' codec
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, video_size)

    # Loop through all PDF files
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=300)
        
        # Process each image to fit the video size and write it as a frame into the video
        for img in images:
            resized_img = resize_image_to_video_size(img, video_size)
            frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)
            video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()
    print(f"Video saved to {output_video_path}")

# Example usage
pdf_folder = '/Users/sebinjohn/gq_proj/Results/glacier_velocity'  # Path to your folder containing PDFs
output_video_path = '/Users/sebinjohn/gq_proj/Results/glacier_velocity/output_video.avi'  # Path to save the output video
pdf_to_video(pdf_folder, output_video_path)
