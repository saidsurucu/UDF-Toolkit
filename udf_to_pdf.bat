@echo off
:: This script converts a UDF file to PDF format

REM Check if a UDF file is provided by dragging
IF "%~1"=="" (
    echo Please drag a UDF file onto this script to convert it to PDF.
    pause
    exit /b 1
)

REM Run the conversion
python udf_to_pdf.py "%~1"

REM Check if the conversion was successful
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to convert UDF to PDF.
    pause
    exit /b 1
)

echo UDF successfully converted to PDF.
pause
