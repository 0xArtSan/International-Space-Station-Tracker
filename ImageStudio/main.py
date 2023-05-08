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
new_file_list = no_webp(image_folder)
# Creating a new directory and renaming files (leaves behind .webp images)
image_list = rename_images(new_file_list)

# TODO: Ask the desired treatment and if they want copies and/or comparison images
