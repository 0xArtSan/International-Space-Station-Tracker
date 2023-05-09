from functions import *

print('Welcome! For more info write help')

treatment = input('What image treatment do you want?(bw, palette, contour) ')
if treatment == 'help':
    print(help_message)
    exit()

copies = input('Do you want a copy, comparison or both? ')

if treatment not in options_treatment or copies not in options_copies:
    print(help_message)
    exit()

print("I'll let you know when I'm done")
# Path where main is
main_folder = Path.cwd()
# Path where the images must be to be treated
image_folder = Path('ImageFolder')
# If prior directory doesn't exist, create it and exit
if not image_folder.exists():
    image_folder.mkdir(parents=True)
    print('ImageFolder directory created. Run the code again.')
    exit()

# Checking if there are any .webp file and convert it to .png
no_webp_image_list = no_webp(image_folder)
# Creating a new directory and renaming files (leaves behind .webp images)
image_list = rename_images(no_webp_image_list)
path_list = list(image_list)

treated_image_list = []
if treatment == 'bw':
    for path in path_list:
        treated_image = black_white(path)
        treated_image_list.append(treated_image)
elif treatment == 'palette':
    for path in path_list:
        treated_image = palette(path)
        treated_image_list.append(treated_image)
elif treatment == 'contour':
    for path in path_list:
        treated_image = contour(path)
        treated_image_list.append(treated_image)

counter = 0
if copies == 'copy' or copies == 'both':
    for item in treated_image_list:
        save_and_name(item, path_list[counter], 'copy')
        counter += 1

if copies == 'comparison' or copies == 'both':
    counter = 0
    for item in treated_image_list:
        compounded_image = compound(path_list[counter], item)
        save_and_name(compounded_image, path_list[counter], copies)
        counter += 1

print('Done')
