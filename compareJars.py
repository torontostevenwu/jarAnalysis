import zipfile
import os
import filecmp
import argparse
import json
import shutil
import tempfile

def extract_jar(jar_path, extract_to):
    """Extracts a JAR/ZIP file to a specified directory."""
    with zipfile.ZipFile(jar_path, 'r') as jar:
        jar.extractall(extract_to)

def compare_directories(dir1, dir2):
    """Compares two directories and returns added, removed, and modified files."""
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

def main():
    parser = argparse.ArgumentParser(description="Compare two JAR or ZIP files.")
    parser.add_argument("jar1", help="Path to the first JAR/ZIP file")
    parser.add_argument("jar2", help="Path to the second JAR/ZIP file")
    parser.add_argument("--output", help="Path to save the comparison results (JSON format)")
    
    args = parser.parse_args()

    # Create temporary directories
    temp_dir1 = tempfile.mkdtemp()
    temp_dir2 = tempfile.mkdtemp()

    try:
        print(f"Comparing {args.jar1} and {args.jar2}...")
        
        extract_jar(args.jar1, temp_dir1)
        extract_jar(args.jar2, temp_dir2)

        added, removed, modified = compare_directories(temp_dir1, temp_dir2)

        results = {
            "added_files": added,
            "removed_files": removed,
            "modified_files": modified
        }

        print("\nComparison Results:")
        print(f"Added files: {len(added)}")
        for f in added:
            print(f"  + {f}")
            
        print(f"Removed files: {len(removed)}")
        for f in removed:
            print(f"  - {f}")
            
        print(f"Modified files: {len(modified)}")
        for f in modified:
            print(f"  * {f}")

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=4)
            print(f"\nResults saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Cleanup
        shutil.rmtree(temp_dir1)
        shutil.rmtree(temp_dir2)

if __name__ == "__main__":
    main()

