import refine
import adjust
import segment
import cv2
import numpy as np
import sys  
import os

def process_music_score(input_path, img_name, output_path="output", mode=None):
    '''Process music score based on the provided mode.'''
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if mode is None:
        ''' 1. Denoise and binarize '''
        denoised_img = refine.convert_to_grayscale_and_remove_noise(img, img_name, output_path)
        ''' 2. Correct rotation and perspective '''
        correct_img = adjust.correct_rotation_and_perspective(denoised_img, img_name, output_path)
        ''' 3. Segment staff lines '''
        segment.segment_staff_lines(correct_img, output_path)

    elif mode == '1':
        refine.convert_to_grayscale_and_remove_noise(img, img_name, output_path)
    elif mode == '2':# Assuming preprocessing is required
        adjust.correct_rotation_and_perspective(img, img_name, output_path)
    elif mode == '3':
        segment.segment_staff_lines(img, output_path)

def process_directory(input_dir, output_dir="../testSheetsProcessed"):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                input_path = os.path.join(root, file)
                img_name = file[:-4]  # Use the whole file name including extension for clarity in processing

                # Construct output path based on input directory structure, replacing base with output base
                relative_path = os.path.relpath(root, input_dir)
                current_output_dir = os.path.join(output_dir, relative_path)

                # Ensure output directory exists
                os.makedirs(current_output_dir, exist_ok=True)
                
                # Determine mode based on directory structure
                if "positionCorrection" in root:
                    mode = '2'
                else:
                    continue  # Skip if none of the conditions are met
                
                # Process image
                # print(input_path, img_name, current_output_dir)
                process_music_score(input_path, img_name, current_output_dir, mode)


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: main.py input_path output_path [mode]")
    #     sys.exit(1)

    # input_path = sys.argv[1]
    # output_path = sys.argv[2]
    # mode = sys.argv[3] if len(sys.argv) > 3 else None

    

    # process_music_score(input_path, "test", output_path, mode)

    input_dir = "../testSheets"  # Base directory to start processing from
    process_directory(input_dir)
