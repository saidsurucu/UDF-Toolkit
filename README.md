# UDF Toolkit

A collection of tools for working with the UYAP UDF file format.

[![Star History Chart](https://api.star-history.com/svg?repos=saidsurucu/udf-toolkit&type=Date)](https://www.star-history.com/#saidsurucu/udf-toolkit&Date)

## Installation

1.  **Install Python:** If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/). Make sure to check the "Add Python to PATH" option during installation.
2.  **Download the Code:** Click the green "Code" button on the top right of this page and select "Download ZIP". Extract the contents of the ZIP file to a folder on your computer.
3.  **Install Dependencies:** Navigate to the project's root directory and double-click the `install_reqs.bat` script located in the `scripts` folder. This will install the necessary Python packages.

## Usage

### For Technical Users (Command Line)

To use the scripts from the command line, run the following commands from the root directory of the project:

-   **Convert UDF to DOCX:**
    ```
    python -m src.udf_to_docx input.udf
    ```
-   **Convert UDF to PDF:**
    ```
    python -m src.udf_to_pdf input.udf
    ```
-   **Convert DOCX to UDF:**
    ```
    python -m src.docx_to_udf input.docx
    ```
    *Note: For best results, run this on Windows. Converting some DOCX features requires Windows libraries. Results may vary on macOS and Linux.*
-   **Convert Scanned PDF to UDF:**
    ```
    python -m src.scanned_pdf_to_udf input.pdf
    ```

### For Non-Technical Users (Drag and Drop on Windows)

The easiest way to use the toolkit on Windows is to use the batch scripts located in the `scripts` folder.

1.  **`install_reqs.bat`:**
    -   **Purpose:** Installs the required Python packages listed in `requirements.txt`.
    -   **How to Use:** Double-click the `install_reqs.bat` script. This will install all the necessary dependencies.
2.  **`udf_to_docx.bat`:**
    -   **Purpose:** Converts a UDF file to DOCX format.
    -   **How to Use:** Drag and drop a `.udf` file onto the `udf_to_docx.bat` script. The script will run and create a `.docx` file in the same directory as the input file.
3.  **`udf_to_pdf.bat`:**
    -   **Purpose:** Converts a UDF file to PDF format.
    -   **How to Use:** Drag and drop a `.udf` file onto the `udf_to_pdf.bat` script. The script will run and create a `.pdf` file in the same directory as the input file.
4.  **`docx_to_udf.bat`:**
    -   **Purpose:** Converts a DOCX file to UDF format.
    -   **How to Use:** Drag and drop a `.docx` file onto the `docx_to_udf.bat` script. The script will run and create a `.udf` file in the same directory as the input file.
5.  **`scanned_pdf_to_udf.bat`:**
    -   **Purpose:** Converts a scanned PDF file to UDF format.
    -   **How to Use:** Drag and drop a `.pdf` file onto the `scanned_pdf_to_udf.bat` script. The script will run and create a `.udf` file in the same directory as the input file.

## UDF Format Documentation

For detailed information about the UDF format, please see the [UDF Format Documentation](./docs/Docs.md).
