"""
 Description: Simple script to move *vtu files to a single folder
 Author: Francisco Jimenez
 Date Created: 2023-12-19
 Python version: 3.10
 Dependencies: None
"""

import os
current = os.getcwd()
folder = os.path.basename(current)
number = folder.split('.')[-1]
os.system('cp res/magnet_rod_t0001.vtu ../results/rotation_' + str(number) + '.vtu') #filename = f"../{folder}/res"
