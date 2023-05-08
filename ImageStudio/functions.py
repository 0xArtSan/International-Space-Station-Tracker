import cv2 as cv
from pathlib import Path
import extcolors
from PIL import Image
import numpy as np


# Input: The path where the files must be to be processed
# Output: A list of the paths to all files in the image directory with .webp images filtered out
# Function: Check all files and converts all .webp images to .png
def no_webp(directory):
    # Create a list of all the data that is inside image_folder
    file_list = directory.iterdir()
    for item in file_list:
        # Checking files only and if the file is a .webp image
        if item.is_file() and item.suffix == '.webp':
            # Converting all .webp images to png
            image = Image.open(item).convert('RGB')
            new_path = f'ImageFolder/{item.stem}.png'
            image.save(new_path, 'png')
    filtered_list = []
    file_list = directory.iterdir()
    for item in file_list:
        if item.is_file() and item.suffix != '.webp':
            filtered_list.append(item)
    return filtered_list


# Input:
# Output:
# Function:
def create_directory():
    counter = 0
    while Path(f"{counter:03d}").exists():
        counter += 1
    new_folder = Path(f"{counter:03d}")
    new_folder.mkdir(parents=True)
    return new_folder


# Input:
# Output:
# Function:
def rename_images(filtered_list):
    new_folder = create_directory()

    rename_counter = 1
    for item in filtered_list:
        extension = item.suffix
        new_name = str(f"{rename_counter:03d}") + extension
        try:
            item.rename(Path(new_folder, new_name))
        except:
            rename_counter += 1
            item.rename(Path(new_folder, new_name))
        rename_counter += 1
    return new_folder.iterdir()


# Input:
# Output:
# Function:
def black_white(original_image):
    image = cv.imread(original_image)
    bw_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return bw_image


# TODO: escribir el codigo de color y el % en cada cuadrado
# Input:
# Output:
# Function:
def palette(original_image):
    image = Image.open(original_image)
    color, pixel_count = extcolors.extract_from_image(image)
    color_palette = []
    counter = 0
    for item in color:
        percentage = (item[1]/pixel_count)*100
        counter += 1
        color_palette.append((item[0], percentage))
        if counter > 8:
            image = cv.imread(original_image)
            height, width, channels = image.shape
            image_palette = np.zeros((height, width, 3), dtype=np.uint8)
            coordinate_1 = int(height/3)
            coordinate_2 = int(width/3)
            counter_2 = 0
            for i in range(3):
                for j in range(3):
                    top = (coordinate_1*j, coordinate_2*i)
                    bot = (coordinate_1*(j+1), coordinate_2*(i+1))
                    cv.rectangle(image_palette, (top), (bot), (color_palette[counter_2][0]), -1)
                    counter_2 += 1
            return image_palette


# Input:
# Output:
# Function:
def contour(original_image):
    image = cv.imread(original_image)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    edges = cv.Canny(image_gray, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    height, width, channels = image.shape
    image_contour = 255*np.ones((height, width, 3), dtype=np.uint8)
    cv.drawContours(image_contour, contours, -1, (0, 0, 0), 1)
    return image_contour


# Input:
# Output:
# Function:
def compound(original_image, modified_image):
    image_1 = cv.imread(original_image)
    compounded_image = cv.hconcat([image_1, modified_image])
    return compounded_image


test_path = '000/001.png'
# print(palette('000/001.png'))
x = palette(test_path)
cv.imshow('bandw', x)
cv.waitKey(0)
cv.destroyAllWindows()
