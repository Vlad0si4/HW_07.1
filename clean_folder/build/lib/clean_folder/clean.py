import shutil
from pathlib import Path
import zipfile
import sys

categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.svg'],
    'Documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'Archives': ['.iso', '.tar', '.gz', '.7z', '.dmg', '.rar', '.zip'],
    'Audio': ['.aac', '.m4a', '.mp3', '.ogg', '.raw', '.wav', '.wma'],
    'Video': ['.avi', '.mov', '.mp4', '.mkv'],
    'PDF': ['.pdf'],
    'Unknown': []
}

known_extensions = set()
unknown_extensions = set()


def extract_archive(file_path, extract_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f'Extracted files from {file_path} to {extract_dir}.')


def sort_files(folder_path):
    path = Path(folder_path)
    for file_path in path.glob('*'):
        if file_path.is_file():
            extension = file_path.suffix.lower()
            found_category = False
            for category, extensions in categories.items():
                if extension in extensions:
                    found_category = True
                    category_folder = path / category
                    if not category_folder.exists():
                        category_folder.mkdir()
                    shutil.move(str(file_path), str(category_folder / file_path.name))
                    print(f'Moved file {file_path.name} to {category} folder.')
                    known_extensions.add(extension)
                    break
            if not found_category:
                unknown_extensions.add(extension)
                unknown_folder = path / 'Unknown'
                if not unknown_folder.exists():
                    unknown_folder.mkdir()
                shutil.move(str(file_path), str(unknown_folder / file_path.name))
                print(f'Moved file {file_path.name} to Unknown folder.')
        elif file_path.is_dir():
            sort_files(file_path)


def main():
    try:
        folder_path = Path(sys.argv[1])
    except IndexError:
        print('Error: no path to folder provided.')
        return 1
    
    if not folder_path.exists():
        print(f"Error: the path '{folder_path}' is invalid or does not exist.")
        return 1
    
    print(f'Sorting files in {folder_path}...')
    sort_files(folder_path)

    print('\nList of files in each category:')
    for category in categories.keys():
        category_folder = folder_path / category
        print(f'{category} ({len(list(category_folder.glob("*")))}):')
        print([f.name for f in category_folder.glob("*")])

    print('\nList of known extensions:')
    print(sorted(known_extensions))
    return 0


if __name__ == "__main__":
    main()