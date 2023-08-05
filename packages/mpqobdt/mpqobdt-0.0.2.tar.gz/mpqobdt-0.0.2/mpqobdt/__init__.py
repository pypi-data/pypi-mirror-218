import sys
import cv2
import os
lib_path = (os.path.split(os.path.realpath(__file__))[0])
sys.path.append(lib_path)
from My_OBDT_train import *
from My_OBDT_detect import *

# -*- coding utf-8 -*-
"""
Created on May 18th 09:41 2023

@auther: Peiqi Miao

"""
def ob_Train():
    ob_train()

def ob_Detect():
    ob_detect()


if __name__ == '__main__':
    print()
