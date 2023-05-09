import cv2 as cv
from pathlib import Path
import extcolors
from PIL import Image
import numpy as np


# Input: The path where the files must be to be processed (ImageFolder/)
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


# Input: -
# Output: Returns the path for the new directory in which the images will be renamed and treated
# Function: Will check the closest directory name between 000 and 999 and make the directory first available
def create_directory():
    counter = 0
    while Path(f"{counter:03d}").exists():
        counter += 1
    new_folder = Path(f"{counter:03d}")
    new_folder.mkdir(parents=True)
    return new_folder


# Input: Takes a list of paths to the images that are not .webp
# Output: The list of all renamed and moved images in the new directory
# Function: Renames and moves all images to the new directory
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
    new_list = new_folder.iterdir()
    return new_list


# Input: The path to an images that is going to be treated
# Output: An image (np array) in black and white
# Function: Opens the path and converts it to black and white
def black_white(original_image):
    image = cv.imread(str(original_image))
    bw_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    bw_image = cv.cvtColor(bw_image, cv.COLOR_GRAY2BGR)
    return bw_image


# Input: The path to an images that is going to be treated
# Output: An image with the same shape as the original divided in 9 rectangles colored with the 9 more common colors of the image and its percentage
# Function: Extracts the 9 more common colors of the image and then draws the new image with the colors and percentages
def palette(original_image):
    image = Image.open(str(original_image))
    color, pixel_count = extcolors.extract_from_image(image)
    color_palette = []
    for item in color:
        percentage = str(round((item[1]/pixel_count)*100, 2)) + '%'
        color_palette.append((item[0], percentage))

    image = cv.imread(str(original_image))
    height, width, channels = image.shape
    image_palette = np.zeros((height, width, 3), dtype=np.uint8)
    coordinate_y = int(height/3)
    coordinate_x = int(width/3)
    counter_2 = 0
    color_number = len(color_palette)

    for i in range(3):
        for j in range(3):
            top = (coordinate_x*j, coordinate_y*i)
            bot = (coordinate_x*(j+1), coordinate_y*(i+1))
            if color_number > counter_2 or counter_2 > 8:
                cv.rectangle(image_palette, top, bot, (color_palette[counter_2][0]), -1)
                cv.putText(image_palette, str(color_palette[counter_2][0]), (top[0], top[1]+int(width/6)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, 2)
                cv.putText(image_palette, str(color_palette[counter_2][0]), (top[0], top[1]+int(width/6)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, 2)
                cv.putText(image_palette, str(color_palette[counter_2][1]), (top[0], top[1]+int(width/6)+25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, 2)
                cv.putText(image_palette, str(color_palette[counter_2][1]), (top[0], top[1]+int(width/6)+25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, 2)
            counter_2 += 1
    return image_palette


# Input: The path to an images that is going to be treated
# Output: An image that (to its best capacity) draws the contour of the objects in the input
# Function: It extracts the contours via edge detection and draws it in a new image with the same shape as the original
def contour(original_image):
    image = cv.imread(str(original_image))
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    edges = cv.Canny(image_gray, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    height, width, channels = image.shape
    image_contour = 255*np.ones((height, width, 3), dtype=np.uint8)
    cv.drawContours(image_contour, contours, -1, (0, 0, 0), 1)
    return image_contour


# Input: It takes a path to the original image and the image that has been treated and concatenates them horizontally
# Output: An image that is the result of the horizontal concatenation of two images
# Function: It opens the path of the original image and concatenates them together horizontally
def compound(original_image, modified_image):
    image_1 = cv.imread(str(original_image))
    compounded_image = cv.hconcat([image_1, modified_image])
    return compounded_image


# Input: It takes an image (np array), the path to the original image and a method in which the image has been treated
# Output: -
# Function: Saves the modified image adding '-{method}' to the filename, so they go together in the directory
def save_and_name(image, path, method):
    name = str(path.stem)
    extension = str(path.suffix)
    directory = str(path.parent)
    filename = directory + '/' + name + '-' + method + extension
    cv.imwrite(filename, image)


help_message = "Explanation:\n" \
               "This program is design as a drawing learning tool\nas it can extract the color palette,\n" \
               "show the values\nand extract the contour of any image\n(to its best capacity)\n" \
               "This program will rename all the files in ImageFolder directory in order\nand it will convert " \
               "any .webp file to .png.\n" \
               "Also, you can choose to make a copy with the desired effect or add the original image\nand the " \
               "transformed image in a single file or both"

options_treatment = ['bw', 'palette', 'contour', 'no']
options_copies = ['copy', 'comparison', 'both', 'no']
