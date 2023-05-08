from functions import *

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


options_treatment = ['bw', 'palette', 'contour']
options_copies = ['copies', 'comparison', 'both']
treated_image_list = []

print('Welcome! For more info write help')

treatment = input('What image treatment do you want?(bw, palette, contour) ')
copies = input('Do you want copies, comparison or both? ')

help_message = 'Help message'

if treatment == 'help' or treatment not in options_treatment or copies == 'help' or copies not in options_copies:
    print(help_message)
    exit()

if treatment == 'bw':
    for item in image_list:
        treated_image_list.append(black_white(item))
elif treatment == 'palette':
    for item in image_list:
        treated_image_list.append(palette(item))
elif treatment == 'contour':
    for item in image_list:
        treated_image_list.append(contour(item))

# TODO: finish copies: save the new images with different names...
if copies == 'copies' or copies == 'both':
    for item in treated_image_list:
        pass
