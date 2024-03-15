import cv2
import numpy as np

def segment_staff_lines(img, output_directory='output', staff_line_spacing_threshold=50):
    # Convert to binary using Otsu's method
    _, binary_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Calculate the horizontal projection of the staff lines
    horizontal_projection = np.sum(binary_image, axis=1)
    # Detect staff line regions by finding where the projection is above a certain threshold
    line_regions = np.where(horizontal_projection > (np.max(horizontal_projection) / 2))[0]
    # Group the line regions into staffs based on the spacing threshold
    staffs = []
    current_staff = []
    for i in range(1, len(line_regions)):
        if line_regions[i] - line_regions[i - 1] > staff_line_spacing_threshold:
            if current_staff:
                staffs.append(current_staff)
                current_staff = []
        current_staff.append(line_regions[i])
    if current_staff:  # Add the last staff if it exists
        staffs.append(current_staff)
    
    # Segment and save each staff
    for i, staff in enumerate(staffs):
        # Find the top and bottom of the staff
        top = max(0, min(staff) - staff_line_spacing_threshold)
        bottom = min(img.shape[0], max(staff) + staff_line_spacing_threshold)
        
        # Extract and save the staff segment
        staff_segment = img[top:bottom]
        staff_segment_filename = f"{output_directory}/staff_segment_{i + 1}.jpg"
        cv2.imwrite(staff_segment_filename, staff_segment)
    
    print(f"Segmented and saved {len(staffs)} staffs to {output_directory}.")