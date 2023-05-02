from pathlib import Path


def rename(directory_list_files):
    rename_list = []
    for item in directory_list_files:
        if item.is_file():
            rename_list.append(item)

    rename_counter = 1
    for item in rename_list:
        extension = item.suffix
        new_name = str(f"{rename_counter:03d}") + extension
        try:
            item.rename(Path(image_folder, new_name))
        except:
            pass
        rename_counter += 1
    return rename_list


main_folder = Path.cwd()
image_folder = Path('ImageFolder')
# if ImageFolder exists -->
if image_folder.exists():
    file_list = image_folder.iterdir()
    # if there are image inside it
    # Rename them
    image_list = rename(file_list)

# create a folder in the same fashion ("001") and put there all the images
counter = 0
try:
    new_folder = Path(f"{counter:03d}")
    new_folder.mkdir(parents=True)
except:
    counter += 1
    new_folder = Path(f"{counter:03d}")
    new_folder.mkdir(parents=True)

for item in
#   Treat the images making copies with the desired effect and/or comparison mode

## Effects: BW, extraction of colors (paleta), RGB total values, extraction of color (solo el lineart)