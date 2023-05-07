import cv2 as cv
from pathlib import Path
import extcolors
import PIL


# create a folder in the same fashion ("001") and put there all the images
def create_directory():
    counter = 0
    while Path(f"{counter:03d}").exists():
        counter += 1
    new_folder = Path(f"{counter:03d}")
    new_folder.mkdir(parents=True)

    return new_folder


def rename_images(directory_list_files):
    new_folder = create_directory()
    rename_list = []
    for item in directory_list_files:
        if item.is_file():
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


def black_white(original_image):
    image = cv.imread(original_image)
    BW_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return BW_image


def palette(original_image):
    image = PIL.Image.open(original_image)
    color, pixel_count = extcolors.extract_from_image(image)
    color_palette = []
    counter = 0
    for item in color:
        percentage = (item[1]/pixel_count)*100
        counter += 1
        color_palette.append((item[0], percentage))
        if counter > 8:
            return color_palette


def color_extraction(original_image):
    image = cv.imread(original_image)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(image_gray, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(image, contours, -1, (0, 0, 0), 1)
    cv.imshow('contours', image)
    cv.waitKey(0)
    # cv.imwrite(f'contour - {original_image}', edges)
    cv.destroyAllWindows()

## Hay que guardar el contorno en un lugar diferente
color_extraction('000/008.webp')
