# JAR/ZIP Analysis Tool

This project provides a tool for comparing the contents of two JAR or ZIP files. It helps identify files that have been added, removed, or modified between two versions of an archive.

The project consists of two main components:
1.  **`app.py`**: A user-friendly web application built with Streamlit for uploading and comparing files via a browser interface.
2.  **`compareJars.py`**: A standalone Python script for comparing files programmatically (currently hardcoded paths).

## Features

-   **Upload & Compare**: Upload two JAR or ZIP files to compare them.
-   **Detailed Analysis**:
    -   **Added Files**: Lists files present in the second archive but not the first.
    -   **Removed Files**: Lists files present in the first archive but not the second.
    -   **Modified Files**: Lists files present in both but with different content.
-   **Visual Interface**: Easy-to-read results using the Streamlit web app.

## Prerequisites

-   Python 3.x
-   pip (Python package installer)

## Installation

1.  Clone or download this repository.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The main dependency is `streamlit`)*

## Usage

### Running the Web App (Recommended)

1.  Navigate to the project directory in your terminal.
2.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
3.  A browser window will open (usually at `http://localhost:8501`).
4.  Upload your two JAR/ZIP files and click "Compare JARs/ZIPs".

### Running the Script

1.  Open your terminal.
2.  Run the script with the paths to your JAR/ZIP files:
    ```bash
    python compareJars.py path/to/file1.jar path/to/file2.jar
    ```
3.  **Optional**: Export the results to a JSON file:
    ```bash
    python compareJars.py path/to/file1.jar path/to/file2.jar --output results.json
    ```

## Testing

To run the unit tests:
```bash
python -m unittest test_compareJars.py
```