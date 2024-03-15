import cv2
import numpy as np

def convert_to_grayscale_and_remove_noise(img, img_name, output_directory='output'):
    print(img_name, output_directory)
    # se=cv2.getStructuringElement(cv2.MORPH_RECT , (1,1))
    # bg=cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
    denoised_img = cv2.fastNlMeansDenoising(img, None, 5, 7, 21)

    # Adaptive thresholding with a smaller block size
    binary_img = cv2.adaptiveThreshold(denoised_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                       cv2.THRESH_BINARY, 15, 2)
    
    # Optional: Smaller kernel for morphological operations
    # 1 and 2 because of the staff line is thin vertically and horizontally is long
    # And so it would not delete staff line acidentlly
    kernel = np.ones((1, 2), np.uint8)
    refined_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(f'{output_directory}/{img_name}.jpg', refined_img)

    return refined_img
