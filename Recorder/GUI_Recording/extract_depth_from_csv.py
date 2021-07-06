#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 20:55:04 2021

@author: salih
"""
import pandas
import numpy as np
import cv2

# Path of the file created by extractor. CHANGE this to desired path
filepath = "/home/salih/Documents/realsense-workspace/star/Intel RealSense D435I"

# default sub-topic names in the bag file.
depth_data_file = "/_device_0_sensor_0_Depth_0_image_data.csv"
depth_meta_data_file = "/_device_0_sensor_0_Depth_0_info_camera_info.csv"

# obtain width and height of the recording
meta_data = pandas.read_csv(filepath + depth_meta_data_file)
width = meta_data["width"][0]
height = meta_data["height"][0]
del meta_data

# read depth frames. this takes a while
depth_data = pandas.read_csv(filepath + depth_data_file)["data"]

# depth data is held as 8 bit, for every frame convert it to 16 bit by shifting and adding
i = 0
for frame in depth_data:
    
    data_8bit_seperated = np.array(frame[1:-1].split(", "), dtype=np.uint16).reshape((height, 2 * width))
    data_16bit = (data_8bit_seperated[:,0::2] + (data_8bit_seperated[:,1::2] << 8))
    
    # now data_16bit have the depth value of each pixel in an height x width array
    # save in image format
    cv2.imwrite(filepath + "/frame_" + str(i) + ".png", data_16bit)
    i += 1
    
    