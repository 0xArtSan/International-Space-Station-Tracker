from pathlib import Path


def rename(directory_list_files):
    rename_list = []
    for item in directory_list_files:
        if item.is_file():
            rename_list.append(item)

    counter = 1
    for item in rename_list:
        extension = item.suffix
        new_name = str(f"{counter:03d}") + extension
        try:
            item.rename(Path(image_folder, new_name))
        except:
            pass
        counter += 1
    return rename_list


main_folder = Path.cwd()
image_folder = Path('ImageFolder')
# if ImageFolder exists -->
if image_folder.exists():
    file_list = image_folder.iterdir()
    # if there are image inside it
    # Rename them
    image_list = rename(file_list)


# TO DO
#   create a folder in the same fashion ("000001") and put there all the images
#   Treat the images making copies with the desired effect and/or comparison mode

## Effects: BW, extraction of colors (paleta), RGB total values, extraction of color (solo el lineart)