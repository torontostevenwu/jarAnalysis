import streamlit as st
import os
import zipfile
import filecmp
import tempfile
import shutil

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

st.title("JAR/ZIP File Comparison Tool")

uploaded_file1 = st.file_uploader("Upload first JAR/ZIP file", type=["jar", "zip"])
uploaded_file2 = st.file_uploader("Upload second JAR/ZIP file", type=["jar", "zip"])

compare_button = st.button("Compare JARs/ZIPs")

if compare_button:
    if uploaded_file1 is not None and uploaded_file2 is not None:
        # Create temporary directories for JARs and their contents
        temp_dir1 = tempfile.mkdtemp()
        temp_dir2 = tempfile.mkdtemp()
        jar1_content_path = os.path.join(temp_dir1, "jar1_contents")
        jar2_content_path = os.path.join(temp_dir2, "jar2_contents")
        os.makedirs(jar1_content_path)
        os.makedirs(jar2_content_path)

        # Define paths for saved JAR files
        jar1_path = os.path.join(temp_dir1, uploaded_file1.name)
        jar2_path = os.path.join(temp_dir2, uploaded_file2.name)

        try:
            # Save uploaded JAR files
            with open(jar1_path, "wb") as f:
                f.write(uploaded_file1.getbuffer())
            with open(jar2_path, "wb") as f:
                f.write(uploaded_file2.getbuffer())

            # Extract JAR contents
            extract_jar(jar1_path, jar1_content_path)
            extract_jar(jar2_path, jar2_content_path)

            # Compare the directories
            added_files, removed_files, modified_files = compare_directories(jar1_content_path, jar2_content_path)

            # Display results
            st.subheader("Comparison Results:")
            if not added_files and not removed_files and not modified_files:
                st.success("No differences found between the JAR/ZIP files.")
            else:
                if added_files:
                    st.write("Files added in the second JAR/ZIP (compared to the first):")
                    for f in added_files:
                        st.markdown(f"- `{f}`")
                if removed_files:
                    st.write("Files removed in the second JAR/ZIP (compared to the first):")
                    for f in removed_files:
                        st.markdown(f"- `{f}`")
                if modified_files:
                    st.write("Files modified between the JARs/ZIPs:")
                    for f in modified_files:
                        st.markdown(f"- `{f}`")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

        finally:
            # Clean up temporary directories
            shutil.rmtree(temp_dir1)
            shutil.rmtree(temp_dir2)
            
    else:
        st.warning("Please upload both JAR/ZIP files before comparing.")
