from pathlib import Path


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


main_folder = Path.cwd()
image_folder = Path('ImageFolder')
# if ImageFolder doesnt exists create the folder -->
if not image_folder.exists():
    image_folder.mkdir(parents=True)
    print('ImageFolder directory created. Run the code again.')
    quit()

file_list = image_folder.iterdir()
# if there are image inside it
# Rename them and move them
image_list = rename_images(file_list)


# Treat the images making copies with the desired effect and/or comparison mode
# Effects: BW, extraction of colors (paleta), RGB total values, extraction of color (solo el lineart)
