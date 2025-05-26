import zipfile
import os
import filecmp


def extract_jar(jar_path, extract_to):
    with zipfile.ZipFile(jar_path, 'r') as jar:
        jar.extractall(extract_to)

def compare_directories(dir1, dir2):
    added_files = []
    removed_files = []
    modified_files = []

    for root, _, files in os.walk(dir1):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), dir1)
            if not os.path.exists(os.path.join(dir2, file_path)):
                removed_files.append(file_path)
            elif not filecmp.cmp(os.path.join(dir1, file_path), os.path.join(dir2, file_path), shallow=False):
                modified_files.append(file_path)

    for root, _, files in os.walk(dir2):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), dir2)
            if not os.path.exists(os.path.join(dir1, file_path)):
                added_files.append(file_path)

    return added_files, removed_files, modified_files

# Paths to the JAR files
jar1 = './j2eeOld.jar'
jar2 = './j2eeNew.jar'


# Extract contents of the JAR files
extract_jar(jar1, 'jar1_contents')
extract_jar(jar2, 'jar2_contents')

# Compare the directories
added_files, removed_files, modified_files = compare_directories('jar1_contents', 'jar2_contents')

print("Added files:", added_files)
print("Removed files:", removed_files)
print("Modified files:", modified_files)

