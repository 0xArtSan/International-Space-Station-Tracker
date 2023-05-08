import cv2 as cv
from pathlib import Path
import extcolors
from PIL import Image


# Input: The path where the files must be to be processed
# Output: A list of the paths to all files in the image directory
# Function: Check all files and converts all .webp images to .png
def no_webp(directory):
    # Create a list of all the data that is inside image_folder
    file_list = directory.iterdir()
    for item in file_list:
        # Checking files only
        if item.is_file():
            # Checking if the file is a .webp image
            if item.suffix == '.webp':
                # Converting all .webp images to png
                image = Image.open(item).convert('RGB')
                new_path = f'ImageFolder/{item.stem}.png'
                image.save(new_path, 'png')
    return directory.iterdir()


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
def rename_images(directory_list_files):
    new_folder = create_directory()
    rename_list = []
    for item in directory_list_files:
        if item.is_file() and item.suffix != '.webp':
            rename_list.append(item)

    rename_counter = 1
    for item in rename_list:
        extension = item.suffix
        new_name = str(f"{rename_counter:03d}") + extension
        try:
            item.rename(Path(new_folder, new_name))
        except:
            rename_counter += 1
            item.rename(Path(new_folder, new_name))
        rename_counter += 1
    return rename_list


# Input:
# Output:
# Function:
def black_white(original_image):
    image = cv.imread(original_image)
    bw_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return bw_image


# TODO: crear una imagen de 3x3 con los colores extraidos
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
            return color_palette


# TODO: crear una imagen sobre fondo blanco con las mismas dimensiones que la imagen original y el contorno dibujado
# Input:
# Output:
# Function:
def contour(original_image):
    image = cv.imread(original_image)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(image_gray, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image_gray, contours, -1, (0, 0, 0), 1)


# Input:
# Output:
# Function:
def compound(original_image, modified_image):
    image_1 = cv.imread(original_image)
    image_2 = cv.imread(modified_image)
    compounded_image = cv.hconcat([image_1, image_2])
    return compounded_image


# test_path = '000/001.jpg'
# no_webp('000/001.png')
# cv.imshow('bandw', bw_image)
# cv.waitKey(0)
# cv.destroyAllWindows()
