from functions import *



main_folder = Path.cwd()
image_folder = Path('ImageFolder')
# if ImageFolder doesnt exists create the folder -->
if not image_folder.exists():
    image_folder.mkdir(parents=True)
    print('ImageFolder directory created. Run the code again.')
    exit()

file_list = image_folder.iterdir()
# if there are image inside it
# Rename them and move them
image_list = rename_images(file_list)


# Treat the images making copies with the desired effect and/or comparison mode
# Effects: BW, extraction of colors (paleta), extraction of color (solo el lineart)
